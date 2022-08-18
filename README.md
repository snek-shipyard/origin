<p align="center">
  <a href="https://snek.at" target="_blank" rel="noopener noreferrer">
    <img src="https://user-images.githubusercontent.com/26285351/115684229-7aa44400-a357-11eb-917b-8d80d6c3e5d1.png" alt="tuwien-club logo" height="150">
  </a>
</p>

<h3 align="center">tuwien-club - Compact Content Management System</h3>

<p align="center">
  This is the official CCMS projects of tuwien-club.
  <br>
  <br>
  <a href="https://github.com/tuwien-club/ccms/issues/new?template=bug_report.md">Report bug</a>
  ·
  <a href="https://github.com/tuwien-club/ccms/issues/new?template=feature_request.md">Request feature</a>
  ·
  <a href="https://www.overleaf.com/read/bcxwhwbhrmps">Documentation</a>
  <br>
  <br>
  <a href="https://www.codacy.com/gh/tuwien-club/ccms/dashboard?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=tuwien-club/ccms&amp;utm_campaign=Badge_Grade">
    <img src="https://app.codacy.com/project/badge/Grade/bb3d984d38704860ba7ad800d319b8c4" />
  </a>
</p>

## Table of contents

-   [Table of contents](#table-of-contents)
-   [Quick start](#quick-start)
-   [Setup with Docker](#setup-with-docker)
    -   [Dependencies](#dependencies)
    -   [Installation](#installation)
    -   [Debugging](#debugging)
-   [Setup with Python Virtual Environment](#setup-with-python-virtual-environment)
    -   [Dependencies](#dependencies-1)
    -   [Installation](#installation-1)
-   [Bugs and feature requests](#bugs-and-feature-requests)
-   [Contributing](#contributing)
-   [Versioning](#versioning)
-   [Creators](#creators)
-   [Thanks](#thanks)
-   [Copyright and license](#copyright-and-license)

## [](#quick-start)Quick start

Several quick start options are available:

-   [Docker](#setup-with-docker)
-   [Python Virtual Environment](#setup-with-python-virtual-environment)

## [](#setup-with-docker)Setup with Docker

### Dependencies

-   [Docker](https://docs.docker.com/engine/installation/)
-   [Docker Compose](https://docs.docker.com/compose/install/)

### Installation

Run the following commands:

```bash
git clone https://github.com/tuwien-club/ccms.git
cd Wagtail-Template
docker-compose up --build -d
docker-compose up
```

The demo site will now be accessible at <http://localhost:8000/>.

**Important:** This `docker-compose.yml` is configured for local testing only, and is _not_ intended for production use.

### Debugging

To tail the logs from the Docker containers in realtime, run:

```bash
docker-compose logs -f
```

## [](#setup-with-python-virtual-environment)Setup with Python Virtual Environment

You can start a Wagtail project from this template without setting up Docker and simply use a virtual environment,
which is the [recommended installation approach](https://docs.python.org/3/library/venv.html) for all Python projects itself.

### Dependencies

-   Python 3.5, 3.6 or 3.7

### Installation

With [PIP](https://github.com/pypa/pip) installed, run:

    git clone https://github.com/tuwien-club/ccms.git
    cd Wagtail-Template
    python --version
    python -m pip --version

Confirm that this is showing a compatible version of Python 3.x. If not, and you have multiple versions
of Python installed on your system, you may need to specify the appropriate version when creating the venv:

    python3 -m venv /path/to/new/virtual/environment

Once a virtual environment has been created, it can be “activated” using a script in the virtual environment’s
binary directory. The invocation of the script is platform-specific (<venv> must be replaced by the path of the
directory containing the virtual environment):

| Platform | Shell      | Command to activate virtual environment |
| :------- | :--------- | :-------------------------------------- |
| Posix    | bash/zsh   | \$ source <venv>/bin/activate      |
|          | fish       | \$ . <venv>/bin/activate.fish      |
|          | csh/tcsh   | \$ source <venv>/bin/activate.csh  |
| Windows  | cmd.exe    | C:> <venv>\\Scripts\\activate.bat       |
|          | PowerShell | PS C:> <venv>\\Scripts\\Activate.ps1    |

Now we're ready to set up the project itself:

    pip install -r requirements/base.txt

To set up your database and load initial data, run the following commands:

    ./manage.py migrate
    ./manage.py runserver
    
## [](#bug-and-feature-requests)Bugs and feature request

Have a bug or a feature request? Please first search for existing and closed issues. If your problem or idea is not
addressed yet, [please open a new issue](https://github.com/tuwien-club/ccms/issues/new/choose).

## [](#contributing)Contributing

![GitHub last commit](https://img.shields.io/github/last-commit/tuwien-club/ccms)
![GitHub issues](https://img.shields.io/github/issues-raw/tuwien-club/ccms)
![GitHub closed issues](https://img.shields.io/github/issues-closed-raw/tuwien-club/ccms?color=green)

Please read through our
[contributing guidelines](https://github.com/tuwien-club/ccms/blob/master/CONTRIBUTING.md). Included are
directions for opening issues, coding standards, and notes on development.

All code should conform to the [Code Guide](https://github.com/tuwien-club/tonic/blob/master/STYLE_GUIDE.md), maintained by
[tuwien-club](https://github.com/tuwien-club).

## [](#versioning)Versioning

For transparency into our release cycle and in striving to maintain backward compatibility, this repository is
maintained under [the Semantic Versioning guidelines](https://semver.org/). Sometimes we screw up, but we adhere to
those rules whenever possible.

## [](#creators)Creators

<table border="0">
    <tr>
        <td>
    	    <a href="https://github.com/kleberbaum">
    	        <img src="https://avatars.githubusercontent.com/kleberbaum?s=100" alt="Avatar kleberbaum">
          </a>
        </td>
    </tr>
    <tr>
        <td><a href="https://github.com/kleberbaum">Florian Kleber</a></td>
    </tr>
</table>

## [](#thanks)Thanks

We do not have any external contributors yet, but if you want your name to be here, feel free
to [contribute to our project](#contributing).

## [](#copyright-and-license)Copyright and license

![GitHub repository license](https://img.shields.io/badge/license-EUPL--1.2-blue)

SPDX-License-Identifier: (EUPL-1.2)
Copyright © 2021 tuwien-club
