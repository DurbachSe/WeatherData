Project to display OpenWeather Data. This is an extension to the README in the main project folder, if you want to run the scripts as docker services.

Setup:

1. Do at least step 4 described in the main README. You can do the other steps to get started if needed.


2. Setup Docker:
	https://docs.docker.com/engine/install/

3. Build dockerfiles:
	docker build PoducerDockerfile.txt .
	docker build ConsumerDockerfile.txt .
	docker build KafkaDockerfile.txt .

4 Start all services with docker compose:
	docker compose up -d
