import abc
import os
from ..core import File
from _typeshed import Incomplete
from abc import ABC, abstractmethod
from io import BytesIO
from typing import BinaryIO

__all__ = ['render_word_file', 'WordFileComponent', 'WordFileImage', 'WordFileResult', 'WordFileTag', 'WordFileTemplate']

class WordFileComponent(ABC, metaclass=abc.ABCMeta):
    identifier: Incomplete
    @abstractmethod
    def __init__(self, identifier: str): ...

class WordFileTag(WordFileComponent):
    value: Incomplete
    def __init__(self, identifier: str, value: object) -> None: ...

class WordFileImage(WordFileComponent):
    file_content: Incomplete
    width: Incomplete
    height: Incomplete
    def __init__(self, file: BinaryIO, identifier: str, width: int = None, height: int = None) -> None: ...
    @classmethod
    def from_path(cls, file_path: str | bytes | os.PathLike, identifier: str, width: int = None, height: int = None) -> WordFileImage: ...

class WordFileResult:
    def __init__(self, *, file_content: bytes = None) -> None: ...
    @property
    def file_content(self) -> bytes: ...

class WordFileTemplate:
    def __init__(self, file: BytesIO, components: list[WordFileComponent]) -> None: ...
    @classmethod
    def from_path(cls, file_path: str | bytes | os.PathLike, components: list[WordFileComponent]) -> WordFileTemplate: ...
    def render(self) -> WordFileResult: ...
    @property
    def result(self) -> WordFileResult: ...

def render_word_file(template: BinaryIO, components: list[WordFileComponent]) -> File: ...
