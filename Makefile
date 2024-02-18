DOCKER_COMPOSE = docker-compose

up:
	$(DOCKER_COMPOSE) up -d --build

down:
	$(DOCKER_COMPOSE) down

clean:
	$(DOCKER_COMPOSE) down -v --remove-orphans

re: down up

restart:
	$(DOCKER_COMPOSE) restart

exec:
	$(DOCKER_COMPOSE) exec <service_name> <command>

build:
	$(DOCKER_COMPOSE) build
