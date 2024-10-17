# Windows Setup Guide

This document provides detailed instructions for installing and running the panso.se project on a Windows machine.

## Prerequisites

Ensure the following tools are installed before proceeding with the setup.

### 1. [Python](https://www.python.org/downloads/)

- Download and install the latest version of Python.
- During installation, **check the box** that says “Add Python to PATH.”

### 2. [Poetry](https://python-poetry.org/)

- Poetry is the tool used for dependency management in this project.
- Open **Powershell** and run the following command to install Poetry:
  - If you installed Python through the Microsoft Store, replace `python3` with `python` in the command below.

```bash
(Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing).Content | py -
```

- Add Poetry to your system’s `PATH`:
  1. Open **Settings** -> **System** -> **About** -> **Advanced System Settings** -> **Environment Variables**.
  2. Under **User variables**, locate **Path** and click **Edit**.
  3. Click **New** and add:
        `C:\Users\lovinator\AppData\Roaming\Python\Python312\Scripts`   # Replace `lovinator` with your username and `Python312` with your Python version.

### 3. [PostgreSQL](https://www.postgresql.org/download/)

- Download and install the latest version of PostgreSQL.
  - If you have Docker installed, you can run PostgreSQL in a container using the following command:

    ```bash
    docker run --name panso-postgres -e POSTGRES_PASSWORD=Secret -e POSTGRES_DB=panso -e POSTGRES_USER=panso -p 5432:5432 -d postgres
    ```

### 4. [git](https://git-scm.com/downloads) or [GitHub Desktop](https://desktop.github.com/)

- Download and install git or GitHub Desktop to clone the repository. If you are an beginner, GitHub Desktop is highly recommended.
- If you are installing git, you probably want to uncheck the box that says “Windows Explorer integration” during installation.

## Project Setup

Follow these steps to clone the project and run it on your machine.

### 0. Clone the Repository

Open **Powershell**, navigate to the folder where you want to store the project, and run:

```bash
git clone https://github.com/TheLovinator1/panso.se.git
cd panso.se
```

### 1. Modify Environment Variables

Copy the `.env.example` file to `.env`:

```bash
cp .env.example .env
```

Open the `.env` file and set the required variables:

- `DJANGO_SECRET_KEY`: Generate a new secret key using the command below:

```bash
python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'
```

- `POSTGRES_PASSWORD`: Set the password you used when setting up PostgreSQL.
- `POSTGRES_USER`: Set the username you used when setting up PostgreSQL.
- `POSTGRES_DB`: Set the database name you used when setting up PostgreSQL.
- `POSTGRES_HOST`: Set the host to `localhost` if you are using a local PostgreSQL instance.

### 2. Install Dependencies

Use Poetry to install the project dependencies:

`poetry install`

### 3. Activate Virtual Environment

Activate the virtual environment created by Poetry:

`poetry shell`

### 4. Set Up the Database

Run the following command to apply migrations and set up the database:

`python manage.py migrate`

### 5. Run the Development Server

Now, you can run the development server:

`python manage.py runserver`

### 6. Running Tests

To ensure everything is working correctly, run the tests:

`pytest`

### 7. Access the Application

Open your browser and navigate to `http://localhost:8000/` to access the application.

---

By following these steps, you should have the panso.se project up and running on your Windows machine. If you encounter any issues, feel free to reach out for help.
