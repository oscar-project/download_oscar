# Downloading language data from OSCAR automated

![Lint & Build](https://github.com/xamm/download_oscar/actions/workflows/lint_build.yml)
![PyPI](https://img.shields.io/pypi/v/download-oscar?color=blue)
![PyPI - License](https://img.shields.io/pypi/l/download-oscar?color=brightgreen)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/download-oscar?color=informational)


## Features

- Adds dodc and dodg as command line tools
- `dodc`: command line variant provided with arguments to download data
- `dodg`: gui variant to download data, put arguments into input fields

## Usage

### `dodc`

To get help with the command line tool use `dodc -h` from a shell.

The command line tool needs to be supplied with multiple arguments:
- **user**: The user used to login to the site providing OSCAR.
- **password**: The password used to login to the site providing OSCAR.
- **base_url**: The url where the language iles are hosted.
- **out**: The folder where files should be downloaded to.
- **chunk_size** *(optional)*: Defaults to 4096. The size of the chunks files are downloaded in.

### `dodg`

The gui tool internally calls the command line tool `dodc`.
Instead of providing arguments to the command line you can enter these into input fields directly and they will be passed downward to the command line tool.

## Installation

- Requires [Python](https://www.python.org/) in version 3.
- Requires [Requests](https://docs.python-requests.org/en/master/)
- Requires [html5lib](https://github.com/html5lib/html5lib-python)
- Requires [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)
- Requires [PySimpleGUI](https://github.com/PySimpleGUI/PySimpleGUI)
- Requires [tqdm](https://github.com/tqdm/tqdm)

#### Building from source

- install [Python](https://www.python.org/)
- `git clone https://github.com/xamm/download_oscar.git`
- `cd download_oscar`
- (optional) create a virtual enironment
- `pip install -r requirements.txt`
- `python setup.py sdist`

#### Release new version

- All pushed git commits and pull requests on the `main` branch trigger an automatic build and packaging for pypi
    - commits without a tag only trigger packaging for [**TestPyPi**](https://test.pypi.org/)
    - commits with a tag will also push to [**PyPi**](https://pypi.org/)
    - A new version number must be specified in `setup.py` in order for publishing to work
        - e.g. `git tag v0.0.1`

## [Licence](https://github.com/xamm/download_oscar/blob/main/LICENSE)
