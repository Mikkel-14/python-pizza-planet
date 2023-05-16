.PHONY: setup-dev-environment
setup-dev-environment:
	pip install -r requirements.txt
	pre-commit install
	pre-commit install --hook-type commit-msg

.PHONY: setup-db
setup-db:
	python3 manage.py db init
	python3 manage.py db migrate
	python3 manage.py db upgrade

.PHONY: start
start: export FLASK_ENV=development
start:
	python3 manage.py run

.PHONY: test
test:
	python3 manage.py test

compute-coverage:
	pytest --cov=./app ./app/test