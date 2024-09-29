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
