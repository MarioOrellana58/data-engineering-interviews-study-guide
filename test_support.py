"""Helpers that load student work by default and reference answers on request."""

from __future__ import annotations

import importlib.util
import os
from pathlib import Path
from types import ModuleType


def homework_path(test_file: str, filename: str) -> Path:
    topic = Path(test_file).resolve().parents[1]
    if os.getenv("STUDY_USE_SOLUTIONS") == "1":
        repository = Path(__file__).resolve().parent
        return repository / "solutions" / topic.parent.name / topic.name / filename
    return topic / filename


def load_homework(test_file: str) -> ModuleType:
    path = homework_path(test_file, "homework.py")
    name = "homework_" + "_".join(path.parts[-3:-1]).replace("-", "_")
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Cannot import {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module
