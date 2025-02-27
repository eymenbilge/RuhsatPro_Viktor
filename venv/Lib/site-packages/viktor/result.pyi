import abc
from .core import File, _Result, _SerializableObject
from .views import ImageResult
from _typeshed import Incomplete
from io import BytesIO
from munch import Munch
from typing import Any

__all__ = ['DownloadResult', 'OptimizationResult', 'OptimizationResultElement', 'SetParamsResult']

class _ButtonResult(_Result, metaclass=abc.ABCMeta): ...

class SetParamsResult(_ButtonResult):
    def __init__(self, params: dict | Munch) -> None: ...
    def get(self, key: str) -> Any: ...
SetParametersResult = SetParamsResult

class DownloadResult(_ButtonResult):
    def __init__(self, file_content: str | bytes | File | BytesIO = None, file_name: str = None, encoding: str = 'utf-8', *, zipped_files: dict[str, File | BytesIO] = None) -> None: ...

class OptimizationResultElement:
    def __init__(self, params: dict | Munch, analysis_result: dict = None) -> None: ...
OptimisationResultElement = OptimizationResultElement

class OptimizationResult(_ButtonResult):
    result_column_names_input: Incomplete
    result_column_names_result: Incomplete
    def __init__(self, results: list[OptimizationResultElement], result_column_names_input: list[str] = None, output_headers: dict = None, image: ImageResult = None) -> None: ...
OptimisationResult = OptimizationResult

class ViktorResult(_SerializableObject):
    def __init__(self, optimisation_result: OptimizationResult = None, set_parameters_result: SetParamsResult = None, download_result: DownloadResult = None, *, optimization_result: OptimizationResult = None, set_params_result: SetParamsResult = None) -> None: ...
