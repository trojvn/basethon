from pathlib import Path
from typing import Generator

from jsoner import json_read_sync


class BaseSession:
    def __init__(self, base_dir: Path, errors_dir: Path, banned_dir: Path):
        self.base_dir = base_dir
        self.base_dir.mkdir(exist_ok=True)
        self.errors_dir = errors_dir
        self.errors_dir.mkdir(exist_ok=True)
        self.banned_dir = banned_dir
        self.banned_dir.mkdir(exist_ok=True)
        self.json_errors: set[Path] = set()

    def iter_sessions(self) -> Generator:
        for item in self.base_dir.glob("*.session"):
            json_file = item.with_suffix(".json")
            if not json_file.is_file():
                self.json_errors.add(json_file)
                continue
            if not (json_data := json_read_sync(json_file)):
                self.json_errors.add(json_file)
                continue
            yield item, json_file, json_data
