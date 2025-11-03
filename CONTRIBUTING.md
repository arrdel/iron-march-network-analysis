# Contributing to Iron March Network Analysis

Thank you for your interest in contributing! This document provides guidelines for contributing to the project.

## Getting Started

1. Fork the repository
2. Clone your fork: `git clone https://github.com/yourusername/knowledge_graph.git`
3. Create a new branch: `git checkout -b feature/your-feature-name`
4. Make your changes
5. Run tests to ensure everything works
6. Commit your changes with clear messages
7. Push to your fork and submit a pull request

## Development Setup

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
pip install -e .

# Install development dependencies
pip install pytest black flake8 mypy
```

## Code Style

- Follow PEP 8 guidelines
- Use meaningful variable and function names
- Add docstrings to all public functions and classes
- Include type hints where appropriate
- Keep functions focused and modular

### Formatting

We use `black` for code formatting:

```bash
black src/ tests/
```

### Linting

We use `flake8` for linting:

```bash
flake8 src/ tests/
```

## Testing

Write unit tests for new features:

```bash
pytest tests/
```

## Pull Request Process

1. Ensure your code passes all tests
2. Update documentation if needed
3. Add your changes to the CHANGELOG (if applicable)
4. Submit a pull request with a clear description of changes
5. Wait for review and address feedback

## Code Review

All submissions require review. We use GitHub pull requests for this purpose.

## Reporting Issues

Use GitHub Issues to report bugs or suggest features. Include:

- Clear description of the issue
- Steps to reproduce (for bugs)
- Expected vs actual behavior
- System information (OS, Python version, etc.)

## Questions?

Feel free to open an issue with your question or reach out to the maintainers.
