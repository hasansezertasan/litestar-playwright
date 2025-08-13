# pyproject

This is a Opinionated GitHub Repository Template with the following:

- `uv` package manager support.
- Build with `hatchling`, dynamic versioning through GitHub Release Tags.
- Tests setup with `pytest` and `tox`.
- Linting and Formatting with `ruff`.
- Type checking with `mypy`.
- Logging setup.
- Configuration setup.
- Typer CLI
- `pre-commit` configuration.
- Dev container configuration.
- Generic `.gitignore` setup.
- GitHub Actions:
  - CI: Type Checking, Linting, Formatting, Testing, etc.
  - CD: PyPI Trusted Host Publishing and GitHub Releases.
- Release Drafter.
- PR Title Checker.
- Issue and Pull Request Templates and Configurations.
- VSCode Debugging Configuration.

## Usage

### Renaming

```sh
# Replace any text containing "theproject" with "yourproject" and "hasansezertasan" with "yourname"
LC_ALL=C find . -type f -exec sed -i '' 's/theproject/yourproject/g; s/hasansezertasan/yourname/g' {} +
# Rename any file or directory containing "theproject" with "yourproject"
find . -name '*theproject*' -exec bash -c 'for f; do mv "$f" "${f//theproject/yourproject}"; done' _ {} +
```

### Customizing

- [ ] [Rename](#renaming) the project name and author.
- [ ] Go ahead and update the [LICENSE](LICENSE) with your preferred license.
- [ ] Go ahead and update the [CONTRIBUTING.md](CONTRIBUTING.md) with your preferred contribution guidelines.
- [ ] Go ahead and update the [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md) with your preferred code of conduct.
- [ ] Go ahead and update the [README_ACTUAL.md](README_ACTUAL.md) with your own project details.
- [ ] Go ahead and update the [CHANGELOG.md](CHANGELOG.md) with your preferred changelog format.
- [ ] Go ahead and update the [pyproject.toml](pyproject.toml) with your own project details. Make sure you have completed all TODOs.
- [ ] Double check the [.gitignore](.gitignore) file and don't stage any secrets!
- [ ] Go ahead and update your repository settings as you wish.

### PyPI Integration

How to integrate with PyPI with GitHub Actions?

1. Go to [Trusted Publisher Management](https://pypi.org/manage/account/publishing//).
1. Scroll down to the "Add a new pending publisher" section.
1. Select "GitHub".
1. Enter the name of your package in the "PyPI Project Name" field.
1. Enter the username of your GitHub account in the "Owner" field.
1. Enter the name of your repository in the "Repository name" field.
1. Enter the workflow name of the [CD](.github/workflows/cd.yml) workflow in the "Workflow name" field. Just type `cd.yml` if you haven't changed the workflow name.
1. Enter the environment name of the [CD](.github/workflows/cd.yml) workflow in the "Environment name" field. Just type `publish` if you haven't changed the environment name.
1. Click the "Add" button.

### Release

How to release a new version of the project?

1. Create a new release draft on GitHub.
1. Update your [CHANGELOG.md](CHANGELOG.md) with the new version.
1. Convert the release draft to a release.
1. The release will trigger the [CD](.github/workflows/cd.yml) workflow:
    1. The workflow will build the project and publish it to PyPI.
    1. The workflow will also attach the build artifacts to the release.

### Sayonara

```sh
# Remove this file and copy the actual README
rm README.md && cp README_ACTUAL.md README.md
```

## Author

This project is maintained by [Hasan Sezer Taşan][author], It's me :wave:

## Disclaimer

This template is not intended to be used for malicious purposes. The author is not responsible for any damage caused by this template. Use at your own risk.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

<!-- Refs -->
[author]: https://github.com/hasansezertasan
[theproject]: https://github.com/hasansezertasan/theproject
[hatchling]: https://hatch.pypa.io/latest/
[uv]: https://docs.astral.sh/uv/
[pytest]: https://docs.pytest.org/en/stable/
[tox]: https://tox.wiki/en/latest/
[ruff]: https://docs.astral.sh/ruff/
[mypy]: https://mypy.readthedocs.io/en/stable/
[typer]: https://typer.tiangolo.com/
[pre-commit]: https://pre-commit.com/
