from ..core import File
from .external_program import ExternalProgram
from _typeshed import Incomplete

__all__ = ['DStabilityAnalysis']

class DStabilityAnalysis(ExternalProgram):
    input_file: Incomplete
    def __init__(self, input_file: File) -> None: ...
    def get_output_file(self, extension: str = '.stix') -> File | None: ...
