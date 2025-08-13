"""Test cases for the main application commands using Typer's CLI runner."""

from typer.testing import CliRunner

from theproject.cli import app

runner = CliRunner()


def test_version() -> None:
    """Test the `version` command of the application.

    This test checks if the `version` command runs without any errors.

    Scenario:
        - Run the `version` command of the application.

    Expected Result:
        - The command should execute successfully and return the application version.
    Given:
        - The application is set up with a `version` command.
    When:
        - The `version` command is invoked using the CLI runner.
    Then:
        - The command should exit with code 0, indicating success.
        - The output should contain the application version information.
    And:
        - If the command fails, the test should fail with the output message.

    Note:
        - This test does not check the actual version number,
        only that the command runs successfully.

    """
    result = runner.invoke(app, ["version"])
    assert result.exit_code == 0, result.output


def test_info() -> None:
    """Test the `info` command of the application.

    This test checks if the `info` command runs without any errors.

    Scenario:
        - Run the `info` command of the application.

    Expected Result:
        - The command should execute successfully and return the application
        information.
    Given:
        - The application is set up with an `info` command.
    When:
        - The `info` command is invoked using the CLI runner.
    Then:
        - The command should exit with code 0, indicating success.
        - The output should contain the application information.
    And:
        - If the command fails, the test should fail with the output message.

    Note:
        - This test does not check the actual information content,
        only that the command runs successfully.

    """
    result = runner.invoke(app, ["info"])
    assert result.exit_code == 0, result.output
