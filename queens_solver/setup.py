import subprocess
import sys


def install_playwright_browsers(browsers: tuple = ("chromium",)) -> None:
    """Install Playwright browser binaries.

    Invokes the Playwright CLI installer via the current Python interpreter.

    Args:
        browsers: Tuple of Playwright browser names to install
            (e.g. ``"chromium"``, ``"firefox"``, ``"webkit"``).
            Defaults to ``("chromium",)``.

    Raises:
        subprocess.CalledProcessError: If the Playwright install command
            exits with a nonzero status.
    """
    subprocess.run(
        [sys.executable, "-m", "playwright", "install"] + list(browsers),
        check=True,
    )
