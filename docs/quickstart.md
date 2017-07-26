# Quick start
The project is not supposed to be run in any MVC, but it was built as a framework for future MVC implementations.
However, you can run the test by simply running [tests.py](tests.py) from the command line.

## Test cases
1. Seed a database (SQLite) with sample data for each type.
3. Ensure the relationships work as expected
4. Find all reports that a loan belongs to
5. Calculate the sum of all loans that went into a specific report

## About the system requirements
Python 3.5.2
Flask-SQLAlchemy 2.2
SQLAlchemy 1.1.12
SQLALchemy-migrate 0.11.0

You can find the rest of the requirements in [requirements.txt](requirements.txt)
