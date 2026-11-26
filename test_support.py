"""Small helpers shared by exercises; not an answer key."""

from __future__ import annotations

import importlib.util
from pathlib import Path
from types import ModuleType


def load_homework(test_file: str) -> ModuleType:
    path = Path(test_file).resolve().parents[1] / "homework.py"
    name = "homework_" + "_".join(path.parts[-3:-1]).replace("-", "_")
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Cannot import {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def homework_path(test_file: str, filename: str) -> Path:
    return Path(test_file).resolve().parents[1] / filename
