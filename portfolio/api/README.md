# API Services

**Project Title:** Django REST Framework Backend API Suite
**Description:** This project implements a set of robust, high-performance APIs using Django REST Framework, designed to handle complex business logic and facilitate seamless data exchange between services.

## Overview
This service provides a structured, scalable backend layer for the entire portfolio. It utilizes Django's ORM and DRF's serialization capabilities to manage data models and expose them via secure, RESTful endpoints.

## Tech Stack
* Django
* Django REST Framework (DRF)
* PostgreSQL (via psycopg2)
* Python 3.x

## Architecture Decisions
The architecture follows a standard Django pattern, separating concerns into `config` (settings/URLs), `apps/core` (business logic/models), and `tests`. Configuration is entirely driven by environment variables for security and portability.

## How To Run
1. **Setup Environment:** Create a virtual environment and install dependencies (`pip install -r requirements.txt`).
2. **Database:** Set up PostgreSQL credentials in the environment.
3. **Migrations:** Run migrations: `python manage.py makemigrations` followed by `python manage.py migrate`.
4. **Run Server:** Start the development server: `python manage.py runserver`.

## Test Coverage
Testing is implemented using Django's built-in testing framework, ensuring comprehensive coverage for models, serializers, and view logic.
