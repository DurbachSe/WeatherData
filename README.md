Project to display OpenWeather Data. This is an educational project and does not represent a "best practice".

Setup:

1. Install python:
     https://www.python.org/

2. Create a virtual environment (optional):
     python -m venv venv      # Create a virtual environment named "env" at the current location
     source venv/bin/activate  # Activates the created virtual environment | On Windows, use `venv\Scripts\activate`

3. Install all dependencies listed in the requirements file via pip:
     pip3 install -r requirements.txt

4. Setup Docker:
     https://docs.docker.com/engine/install/
   
5. Install Kubernetes usingMinikube:
     https://kubernetes.io/docs/tasks/tools/install-kubectl-macos/
     https://kubernetes.io/de/docs/tasks/tools/install-minikube/ (DE)

6. Make a free account and get an API-KEY at OpenWeather
     https://openweathermap.org/

7. Replace the key in line 5 in weather_processor.py with your API-KEY:
     api_key = 'YOUR_API_KEY'
     api_endpoint = 'http://api.openweathermap.org/data/2.5/weather'

8. Install Kafka:
   https://kafka.apache.org/downloads
   https://www.conduktor.io/kafka/how-to-install-apache-kafka-on-mac-with-homebrew/ (Mac OS)
