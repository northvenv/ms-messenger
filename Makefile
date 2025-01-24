DC = docker-compose
LOGS = docker logs
EXEC = docker exec -it

#NGINX
NGINX_FILE = docker_compose/nginx.yaml
NGINX_CONTAINER = messenger_nginx

.PHONY: nginx
nginx:
	${DC} -f ${NGINX_FILE} up --build -d

.PHONY: nginx-down
nginx-down:
	${DC} -f ${NGINX_FILE} down

.PHONY: nginx-logs
nginx-logs:
	${LOGS} ${NGINX_CONTAINER} -f

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

NS_FILE = docker_compose/notification_service.yaml
NS_CONTAINER = notification_service

.PHONY: ns
ns:
	${DC} -f ${NS_FILE} up --build -d

.PHONY: ns-down
ns-down:
	${DC} -f ${NS_FILE} down

.PHONY: ns-logs
ns-logs:
	${LOGS} ${NS_CONTAINER} -f

#MESSAGE_SERVICE (MS, ms)
MS_FILE = docker_compose/message_service.yaml
MS_CONTAINER = message_service
WS_MS_CONTAINER = ws_message_service
MS_ENV = message_service/.env.message_service

.PHONY: ms
ms:
	${DC} -f ${MS_FILE} up --build -d

.PHONY: ms-down
ms-down:
	${DC} -f ${MS_FILE} down

.PHONY: ms-logs
ms-logs:
	${LOGS} ${MS_CONTAINER} -f

.PHONY: ws-ms-logs
ws-ms-logs:
	${LOGS} ${WS_MS_CONTAINER} -f


#INFRASTRUCTURE
ENV = ./.env
REDIS_FILE = docker_compose/redis.yaml
POSTGRES_FILE = docker_compose/postgres.yaml
KAFKA_FILE = docker_compose/kafka.yaml
MONGO_FILE = docker_compose/mongo.yaml

POSTGRES_CONTAINER = messenger_postgres
REDIS_CONTAINER = messenger_redis
KAFKA_CONTAINER = messenger_kafka
MONGO_CONTAINER = messenger_mongo


.PHONY: postgres
postgres:
	${DC} -f ${POSTGRES_FILE} --env-file ${ENV} up --build -d

.PHONY: redis
redis:
	${DC} -f ${REDIS_FILE} --env-file ${ENV} up --build -d

.PHONY: kafka
kafka:
	${DC} -f ${KAFKA_FILE} --env-file ${ENV} up --build -d

.PHONY: mongo
mongo:
	${DC} -f ${MONGO_FILE} --env-file ${ENV} up --build -d


.PHONY: postgres-down
postgres-down:
	${DC} -f ${POSTGRES_FILE} --env-file ${ENV} down

.PHONY: redis-down
redis-down:
	${DC} -f ${REDIS_FILE} --env-file ${ENV} down 

.PHONY: kafka-down
kafka-down:
	${DC} -f ${KAFKA_FILE} --env-file ${ENV} down

.PHONY: mongo-down
mongo-down:
	${DC} -f ${MONGO_FILE} --env-file ${ENV} down  


.PHONY: postgres-logs
postgres-logs:
	${LOGS} ${POSTGRES_CONTAINER} -f

.PHONY: redis-logs
redis-logs:
	${LOGS} ${REDIS_CONTAINER} -f

.PHONY: kafka-logs
kafka-logs:
	${LOGS} ${KAFKA_CONTAINER} -f

.PHONY: mongo-logs
mongo-logs:
	${LOGS} ${MONGO_CONTAINER} -f











