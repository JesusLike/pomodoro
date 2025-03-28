.DEFAULT_GOAL := help

HOST ?= 0.0.0.0
PORT ?= 8000

run-gunicorn: ## Run the application using uvicorn with provided arguments or defaults
	poetry run gunicorn app.main:app --worker-class uvicorn.workers.UvicornWorker -c gunicorn.conf.py

run-dev:
	poetry run fastapi dev ./src/main.py --host $(HOST) --port $(PORT)

migrate:
	alembic revision --autogenerate -m "$(MESSAGE)"

migrate-apply:
	alembic upgrade head

install: ## Install a dependency using poetry
	@echo "Installing dependency $(LIBRARY)"
	poetry add $(LIBRARY)

uninstall: ## Uninstall a dependency using poetry
	@echo "Uninstalling dependency $(LIBRARY)"
	poetry remove $(LIBRARY)

update:
	@echo "Updating dependency $(LIBRARY) to the last available version"
	poetry update $(LIBRARY)

migrate-create:
	alembic revision --autogenerate -m $(MIGRATION)

migrate-apply:
	alembic upgrade head

help: ## Show this help message
	@echo "Usage: make [command]"
	@echo ""
	@echo "Commands:"
	@grep -E '^[a-zA-Z0-9_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  %-20s %s\n", $$1, $$2}'