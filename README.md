# panso.se

This is the source code for [panso.se](https://panso.se/), a price comparison website for computer hardware in Sweden.

## Contributing

Pull requests are welcome. For major changes, please [open an issue](https://github.com/TheLovinator1/panso.se/issues) first to discuss what you would like to change.

You don't have to think about style, formatting, or testing. Just write the code and I'll take care of the rest if needed.

- [Windows Setup](docs/windows.md)

## tl;dr

```bash
git clone git@github.com:TheLovinator1/panso.se.git
cd panso.se
cp .env.example .env
${VISUAL-${EDITOR-nano}} .env
poetry install
poetry shell
python manage.py migrate
python manage.py runserver
pytest
```

## Django information

Django uses `apps` to separate different parts of the website. Each app has its own `urls.py` and `views.py`. The main `urls.py` is in the `config` folder.

We have the following apps:

- `config` - Main configuration for the website. This has settings for the entire website.
- `panso` - Everything related to the root of the website. For example, the index page.
- `webhallen` - Everything related to [Webhallen](https://www.webhallen.com/).

If you want to add a new app, you can run `python manage.py startapp app_name` and add it to the `INSTALLED_APPS` list in `config/settings.py`.

## Purpose of key files

- `app_name/models.py` - Contains model definitions. Models are Python classes that map to database tables.
- `app_name/migrations` - Auto-generated files created when you run `python manage.py makemigrations`. They contain database schema changes.
- `app_name/urls.py` - Declares URL patterns, connecting routes to views.
- `app_name/views.py` - Defines the logic executed when a request is made to a specific route.
- `templates` - Contains HTML files.
- `static` - Stores CSS, JavaScript, and image assets.

## Commands

### User management

- `python manage.py changepassword <username>`
  - Change a user's password for the specified username.
- `python manage.py createsuperuser`
  - Create a superuser.

### Database management

- `python manage.py dumpdata --output=data.json`
  - Dump the database contents to a JSON file.
- `python manage.py loaddata data.json`
  - Load data from a JSON file into the database.
- `python manage.py makemigrations`
  - Create new migrations based on changes to models.
- `python manage.py migrate`
  - Synchronize the database state with current models and migrations.

### Development

- `python manage.py startapp app_name`
  - Create a new Django app.
- `python manage.py collectstatic`
  - Collect static files into the STATIC_ROOT directory.
- `python manage.py runserver`
  - Start the development server.

### Webhallen

- `python manage.py webhallen_aggregate_json_keys`
  - Aggregate all keys from JSON data in the database into a single JSON file, with one example value per key.
- `python manage.py webhallen_fetch_json`
  - Fetch the sitemap from Webhallen, parse it, and use the URLs to retrieve product JSON data.
- `python manage.py webhallen_populate`
  - Populate models with the JSON data stored in the database.
- `python manage.py webhallen_save_json_to_disk`
  - Download all JSON data from the database and save it to disk.
