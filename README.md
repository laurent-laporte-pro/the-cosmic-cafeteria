# The Cosmic Cafeteria

> 🛸 A fun microservice-based web app where hungry heroes order interstellar meals, powered by Flask, PostgreSQL, Redis
> queues, and Docker. Includes allergy checks, logs, tests, and cosmic flavor.

## Table of Contents

- [Instructions](docs/index.md) ← Read that first
- [Prerequisites](#prerequisites)
- [Getting Started](#getting-started)
- [Project Structure](#project-structure)
- [Development](#development)
- [Testing](#testing)
- [Docker Setup](#docker-setup)
- [Contributing](#contributing)

## Prerequisites

Before getting started, make sure you have the following installed on your machine:

- [Python 3.12](https://www.python.org/downloads/) or higher
- [Docker](https://www.docker.com/get-started) and [Docker Compose](https://docs.docker.com/compose/install/)
- [Docker Desktop](https://www.docker.com/products/docker-desktop) (Windows or Mac)
- [Git](https://git-scm.com/downloads) and a GitHub account for the final PR

## Getting Started

The project uses [hatch](https://hatch.pypa.io/latest/) for dependency management and virtual environment.
Check the [Hatch Installation](https://hatch.pypa.io/latest/install/) page to install it.

```shell
hatch env create
```

Alternatively, you can use [uv](https://docs.astral.sh/uv/) for development and dependency management.

```shell
uv sync
```

If you're allergic to `hatch` and `uv`, proceed traditionally as follows:

```shell
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -e .
```

## Project Structure

```
the-cosmic-cafeteria/
├── docs/                   # Documentation files
├── src/                    # Source code
│   ├── api/                # Flask API components
│   │   ├── __init__.py
│   │   ├── models/         # SQLAlchemy models
│   │   ├── routes/         # API endpoints
│   │   └── schemas/        # Data validation schemas
│   ├── cli/                # Command Line Interface (client API)
│   │   └── __init__.py
│   └── worker/             # RQ worker implementation
│       ├── __init__.py
│       └── tasks.py        # Async task definitions
├── tests/                  # Pytest test suites
├── docker/                 # Docker configuration files
└── docker-compose.yml      # Service orchestration
```

## Development

Start the development environment with Docker:

```shell
docker-compose up -d
```

The API will be available at http://localhost:5000

## Testing

Run the test suite:

```shell
hatch test
```

## Docker Setup

The application consists of four containers:

- Flask API
- RQ Worker
- PostgreSQL database
- Redis queue

To build and start all services:

```shell
docker-compose up --build
```

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request
