# panso.se

A price comparison site for the Swedish market. The site is built with Django.

## Dependencies

- [Python 3.12](https://www.python.org/)
- [Poetry](https://python-poetry.org/docs/#installation)

## tl;dr
```bash
poetry install
poetry shell
python manage.py migrate
python manage.py runserver
python manage.py test

# Optional
pre-commit install
pre-commit run --all-files

# Crawlers
scrapy crawl webhallen
```

## Environment Variables

- `SECRET_KEY` - A key used for cryptographic signing. Ensure this key is kept secret and not exposed to the public. In a production environment, generate a unique, unpredictable value.
- `DEBUG` - Determines whether your Django project is in debug mode. Setting this to true enables detailed error pages and other debug-specific features, useful during development. For production environments, this should be set to false to avoid exposing sensitive information. Accepts true or false (case insensitive).
- `EMAIL_HOST_USER` - Gmail address to send emails from.
- `EMAIL_HOST_PASSWORD` - [Gmail app password](https://support.google.com/mail/answer/185833?hl=en).

## Contributing

Feel free to contribute to the project. If you have any questions, please open an issue.

### Directory Structure

This project follows the [MVC (Model-View-Controller) pattern](https://en.wikipedia.org/wiki/Model%E2%80%93view%E2%80%93controller). ([But Controller -> View, and View -> Template](https://docs.djangoproject.com/en/5.0/faq/general/#django-appears-to-be-a-mvc-framework-but-you-call-the-controller-the-view-and-the-view-the-template-how-come-you-don-t-use-the-standard-names)).

The directory structure is as follows:

- `panso` - My Django app is in the same directory as the project.
- `panso/views` - Views for the project that handle requests and return responses.
- `panso/models` - The database models for the project.
    - You need to run `python manage.py makemigrations` and `python manage.py migrate` to apply changes to the database.
- `panso/urls.py` - The URL configuration for the project.
- `panso/settings.py` - The settings for the project.
- `panso/tests.py` - Tests using [Django Unit Test framework](https://docs.djangoproject.com/en/5.0/topics/testing/overview/).
- `templates` - The HTML templates for the project. `base.html` is the base template that other templates extend.
- `static` - The static files for the project (e.g., CSS, JavaScript, images).

## Data

- The main database is stored in /data/panso.sqlite3.
- Logs are stored in /data/{date}.log.

## Contact

If you have any questions, please open an issue.

I can also be reached at [hello@panso.se](mailto:hello@panso.se) or on Discord: `TheLovinator#9276`
