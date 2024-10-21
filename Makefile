DC = docker compose
ALEMBIC_INI_PATH = access_service/src/access_service/infrastructure/persistence/alembic/alembic.ini
APP_FILE = docker_compose/access_service.yaml
STORAGE_FILE = docker_compose/storage.yaml
LOGS = docker logs
DB_CONTANER = access_service_postgres
APP_CONTAINER = access_service
EXEC = docker exec -it

.PHONY: app
app:
	${DC} -f ${APP_FILE} up --build -d

.PHONY: storage
storage:
	${DC} -f ${STORAGE_FILE} ${ENV} up --build 

.PHONY: app-down
app-down:
	${DC} -f ${APP_FILE} down

.PHONY: storage-down
storage-down:
	${DC} -f ${STORAGE_FILE} down

.PHONY: app-logs
app-logs:
	${LOGS} ${APP_CONTAINER} -f

.PHONY: db-logs
db-logs:
	${LOGS} ${DB_CONTAINER} -f

.PHONY: migrate
migrate:
	${EXEC} ${APP_CONTAINER} poetry run alembic -c ${ALEMBIC_INI_PATH} upgrade head

.PHONY: revision
revision:
	${EXEC} ${APP_CONTAINER} poetry run alembic -c ${ALEMBIC_INI_PATH} revision --autogenerate -m "${message}"