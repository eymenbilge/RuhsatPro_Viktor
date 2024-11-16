from ..core import File
from .external_program import ExternalProgram
from _typeshed import Incomplete
from io import BytesIO

__all__ = ['GRLWeapAnalysis']

class GRLWeapAnalysis(ExternalProgram):
    input_file: Incomplete
    def __init__(self, input_file: BytesIO | File) -> None: ...
    def get_output_file(self, *, as_file: bool = False) -> BytesIO | File | None: ...
