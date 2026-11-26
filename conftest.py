"""Repository-wide test reporting safeguards."""

import os


def pytest_sessionstart(session):
    target = "REFERENCE SOLUTIONS" if os.getenv("STUDY_USE_SOLUTIONS") == "1" else "STUDENT HOMEWORK"
    reporter = session.config.pluginmanager.get_plugin("terminalreporter")
    if reporter is not None:
        reporter.write_line(f"STUDY TARGET: {target}", bold=True)
