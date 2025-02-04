## Setup

* Create a virtual environment and install libraries

  ```
  python3 -m venv .venv
  source .venv/bin/activate
  pip install -r requirements.txt
  ```

* Create a `.env` file containing:
  ```
  POSTGRES_DB_NAME=<database name>
  POSTGRES_USERNAME=<username>
  POSTGRES_PASSWORD=<password>
  POSTGRES_HOST=<hostname>
  POSTGRES_PORT=5432
  ```

* To create the database tables run
  ```
  python3 CreateTables.py
  ```

* To drop the database tables run
  ```
  python3 DropTables.py
  ```