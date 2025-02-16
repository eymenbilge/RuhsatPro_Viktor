from ..core import File
from .external_program import ExternalProgram
from io import BytesIO

__all__ = ['PythonAnalysis']

class PythonAnalysis(ExternalProgram):
    def __init__(self, script: File = None, script_key: str = '', files: list[tuple[str, BytesIO | File]] = None, output_filenames: list[str] = None) -> None: ...
    def get_output_file(self, filename: str) -> File | None: ...
