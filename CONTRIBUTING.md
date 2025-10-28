# Contributing to pyfiles_db

Thank you for considering contributing to **pyfiles_db**! We welcome contributions that improve the functionality, documentation, and usability of the project.

## How to Contribute

### Reporting Issues

If you encounter a bug or have a feature request, please open an issue in the [Issues](https://github.com/LangNeuron/pyfiles_db/issues) section. When reporting an issue, include:

- A descriptive title
- Steps to reproduce the issue
- Expected and actual behavior
- Any relevant logs or error messages

### Submitting Pull Requests

To submit a pull request:

1. Fork the repository
2. Create a new branch (`git checkout -b feature/your-feature-name`)
3. Make your changes
4. Ensure all tests pass (`pytest` recommended)
5. Commit your changes (`git commit -am 'Add new feature'`)
6. Push to your fork (`git push origin feature/your-feature-name`)
7. Open a pull request to the `main` branch of the original repository

### Code Style

- Follow PEP 8 guidelines
- Use descriptive variable and function names
- Include comments and docstrings where appropriate

### Testing

Ensure your changes are covered by tests. We use `pytest` for testing. Run tests using:

```bash
pytest
```

# Contributing to pyfiles_db

Thank you for considering contributing to **pyfiles_db**! We welcome contributions that improve the functionality, documentation, and usability of the project.

## How to Contribute

### Reporting Issues

If you encounter a bug or have a feature request, please open an issue in the [Issues](https://github.com/LangNeuron/pyfiles_db/issues) section. When reporting an issue, include:

- A descriptive title
- Steps to reproduce the issue
- Expected and actual behavior
- Any relevant logs or error messages

### Submitting Pull Requests

To submit a pull request:

1. Fork the repository
2. Create a new branch (`git checkout -b feature/your-feature-name`)
3. Make your changes
4. Ensure all tests pass (`pytest` recommended)
5. Commit your changes (`git commit -am 'Add new feature'`)
6. Push to your fork (`git push origin feature/your-feature-name`)
7. Open a pull request to the `main` branch of the original repository

### Managing Dependencies with Poetry

We use **Poetry** for dependency management. When adding or updating dependencies:



1. Add the dependency via Poetry:

```bash
poetry add package_name
```

or for development dependencies:

```bash
poetry add --dev package_name
```

2. Make sure pyproject.toml is updated correctly.

3. Run tests to ensure compatibility:

```bash
poetry install
pytest
```

4. Commit any changes to pyproject.toml and poetry.lock.


### Code Style

- Follow PEP 8 guidelines
- Use descriptive variable and function names
- Include comments and docstrings where appropriate

### Testing

Ensure your changes are covered by tests. We use `pytest` for testing. Run tests using:

```bash
pytest
```

## Documentation

Update the README.md or other relevant documentation files to reflect your changes.

## Code of Conduct

By participating in this project, you agree to abide by the [Code of Conduct](https://github.com/LangNeuron/pyfiles_db/blob/main/CODE_OF_CONDUCT.md).

## License

By contributing, you agree that your contributions will be licensed under the project's [LICENSE](https://github.com/LangNeuron/pyfiles_db/blob/main/LICENSE).
