from . import GenericAnalysis
from ..core import File
from io import BytesIO

__all__ = ['MatlabAnalysis']

class MatlabAnalysis(GenericAnalysis):
    def __init__(self, files: list[tuple[str, BytesIO | File]] | None = None, executable_key: str = 'matlab', output_filenames: list[str] = None) -> None: ...
