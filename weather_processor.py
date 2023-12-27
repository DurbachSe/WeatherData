import requests
import time
import os
from kafka import KafkaProducer #This may generate some problems with python 3.12:https://github.com/dpkp/kafka-python/issues/2412
from secret import OPENWEATHERMAP_API_KEY

# Get the OpenWeatherMap API key from the environment variable
api_key = OPENWEATHERMAP_API_KEY
api_endpoint = "http://api.openweathermap.org/data/2.5/weather"
city_name = "Larochette, LU"

#Kafka Configuartion and Generate Kafka Producer
kafka_bootstrap_servers = "localhost:9092"
kafka_topic = "weather-data"

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

    #Extract Information from Data
    #print (weather_data) #Uncomment to get a list of available data
    temperature = weather_data['main']['temp']-273.15 #Change the temperature from Kelvin to degree Celsius
    humidity = weather_data['main']['humidity']
    description = weather_data['weather'][0]['description']

    #Produce Message to Kafka topic
    message = f'Temperature: {"%.2f" % temperature}°C, Humidity: {humidity}%, Description: {description}'
    #print (message)
    return message

# Loop to send periodic updates
while True:
    # Fetch live weather data
    weather_data = fetch_weather_data()

    # Send message to Kafka topic
    producer.send(kafka_topic, value=weather_data)
    print(f'Sent: {weather_data}')

    # Wait for a specified interval (e.g., 5 minutes)
    time.sleep(30)  # 300 seconds = 5 minutes

#Close Kafka producer
producer.close()
