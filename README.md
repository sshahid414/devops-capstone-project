# Customer Accounts Microservice

[![Build Status](https://github.com/sshahid414/devops-capstone-project/actions/workflows/ci-build.yaml/badge.svg)](https://github.com/sshahid414/devops-capstone-project/actions)
[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Python](https://img.shields.io/badge/Python-3.9-blue.svg)](https://www.python.org/)

> DevOps Capstone Project — a RESTful **Customer Accounts** microservice built
> with Flask, tested with `nosetests`, secured with Flask-Talisman & CORS,
> containerized with Docker, and deployed to Kubernetes with a Tekton CD pipeline.

## Project Name: Customer Accounts Microservice

This microservice manages the lifecycle of customer **Accounts**. It exposes a
REST API supporting full CRUD operations (Create, Read, Update, Delete, List).

> **NOTE:** Replace `YOUR_GITHUB_USERNAME` in the build badge URL above with your
> actual GitHub username (and the repo name if different) so the badge renders
> your real build status.

## REST API

| Method   | URL                       | Operation                       |
| -------- | ------------------------- | ------------------------------- |
| `POST`   | `/accounts`               | Create a new account            |
| `GET`    | `/accounts`               | List all accounts               |
| `GET`    | `/accounts/{id}`          | Read an account                 |
| `PUT`    | `/accounts/{id}`          | Update an account               |
| `DELETE` | `/accounts/{id}`          | Delete an account               |
| `GET`    | `/health`                 | Health check                    |
| `GET`    | `/`                       | Service metadata (root)         |

## Account Model

| Field          | Type    | Description                |
| -------------- | ------- | -------------------------- |
| `id`           | Integer | Primary key                |
| `name`         | String  | Customer name              |
| `email`        | String  | Customer email             |
| `address`      | String  | Customer address           |
| `phone_number` | String  | Customer phone (optional)  |
| `date_joined`  | Date    | Date the account was added |

## Running locally (with Docker — recommended)

This project targets **Python 3.9** (matching the course environment). The
quickest way to run it on any machine is via Docker.

```bash
# Build the dev image
docker build -t accounts-dev -f Dockerfile.dev .

# Run the unit tests with nosetests
docker run --rm accounts-dev nosetests

# Run the service on http://localhost:8080
docker run --rm -p 8080:8080 accounts-dev \
    gunicorn --bind=0.0.0.0:8080 service:app
```

## Running locally (with Python 3.9 installed)

```bash
python -m venv venv
source venv/bin/activate        # On Windows: venv\Scripts\activate
pip install -r requirements.txt
nosetests                       # run the test suite
honcho start                    # run the service (uses the Procfile)
```

## Test coverage

```bash
nosetests
coverage report -m
```

## License

Licensed under the Apache License, Version 2.0.
