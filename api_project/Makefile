# Django REST Framework API Project Makefile
# ALX Django REST Framework Tasks

# Python path for virtual environment
PYTHON = /Users/Wills/Desktop/ALX/Alx_DjangoLearnLab/.venv/bin/python

# Start development server
server:
	$(PYTHON) manage.py runserver

# Run migrations
migrate:
	$(PYTHON) manage.py makemigrations
	$(PYTHON) manage.py migrate

# Create superuser
super:
	$(PYTHON) manage.py createsuperuser

# Populate database with sample data
populate:
	$(PYTHON) manage.py shell -c "exec(open('api/pop.py').read())"

# Run Django checks
check:
	$(PYTHON) manage.py check

# Test API endpoints
test:
	$(PYTHON) test_api.py

# Clean database and start fresh
clean:
	rm -f db.sqlite3
	rm -rf api/migrations/000*.py
	$(PYTHON) manage.py makemigrations
	$(PYTHON) manage.py migrate
	$(PYTHON) manage.py shell -c "exec(open('api/pop.py').read())"

# Install requirements
install:
	pip install django djangorestframework requests

# Show all available commands
help:
	@echo "Available commands:"
	@echo "  make server     - Start Django development server"
	@echo "  make migrate    - Run database migrations"
	@echo "  make super      - Create superuser"
	@echo "  make populate   - Add sample data to database"
	@echo "  make check      - Run Django system checks"
	@echo "  make test       - Test API endpoints"
	@echo "  make clean      - Clean database and start fresh"
	@echo "  make install    - Install required packages"
	@echo "  make help       - Show this help message"

.PHONY: server migrate super populate check test clean install help

shell:
	python manage.py shell