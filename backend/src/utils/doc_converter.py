import subprocess
import re
from tempfile import TemporaryDirectory, NamedTemporaryFile

from .files import read_binary_file, write_binary_file


def convert_to(source: bytes, from_format: str, to_format: str, timeout: int) -> bytes:

    with NamedTemporaryFile(
        suffix=f".{from_format}"
    ) as src_file, TemporaryDirectory() as out_dir:

        write_binary_file(src_file.name, source)

        args = [
            "libreoffice",
            "--headless",
            "--convert-to",
            to_format,
            "--outdir",
            out_dir,
            src_file.name,
        ]
        process = subprocess.run(
            args, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=timeout
        )
        out_file_gr = re.search("-> (.*?) using filter", process.stdout.decode())

        if out_file_gr is None:
            raise ConvertingError(process.stdout.decode())
        else:
            return read_binary_file(out_file_gr.group(1))


class ConvertingError(Exception):
    def __init__(self, output):
        self.output = output
