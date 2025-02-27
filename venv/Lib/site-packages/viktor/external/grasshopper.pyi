from ..core import File
from .external_program import ExternalProgram
from _typeshed import Incomplete
from typing import Any

__all__ = ['GrasshopperAnalysis']

class _DataTree:
    data: Incomplete
    def __init__(self, name: str) -> None: ...
    def append(self, path: list, items: list) -> None: ...

class GrasshopperAnalysis(ExternalProgram):
    script: Incomplete
    def __init__(self, *, script: File, input_parameters: dict[str, Any] = None) -> None: ...
    def get_output(self) -> dict: ...
