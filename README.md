# Downloading language data from OSCAR automated

[![Lint & Build Package](https://github.com/xamm/download_oscar/actions/workflows/lint_build.yml/badge.svg)](https://github.com/xamm/download_oscar/actions/workflows/lint_build.yml)
[![Deploy Python Package](https://github.com/xamm/download_oscar/actions/workflows/lint_build_deploy.yml/badge.svg?branch=main)](https://github.com/xamm/download_oscar/actions/workflows/lint_build_deploy.yml)
[![PyPI](https://img.shields.io/pypi/v/download-oscar?color=blue)](https://pypi.org/project/download-oscar/)
[![PyPI - License](https://img.shields.io/pypi/l/download-oscar?color=brightgreen)](https://github.com/xamm/download_oscar/blob/f0caf517f9846235696a5590fcf5c758bcac0a1a/LICENSE)
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

### Simple Installation

```pip install download-oscar``` will install the requirements and the tool with one command.

### Installing from source

#### Requirements

- Requires [Python](https://www.python.org/) in version 3.
- Requires [Requests](https://docs.python-requests.org/en/master/)
- Requires [html5lib](https://github.com/html5lib/html5lib-python)
- Requires [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)
- Requires [PySimpleGUI](https://github.com/PySimpleGUI/PySimpleGUI)
- Requires [tqdm](https://github.com/tqdm/tqdm)

#### Building

- install [Python](https://www.python.org/)
- `git clone https://github.com/xamm/download_oscar.git`
- `cd download_oscar`
- (optional) create a virtual enironment
- `pip install -r requirements.txt`
- `pip install -e .` will install the tool in development mode.

## Release a new version

- All pushed git commits and pull requests on the `main` branch trigger an automatic build and packaging for pypi
    - commits without a tag only trigger packaging for [**TestPyPi**](https://test.pypi.org/)
    - commits with a tag will also push to [**PyPi**](https://pypi.org/)
    - A new version number must be specified in `setup.py` in order for publishing to work
        - publishing is trigerred on creation of a `tag` on the `main` branch
        - e.g. `git tag -a v0.0.1 -m 'Release 0.1' and `git push origin v0.0.1`
        - easiest procedure:
            - work on your code
            - add & commit changes
            - push changes
            - create tag
            - push tag

## [Licence](https://github.com/xamm/download_oscar/blob/main/LICENSE)
