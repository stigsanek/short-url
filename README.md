# Short URL

![GitHub Workflow Status](https://img.shields.io/github/actions/workflow/status/stigsanek/short-url/pyci.yml?branch=main)
![Code Climate maintainability](https://img.shields.io/codeclimate/maintainability/stigsanek/short-url)
![Code Climate coverage](https://img.shields.io/codeclimate/coverage/stigsanek/short-url)

## Description

"Short URL" is API service for URL shortening. Service work by transforming any long URL into a shorter, more readable link. When a user clicks the shortened version, they’re automatically forwarded to the destination URL. Think of a short URL as a more descriptive and memorable nickname for your long webpage address.

## Usage

You can deploy the project locally or via Docker.

### 1. Locally

#### Python

Before installing the package, you need to make sure that you have Python version 3.8 or higher installed.

```bash
>> python --version
Python 3.8.0+
```

If you don't have Python installed, you can download and install it
from [the official Python website](https://www.python.org/downloads/).

#### Poetry

The project uses the Poetry manager. Poetry is a tool for dependency management and packaging in Python. It allows you
to declare the libraries your project depends on and it will manage (install/update) them for you. You can read more
about this tool on [the official Poetry website](https://python-poetry.org/)

#### Dependencies

To work with the package, you need to clone the repository to your computer. This is done using the `git clone` command.
Clone the project on the command line:

```bash
# clone via HTTPS:
>> git clone https://github.com/stigsanek/short-url.git
# clone via SSH:
>> git@github.com:stigsanek/short-url.git
```

It remains to move to the directory and install the dependencies:

```bash
>> cd short-url
>> poetry install --no-root
```

#### Environment

For the application to work, you need to create a file `.env` in the root of the project:

```
SECRET_KEY="your_key"
DATABASE_URL=sqlite:///db.sqlite3
ALLOWED_HOSTS=127.0.0.1,localhost

# If you want to enable debug mode
DEBUG=True
```

#### Run

* Run database migrations:

```bash
>> python manage.py migrate

 ...
 ...
 ...
 Applying links.0001_initial... OK
```

* Run application:

```bash
>> python manage.py runserver

Watching for file changes with StatReloader
Performing system checks...

System check identified no issues (0 silenced).
December 26, 2022 - 11:45:42
Django version 4.1.4, using settings 'short_url.settings'
Starting development server at http://127.0.0.1:8000/    
Quit the server with CTRL-BREAK.
```

* Open [http://127.0.0.1:8000](http://127.0.0.1:8000) in your browser.

### 2. Docker

Docker is a platform designed to help developers build, share, and run modern applications.
You can read more about this tool on [the official Docker website](https://www.docker.com/).
You need to [install Docker Desktop](https://www.docker.com/products/docker-desktop/).
Docker Desktop is an application for the building and sharing of containerized applications and microservices.

#### Environment

Depending on the application mode, different environment files are used.
For development mode, the `.env.dev` file with basic settings has already been created.
For production mode, you need to create an `.env.prod` file:

```
# Database environment
POSTGRES_DB=short_url
POSTGRES_USER=user
POSTGRES_PASSWORD=password
POSTGRES_HOST=db
POSTGRES_PORT=5432

# App environment
SECRET_KEY=prod
ALLOWED_HOSTS=127.0.0.1
DATABASE_URL=postgres://${POSTGRES_USER}:${POSTGRES_PASSWORD}@${POSTGRES_HOST}:${POSTGRES_PORT}/${POSTGRES_DB}
```

#### Run development mode

```bash
>> docker-compose -f compose.dev.yml up -d

 ...
 ...
 ...
 Creating short-url_db_1 ... done
 Creating short-url_web_1 ... done
```

Open [http://127.0.0.1:8000](http://127.0.0.1:8000) in your browser.

#### Run production mode

```bash
>> docker-compose -f compose.prod.yml up -d

 ...
 ...
 ...
 Creating short-url_db_1 ... done
 Creating short-url_web_1 ... done
```

Open [http://127.0.0.1:8000](http://127.0.0.1:8000) in your browser.
