import requests
import time
import re
import os
from datetime import datetime
from kafka import KafkaProducer #This may generate some problems with python 3.12:https://github.com/dpkp/kafka-python/issues/2412

#use secret from python file | uncomment if needed
#from secret import OPENWEATHERMAP_API_KEY
print('Starting .... ')
time.sleep(8)  # 3give the kafka broker some time to start


#Method to extract the API key from secret
def extract_api_key(api_key_string):
    # Define a regular expression pattern to match the API key
    pattern = r"OPENWEATHERMAP_API_KEY=\"([a-zA-Z0-9]+)\""

    # Use re.search to find the match in the string
    match = re.search(pattern, api_key_string)

    # Check if a match is found
    if match:
        # Return the extracted API key
        return match.group(1)
    else:
        # Return None if no match is found
        return None

#use secret in docker
secret_file_path = '/run/secrets/WeatherAPIKey'

try:
  with open(secret_file_path, 'r') as file:
    api_key_from_secret = extract_api_key(file.read().strip())
    #API Key should be loaded now, here a test:
    #print(f'The AOI key is: {api_key_from_secret}')
except FileNotFoundError:
  print(f'Secret file not foiund at {secret_file_path}')
except Exception as e:
  print(f'Error reading secret: str(e)')

# Get the OpenWeatherMap API key from the environment variable or secret from docker compose
#api_key = OPENWEATHERMAP_API_KEY
api_key = api_key_from_secret
api_endpoint = "http://api.openweathermap.org/data/2.5/weather"
city_name = "Larochette, LU"

#Kafka Configuartion and Generate Kafka Producer
kafka_bootstrap_servers = os.environ.get('KAFKA_BOOTSTRAP_SERVER', 'kafka:9092')
kafka_topic = os.environ.get('KAFKA_TOPIC', 'weather-data')

producer = KafkaProducer(
    bootstrap_servers=kafka_bootstrap_servers,
    value_serializer=lambda v: str(v).encode("utf-8")
)

#Fetch Data
def fetch_weather_data():
    parameters = {
        'q': city_name,
        'appid': api_key,
    }

    response = requests.get(api_endpoint, params=parameters)
    weather_data = response.json()
    print(f'raw_data = {weather_data}')

    #Extract Information from Data
    #print (weather_data) #Uncomment to get a list of available data
    temperature = weather_data['main']['temp']-273.15 #Change the temperature from Kelvin to degree Celsius
    humidity = weather_data['main']['humidity']
    description = weather_data['weather'][0]['description']

    # Generate a human-readable timestamp
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    #Produce Message to Kafka topic
    message = f'Time: {timestamp}, Temperature: {"%.2f" % temperature}°C, Humidity: {humidity}%, Description: {description}'
    #print (message)
    return message

refreshtime = 60 #in seconds
# Loop to send periodic updates
while True:
    # Fetch live weather data
    weather_data = fetch_weather_data()

    # Send message to Kafka topic
    producer.send(kafka_topic, value=weather_data)
    print(f'Sent: {weather_data}')

    # Wait for a specified interval (e.g., 5 minutes)
    time.sleep(refreshtime)  # 300 seconds = 5 minutes

#Close Kafka producer
producer.close()
