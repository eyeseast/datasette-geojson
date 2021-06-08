# datasette-geojson

[![PyPI](https://img.shields.io/pypi/v/datasette-geojson.svg)](https://pypi.org/project/datasette-geojson/)
[![Changelog](https://img.shields.io/github/v/release/eyeseast/datasette-geojson?include_prereleases&label=changelog)](https://github.com/eyeseast/datasette-geojson/releases)
[![Tests](https://github.com/eyeseast/datasette-geojson/workflows/Test/badge.svg)](https://github.com/eyeseast/datasette-geojson/actions?query=workflow%3ATest)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/eyeseast/datasette-geojson/blob/main/LICENSE)

Add GeoJSON as an output option for datasette queries.

## Installation

Install this plugin in the same environment as Datasette.

    datasette install datasette-geojson

## Usage

To render GeoJSON, add a `.geojson` extension to any query URL.

## Development

To set up this plugin locally, first checkout the code. Then create a new virtual environment:

    cd datasette-geojson
    python3 -mvenv venv
    source venv/bin/activate

Or if you are using `pipenv`:

    pipenv shell

Now install the dependencies and tests:

    pip install -e '.[test]'

To run the tests:

    pytest
