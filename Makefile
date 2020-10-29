
DEPLOY_ENV ?= staging

setup:
	python3 -m venv venv

run:
	source venv/bin/activate &&\
		source $(DEPLOY_ENV)_env.sh &&\
		python restore_cloudsql_backup.py

all: setup run
