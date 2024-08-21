****# Django REST Framework Recursive (Fork)

This repository is the friendly fork of the original [django-rest-framework-recursive](https://github.com/heywbj/django-rest-framework-recursive) by [heywbj](https://github.com/heywbj). As the original repo is no longer being actively maintained, we've friendly forked it here to undertake maintenance for modern versions of Python, Django, and Django Rest Framework.

This **package** provides a `RecursiveField` that enables you to serailize a tree, linked list, or even a directed acyclic graph. It also supports validation, deserialization, ModeSerializer, and multi-step recursive structures.

### Example Usage

#### Tree Recursion

```python
from rest_framework import serializers
from django_rest_framework_recursive.fields import RecursiveField

class TreeSerializer(serializers.Serializer):
    name = serializers.CharField()
    children = serializers.ListField(child=RecursiveField())
```

### #Linked List Recursion
```python
from rest_framework import serializers
from django_rest_framework_recursive.fields import RecursiveField

class LinkSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=25)
    next = RecursiveField(allow_null=True)
```

Further use cases are documented in the tests, see [**here**][tests] for more usage examples


## Prerequisites

This package supports:

- Python 3.10
- Django 3.2, 4.0, 4.1, 4.2
- Django Rest Framework 3.13, 3.14, 3.15

During development you will also need:

- `uv` installed as a system package.
- pre-commit 3 _(Optional, but strongly recommended)_

## Installation

Install using `pip`...

```
pip install django-rest-framework-recursive
```

## Local development

When making changes please remember to update the `CHANGELOG.md`, which follows the guidelines at
[keepachangelog]. Add your changes to the `[Unreleased]` section when you create your PR.

[keepachangelog]: https://keepachangelog.com/

### Installation

Ensure one of the above Pythons is installed and used by the `python` executable:****

```sh
python --version
Python 3.10.13   # or any of the supported versions
```

Ensure `uv` is installed as a system package. This can be done with `pipx` or Homebrew.

Then create and activate a virtual environment. If you don't have any other way of managing virtual
environments this can be done by running:

```sh
uv venv
source .venv/bin/activate
```

You could also use [virtualenvwrapper], [direnv] or any similar tool to help manage your virtual
environments.

Once you are in an active virtual environment run

```sh
make dev
```

This will set up your local development environment, installing all development dependencies.

[virtualenvwrapper]: https://virtualenvwrapper.readthedocs.io/
[direnv]: https://direnv.net

### Testing (single Python version)

To run the test suite using the Python version of your virtual environment, run:

```sh
make test
```

### Testing (all supported Python versions)

To test against multiple Python (and package) versions, we need to:

- Have [`nox`][nox] installed outside of the virtualenv. This is best done using `pipx`:

  ```sh
  pipx install nox
  ```

- Ensure that all supported Python versions are installed and available on your system (as e.g.
  `python3.10`, `python3.11` etc). This can be done with `pyenv`.

Then run `nox` with:

```sh
nox
```

Nox will create a separate virtual environment for each combination of Python and package versions
defined in `noxfile.py`.

To list the available sessions, run:

```sh
nox --list-sessions
```

To run the test suite in a specific Nox session, use:

```sh
nox -s $SESSION_NAME
```

[nox]: https://nox.thea.codes/en/stable/

### Static analysis

Run all static analysis tools with:

```sh
make lint
```

### Auto formatting

Reformat code to conform with our conventions using:

```sh
make format
```

### Dependencies

Package dependencies are declared in `pyproject.toml`.

- _package_ dependencies in the `dependencies` array in the `[project]` section.
- _development_ dependencies in the `dev` array in the `[project.optional-dependencies]` section.

For local development, the dependencies declared in `pyproject.toml` are pinned to specific
versions using the `requirements/development.txt` lock file.

#### Adding a new dependency

To install a new Python dependency add it to the appropriate section in `pyproject.toml` and then
run:

```sh
make dev
```

This will:

1. Build a new version of the `requirements/development.txt` lock file containing the newly added
   package.
2. Sync your installed packages with those pinned in `requirements/development.txt`.

This will not change the pinned versions of any packages already in any requirements file unless
needed by the new packages, even if there are updated versions of those packages available.

Remember to commit your changed `requirements/development.txt` files alongside the changed
`pyproject.toml`.

#### Removing a dependency

Removing Python dependencies works exactly the same way: edit `pyproject.toml` and then run
`make dev`.

#### Updating all Python packages

To update the pinned versions of all packages simply run:

```sh
make update
```

This will update the pinned versions of every package in the `requirements/development.txt` lock
file to the latest version which is compatible with the constraints in `pyproject.toml`.

You can then run:

```sh
make dev
```

to sync your installed packages with the updated versions pinned in `requirements/development.txt`.

#### Updating individual Python packages

Upgrade a single development dependency with:

```sh
uv pip compile -P $PACKAGE==$VERSION pyproject.toml --extra=dev --output-file=requirements/development.txt
```

You can then run:

```sh
make dev
```

to sync your installed packages with the updated versions pinned in `requirements/development.txt`.

## Versioning

This project uses [SemVer] for versioning with no additional suffix after the version number. When
it is time for a new release, run the command `make version_{type}` where `{type}` should be
replaced with one of `major`, `minor`, `patch` depending on the type of changes in the release.

The command will update the version in `pyproject.toml` and move the changes from the "Unreleased"
section of the changelog to a versioned section and create a new "Unreleased" section for future
improvements.

[semver]: https://semver.org/
