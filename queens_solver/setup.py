import subprocess
import sys


def install_playwright_browsers(browsers: tuple = ("chromium",)) -> None:
    """Install Playwright browser binaries.

    This function invokes the Playwright CLI installer using the
    current Python interpreter and installs the specified browser
    binaries required by Playwright automation.

    Args:
        browsers: Tuple of Playwright browser names to install.
            Common values include:
                - "chromium"
                - "firefox"
                - "webkit"

            Defaults to installing Chromium only.

    Raises:
        subprocess.CalledProcessError: If the Playwright installation
            command exits with a nonzero status.

    Example:
        ```python
        install_playwright_browsers()

        install_playwright_browsers(
            browsers=("chromium", "firefox")
        )
        ```
    """
    subprocess.run(
        [sys.executable, "-m", "playwright", "install"] + list(browsers),
        check=True,
    )
