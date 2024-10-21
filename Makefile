DC = docker compose
ALEMBIC_INI_FILE = src/access_service/infrastructure/persistence/alembic/alembic.ini
APP_FILE = docker_compose/access_service.yaml
STORAGE_FILE = docker_compose/storage.yaml
LOGS = docker logs
STORAGE_CONTANER = access_service_postgres
APP_CONTAINER = access_service
EXEC = docker exec -it
ENV = access_service/.env


.PHONY: app
app:
	${DC} -f ${APP_FILE} up --build -d

.PHONY: storage
storage:
	${DC} -f ${STORAGE_FILE} --env-file ${ENV} up --build -d

.PHONY: app-down
app-down:
	${DC} -f ${APP_FILE} down

.PHONY: storage-down
storage-down:
	${DC} -f ${STORAGE_FILE} down

.PHONY: app-logs
app-logs:
	${LOGS} ${APP_CONTAINER} -f

.PHONY: storage-logs
storage-logs:
	${LOGS} ${STORAGE_CONTANER} -f

.PHONY: migrate
migrate:
	${EXEC} ${APP_CONTAINER} poetry run alembic -c ${ALEMBIC_INI_FILE} upgrade head

.PHONY: revision
revision:
	${EXEC} ${APP_CONTAINER} poetry run alembic -c ${ALEMBIC_INI_FILE} revision --autogenerate -m "${message}"