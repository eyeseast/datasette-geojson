from setuptools import setup
import os

VERSION = "0.3.0"


def get_long_description():
    with open(
        os.path.join(os.path.dirname(os.path.abspath(__file__)), "README.md"),
        encoding="utf8",
    ) as fp:
        return fp.read()


setup(
    name="datasette-geojson",
    description="Add GeoJSON as an output option",
    long_description=get_long_description(),
    long_description_content_type="text/markdown",
    author="Chris Amico",
    url="https://github.com/eyeseast/datasette-geojson",
    project_urls={
        "Issues": "https://github.com/eyeseast/datasette-geojson/issues",
        "CI": "https://github.com/eyeseast/datasette-geojson/actions",
        "Changelog": "https://github.com/eyeseast/datasette-geojson/releases",
    },
    license="Apache License, Version 2.0",
    version=VERSION,
    packages=["datasette_geojson"],
    entry_points={"datasette": ["datasette_geojson = datasette_geojson"]},
    install_requires=["datasette", "geojson"],
    extras_require={"test": ["pytest", "pytest-asyncio", "geojson-to-sqlite"]},
    tests_require=["datasette-geojson[test]"],
    python_requires=">=3.6",
)
