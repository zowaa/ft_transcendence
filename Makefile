all:
	sudo docker-compose up --build

detach:
	sudo docker-compose up --build -d

start:
	sudo docker-compose start

stop:
	sudo docker-compose stop

down:
	sudo docker-compose down