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

7. Install Kafka (and Zookeeper):
   https://kafka.apache.org/downloads
   https://www.conduktor.io/kafka/how-to-install-apache-kafka-on-mac-with-homebrew/ (Mac OS)
   
8. Start local Kafka
   Start Zookeeper: /usr/local/bin/zookeeper-server-start /usr/local/etc/zookeeper/zoo.cfg
   Start Kafka: /usr/local/bin/kafka-server-start /usr/local/etc/kafka/server.properties
   Create topic: /zsr/local/bin/kafka-topics --create --topic weather-data --bootstrap-server localhost:9092 --partitions 1 --replication-factor 1

   Optionally you can start kafka via a bash script as provided with start_kafka.sh. You can change all paths and parameters as needed for your setup.
   You may need to give the script permissions to run, as for example with (Mac OS):
   chmod +x start_kafka.sh
   xattr -d com.apple.quarantine start_kafka.sh

   To run the script simply use following command:
   ./start_kafka.sh   

9. Get your Weather data API-Key (https://home.openweathermap.org/api_keys):
   create in the same folder a secret.py including your API-Key. The content looks like this: OPENWEATHERMAP_API_KEY="PasteYourKey"

