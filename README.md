# To Do

A simple To Do web application built in Python.

## Running the App

### Requirements

* Python 3
* PostgreSQL

### Setup

Clone the repository to your local machine.

Set up a Postgres database and user. Note the credentials for later.

Import the SQL DDL commands to set up the required database table:

```shell
psql -f todo/schema.sql your_db_name
```
Create a folder called `instance` in the root of the repository. Copy the `config.toml.example` file to the new `instance` folder. Update the copied file with the user credentials you noted above. Remove `.example` from the filename.

Activate a [`pipenv`](https://pipenv.pypa.io/en/latest/) environment and install dependencies in that environment:

```shell
pipenv shell
pipenv install
```

### Run

Run the app using [Gunicorn](https://gunicorn.org/):

```shell
gunicorn todo.app:app
```

Add the `--reload` flag during development to autoreload when the app's Python code changes.

```shell
gunicorn --reload todo.app:app
```

Note that autoreload doesn't work for Jinja2 templates. You'll need to restart Gunicorn.
