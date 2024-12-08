from pathlib import Path
import os
from typing import List


def read_file(path: str):
    with open(path, "r") as f:
        return f.read()


def read_binary_file(path: str) -> bytes:
    with open(path, "rb") as f:
        return f.read()


def write_binary_file(path: str, data: bytes):
    with open(path, "wb") as f:
        return f.write(data)


def file_exists(path: str):
    return Path(path).is_file()


def read_dir_files(path: str):
    ret: List[str] = []
    for entry in os.scandir(path):
        if entry.is_file():
            ret.append(entry.name)
    return ret
