# Contributing to `convert_flux`

Thank you for your interest in contributing to `convert_flux`! We welcome and encourage contributions 
of many kinds. Our goal is to keep this a positive, inclusive, successful, and growing community.

## Table of Contents

- [Getting Started](#getting-started)
- [Setting Up Your Development Environment](#setting-up-your-development-environment)
- [Making Changes](#making-changes)
- [Submitting Changes](#submitting-changes)
- [Reporting Bugs](#reporting-bugs)
- [Suggesting Enhancements](#suggesting-enhancements)
- [Coding Guidelines](#coding-guidelines)
- [Testing](#testing)
- [Documentation](#documentation)
- [Getting Help](#getting-help)

## Getting Started

### Prerequisites

- GitHub account
- Git installed on your machine
- Python

### Set Up GitHub and Git

If you're new to Git and GitHub, see the [GitHub documentation for contributing to projects](https://docs.github.com/en/get-started/quickstart/contributing-to-projects).

### Create a Fork and Clone

1. Fork the repository by clicking the "Fork" button on GitHub
2. Clone your fork locally:

```
git clone https://github.com/YOUR-USERNAME/convert_flux.git
cd convert_flux
```

## Setting Up Your Development Environment

### Create an Isolated Python Environment (Recommended)

Using conda:

```
conda create -n convert_flux_dev python=3.13
conda activate convert_flux_dev
```


Or using venv:

```
python -m venv convert-flux-env
source convert-flux-env/bin/activate
```

### Install Development Dependencies

```
pip install -e ".[dev]"
```

### Install Pre-commit (Optional but Recommended)

Pre-commit runs code quality checks automatically before you commit:
```
pip install pre-commit
pre-commit install
```


## Making Changes

### Create a Branch

Always create a new branch for your changes:

```
git switch main
git pull upstream main --ff-only
git switch -c descriptive-branch-name
```

Use descriptive branch names like `fix-bug-123` or `add-feature-xyz`.

### Make Your Changes

1. Make code changes - Use your editor or IDE to make modifications
2. Test your changes - See Testing section
3. Update documentation - If applicable
4. Add a changelog entry - Follow the project's changelog format

### Commit Your Changes
Commit message guidelines:
- Make sure to use a commit-tag for [semantic versioning](https://www.geeksforgeeks.org/software-engineering/introduction-semantic-versioning/) because our package releases are automated using [`python-semantic-release`](https://python-semantic-release.readthedocs.io/en/latest/). `python-semantic-release` is configured to follow the [conventional commit guidlines](https://www.conventionalcommits.org/en/v1.0.0/). As a summary:
	- For small changes start the commit message with `fix:` to increment the minor tag in the version
   - For new features or larger changes start the commit message with `feat:` to increment the middle tag in the version
- Use the present tense ("add feature" not "added feature")
- Use the imperative mood ("move cursor to..." not "moves cursor to...")
- Limit the first line to 72 characters
- Reference issues and pull requests liberally after the first line


```
git add files-you-changed
git commit -m "commit-tag: Clear, descriptive commit message"
```
	
## Submitting Changes
	
### Push Your Branch

```
git push
```


### Create a Pull Request

1. Go to your fork on GitHub
2. Click "Compare & pull request"
3. Fill out the PR template completely
4. If your PR is a work in progress, create a draft PR instead
5. Submit the PR

Tips for a successful PR:
- Reference any related issues
- Keep PRs focused on a single feature or bug fix
- Ensure all tests pass
- Keep commit history clean
- Respond promptly to feedback

### Updating Your PR

If reviewers request changes:
```
git add files-you-changed
git commit -m "Address feedback: some detailed commit message"
git push
```


## Reporting Bugs

### Before Submitting a Bug Report

- Check the issue tracker to see if the bug has already been reported
- Check the documentation to ensure you're using the feature correctly

### How to Submit a Bug Report

When filing an issue, please include:

- Clear title and description - Use a descriptive title
- Steps to reproduce - Provide specific steps
- Expected behavior - What you expected to happen
- Actual behavior - What actually happened
- Environment details - OS, Python version, package version, etc.
- Minimal code example - If applicable, provide a minimal reproducible example

## Suggesting Enhancements

### Before Suggesting an Enhancement

- Check the issue tracker to see if it has already been suggested
- Check the documentation and code to see if the feature already exists

### How to Submit an Enhancement Suggestion

When suggesting an enhancement, please include:

- Clear title and description - Use a descriptive title
- Motivation - Why would this enhancement be useful?
- Proposed implementation - Describe how you envision it working
- Example use cases - Provide concrete examples

## Coding Guidelines

### Style Guide

This project follows PEP 8 with the following guidelines:

- Maximum line length: 88 characters (Black default)
- Use type hints where possible
- Write docstrings for all public functions and classes

### Code Formatting

We use ruff for code formatting. If you've installed pre-commit, this will run automatically.

To manually format your code run 
```
ruff
```


## Testing

### Running Tests

Run the test suite with:
```
pytest
```


Run tests for a specific module:
```
pytest tests/module-name.py
```


### Writing Tests

- Place tests in the `tests/` directory
- Use descriptive test names
- Aim for good coverage of your new code
- See existing tests for examples

## Documentation

### Building Documentation
```
cd docs
make html
```


View the built documentation in `docs/_build/html/index.html`

### Writing Documentation

- Write clear docstrings in the Google or NumPy style
- Update relevant documentation files
- Include examples where appropriate

## Getting Help

Questions? Reach out!

## Additional Resources

- Project Documentation - [link-to-docs once we have them]
- Project Roadmap - [link-to-roadmap once we set it up]
- [Issue Tracker](https://github.com/alexander-group/convert_flux/issues)

---

Thank you for contributing to convert_flux! 🎉
