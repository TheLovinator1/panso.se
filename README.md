# panso.se

## Development

Pull requests are welcome. For major changes, please [open an issue](https://github.com/TheLovinator1/panso.se/issues) first to discuss what you would like to change.

### Prerequisites

- [Latest Python](https://www.python.org/)
  - Add to PATH during installation.
- [Poetry](https://python-poetry.org/)
  - Linux, macOS, Windows (WSL): `curl -sSL https://install.python-poetry.org | python3 -`
    - Add `$HOME/.local/bin` to your PATH if it's not already there.
    - `echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc`
  - Windows (Powershell): `(Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing).Content | py -`
    - If you have installed Python through the Microsoft Store, replace py with python in the command above.
    - Add `$HOME\AppData\Roaming\Python\Scripts` to your PATH if it's not already there.
    - Settings -> System -> About -> Advanced system settings -> Environment Variables -> User variables -> Path -> Edit -> New -> `$HOME\AppData\Roaming\Python\Python312\Scripts`

### Installation

Download the repository and install the dependencies.

```bash
git clone git@github.com:TheLovinator1/panso.se.git
cd panso.se
poetry install
poetry shell
python manage.py migrate
python manage.py runserver
```

Database is saved to `%APPDATA%/TheLovinator/Panso/panso.sqlite3` on Windows and `$HOME/.local/share/TheLovinator/Panso/panso.sqlite3` on Linux and macOS.

### Django information

Django uses `apps` to separate different parts of the website. Each app has its own `urls.py` and `views.py`. The main `urls.py` is in the `config` folder.

We have the following apps:

- `config` - Main configuration for the website. This has settings for the entire website.
- `panso` - Everything related to the root of the website. For example, the index page.
- `webhallen` - Everything related to [Webhallen](https://www.webhallen.com/).

If you want to add a new app, you can use the following command and add it to the `INSTALLED_APPS` list in `config/settings.py`.

```bash
python manage.py startapp app_name
```

### Purpose of key files

- `app_name/models.py` - This file contains model definitions for the app. Models are Python classes that map to database tables.
- `app_name/migrations` - Auto-generated files created when you run `python manage.py makemigrations`. They contain database schema changes.
- `app_name/urls.py` - The URL patterns for the app are declared here. This file connects URLs to the views.
- `app_name/views.py` - This is where you define the logic that will be executed when a request is made to a specific route.
- `templates` - Contains the HTML files.
- `static` - Contains the CSS, JavaScript, and images.

### Running tests

```bash
pytest
```
