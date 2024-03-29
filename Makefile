all:
	docker-compose up --build

detach:
	docker-compose up --build -d

start:
	docker-compose start

stop:
	docker-compose stop

down:
	docker-compose down