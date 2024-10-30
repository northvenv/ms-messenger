DC = docker compose
LOGS = docker logs
EXEC = docker exec -it


# ACCESS SERVICE (AS, as)
AS_FILE = docker_compose/access_service.yaml
AS_ALEMBIC_INI_FILE = src/access_service/infrastructure/persistence/alembic/alembic.ini
AS_CONTAINER = access_service
AS_ENV = access_service/.env.access_service

.PHONY: as
as:
	${DC} -f ${AS_FILE} up --build -d

.PHONY: as-down
as-down:
	${DC} -f ${AS_FILE} down

.PHONY: as-logs
as-logs:
	${LOGS} ${AS_CONTAINER} -f

.PHONY: as-migrate
as-migrate:
	${EXEC} ${AS_CONTAINER} poetry run alembic -c ${AS_ALEMBIC_INI_FILE} upgrade head

.PHONY: as-revision
as-revision:
	${EXEC} ${AS_CONTAINER} poetry run alembic -c ${AS_ALEMBIC_INI_FILE} revision --autogenerate -m "${message}"


#NOTIFICATION SERVICE (NS, ns)



#INFRASTRUCTURE
ENV = ./.env
REDIS_FILE = docker_compose/redis.yaml
POSTGRES_FILE = docker_compose/postgres.yaml
KAFKA_FILE = docker_compose/kafka.yaml

POSTGRES_CONTAINER = messenger_postgres
REDIS_CONTAINER = messenger_redis
KAFKA_CONTAINER = messenger_kafka


.PHONY: postgres
postgres:
	${DC} -f ${POSTGRES_FILE} --env-file ${ENV} up --build -d

.PHONY: redis
redis:
	${DC} -f ${REDIS_FILE} --env-file ${ENV} up --build -d

.PHONY: kafka
kafka:
	${DC} -f ${KAFKA_FILE} --env-file ${ENV} up --build -d

.PHONY: postgres-down
postgres-down:
	${DC} -f ${POSTGRES_FILE} --env-file ${ENV} down

.PHONY: redis-down
redis-down:
	${DC} -f ${REDIS_FILE} --env-file ${ENV} down 

.PHONY: kafka-down
kafka-down:
	${DC} -f ${KAFKA_FILE} --env-file ${ENV} down 

.PHONY: postgres-logs
postgres-logs:
	${LOGS} ${POSTGRES_CONTAINER} -f

.PHONY: redis-logs
redis-logs:
	${LOGS} ${REDIS_CONTAINER} -f

.PHONY: kafka-logs
kafka-logs:
	${LOGS} ${KAFKA_CONTAINER} -f











