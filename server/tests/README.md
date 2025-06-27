# Audapolis Server Tests

This directory contains the tests for the Audapolis Python backend.

## Running Tests

To run all tests, navigate to the `server` directory and use `poetry`:

```bash
cd server
poetry run pytest
```

## Test Coverage

To generate a test coverage report, use the following command:

```bash
cd server
poetry run pytest --cov=app --cov-report=term-missing
```

This will display a summary of the code coverage in your terminal.
