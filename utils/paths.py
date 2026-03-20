import sys
from pathlib import Path


def base_path() -> Path:

    if getattr(sys, "frozen", False):
        return Path(sys._MEIPASS)
    
    return Path(__file__).resolve().parent.parent


def resources_path(*path) -> Path:
    return base_path().joinpath(*path)


def ui_path(file_name: str) -> Path:
    return resources_path("ui", file_name)
