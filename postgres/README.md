# PostgreSQL with Docker Compose

## Introduction

This repository contains a `docker-compose.yml` file that sets up a PostgreSQL database with a volume for persistent storage.

## Usage

To start the PostgreSQL container, run:

```sh
docker-compose up -d
```

## Configuration

### Environment Variables

Create a `.env` file and add the following variables:

```env
POSTGRES_DB=your_database_name
POSTGRES_USER=your_username
POSTGRES_PASSWORD=your_secure_password
```

Replace `your_database_name`, `your_username`, and `your_secure_password` with your desired values.

### Connecting to PostgreSQL

After starting the container, you can connect to the PostgreSQL database using:

```sh
psql -h localhost -U $POSTGRES_USER -d $POSTGRES_DB
```

