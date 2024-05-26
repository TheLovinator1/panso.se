# Panso.se

This Django-based web application allows users to compare prices of various products from different vendors in the Swedish market. The goal is to help consumers find the best deals and make informed purchasing decisions.

## Features

- **Product Search**: Users can search for products using keywords.
- **Price Comparison**: Displays prices from multiple vendors for each product.
- **Product Details**: Shows detailed information about each product, including specifications and reviews.
- **User Accounts**: Allows users to create accounts, log in, and save their favorite products.
- **Admin Interface**: An admin interface for managing products, vendors, and user accounts.

## Requirements

- Latest version of [Python](https://www.python.org/downloads/)
- [Garnet](https://github.com/microsoft/garnet) (Or other Redis alternative)
- [Docker](https://www.docker.com/get-started)

If you have Docker you can start Garnet with `docker-compose up garnet` otherwise download the [executable](https://github.com/microsoft/garnet/releases).

## Installation

1. Clone the repository:

```bash
git clone https://github.com/TheLovinator1/panso.se.git
cd panso.se
```

2. Create a virtual environment and install dependencies:

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

3. Rename the `.env.example` file to `.env` and update the environment variables:

```bash
mv .env.example .env
```

4. Run the Django migrations:

```bash
python manage.py migrate
```

5. Create a superuser account:

```bash
python manage.py createsuperuser
```

6. Start the development server:

```bash
python manage.py runserver
```

7. Open the browser and go to `http://localhost:8000/` to access the application.

## Usage

### Populating the database

[Celery](https://docs.celeryproject.org/en/stable/) is used to periodically fetch product data from various vendors and update the database. To start the Celery worker, run the following command:

```bash
celery -A panso worker --loglevel=info
```

To schedule periodic tasks, start the Celery beat:

```bash
celery -A panso beat --loglevel=info
```

### Admin Interface

To access the admin interface, go to `http://localhost:8000/admin/` and log in with the superuser account created earlier.


### Running Tests

To run the tests, use the following command:

```bash
# Remember to start the Garnet server before running the tests
pytest -v -n 8
```

## Contributing

Any contributions you make are **greatly appreciated**. If you have any suggestions, bug reports, or pull requests, please open an issue or create a pull request.

Two notes before contributing:
- If this is a major change, please open an issue or contact me first to double-check if the change is appropriate.
- Don't be afraid to make a pull request even if you are new to open-source. I am happy to help you through the process.

### Steps to Contribute

- Click the "Fork" button at the top-right corner of the repository.
- You can find the repository URL by clicking the green "Code" button.
- Create a new branch with a descriptive name to work on a feature or bug fix.
  - For example, if you want to turn the logo upside down, you would do the following:
  - `git checkout -b flip-logo`
    - You can name the branch whatever you want, it won't affect anything.
- Test your changes locally by running the following commands:
  - `python manage.py test`
    - This command will run the tests to ensure that your changes don't break any existing functionality.
    - I can help you with writing tests if you are not familiar with it.
  - `pre-commit run --all-files`
    - This command will run the pre-commit checks to ensure that the code is formatted correctly and passes all linting checks.
    - You can install the pre-commit hooks by running `pre-commit install` if you don't want to run the checks manually.
  - Fix any issues that arise from the tests or pre-commit checks.
- After making the necessary changes, commit your changes.
  -  Add all changes
     - `git add .`
   - Write a commit message describing the changes
     - `git commit -m "Add new feature"`
   - Push the changes to your fork
     - `git push origin feature/new-feature`
- Go to your fork on GitHub and click the "New Pull Request" button. Fill in the details and submit the pull request.
- After submitting the pull request, it will be reviewed and once approved, it will be merged into the main branch.

## Contact

You can contact me at the following places:
- Email: [mailto:tlovinator@gmail.com](tlovinator@gmail.com)
- Discord: TheLovinator#9276
- Open an issue in the repository
