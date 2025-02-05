# PostgreSQL with Docker Compose
## Introduction

This repository contains a `docker-compose.yml` file that sets up a PostgreSQL database with a volume for persistent storage.


## Requirements
* Docker
* Docker Compose

## Setup
* Create a virtual environment and install libraries

  ```
  python3 -m venv .venv
  source .venv/bin/activate
  pip install -r requirements.txt
  ```

* Create a `.env` file containing:
  ```
  POSTGRES_DB=<database name>
  POSTGRES_USERNAME=<username>
  POSTGRES_PASSWORD=<password>
  POSTGRES_HOST=<hostname>
  POSTGRES_PORT=5432
  ```

## Usage

To start the PostgreSQL container, run:

```sh
docker-compose up -d
```

## Configuration

### Environment Variables

Create a `.env` file and add the following variables:



### Connecting to PostgreSQL

After starting the container, you can connect to the PostgreSQL database using:

```sh
psql -h localhost -U $POSTGRES_USER -d $POSTGRES_DB

```


### Adding and Dropping Tables 
* To create the database tables run
  ```
  python3 CreateTables.py
  ```

* To drop the database tables run
  ```
  python3 DropTables.py
  ```