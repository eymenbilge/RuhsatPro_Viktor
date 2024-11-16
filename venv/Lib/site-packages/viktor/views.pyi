import abc
import datetime
import os
import pandas as pd
from .api_v1 import FileResource
from .core import Color, File, _Result
from .geometry import GeoPoint, GeoPolygon, GeoPolyline, Point, TransformableObject
from _typeshed import Incomplete
from abc import ABC
from collections import OrderedDict
from enum import Enum
from io import BytesIO, StringIO
from pandas.io.formats.style import Styler
from typing import Any, Callable, Literal, Sequence

__all__ = ['DataGroup', 'DataItem', 'DataResult', 'DataStatus', 'DataView', 'GeoJSONAndDataResult', 'GeoJSONAndDataView', 'GeoJSONResult', 'GeoJSONView', 'GeometryAndDataResult', 'GeometryAndDataView', 'GeometryResult', 'GeometryView', 'IFCAndDataResult', 'IFCAndDataView', 'IFCResult', 'IFCView', 'ImageAndDataResult', 'ImageAndDataView', 'ImageResult', 'ImageView', 'InteractionEvent', 'Label', 'MapAndDataResult', 'MapAndDataView', 'MapEntityLink', 'MapFeature', 'MapLabel', 'MapLegend', 'MapLine', 'MapPoint', 'MapPolygon', 'MapPolyline', 'MapResult', 'MapView', 'PDFResult', 'PDFView', 'PlotlyAndDataResult', 'PlotlyAndDataView', 'PlotlyResult', 'PlotlyView', 'Summary', 'SummaryItem', 'TableCell', 'TableHeader', 'TableResult', 'TableView', 'WebAndDataResult', 'WebAndDataView', 'WebResult', 'WebView']

class DataStatus(Enum):
    INFO: DataStatus
    SUCCESS: DataStatus
    WARNING: DataStatus
    ERROR: DataStatus

class DataItem:
    def __init__(self, label: str, value: str | float | None, subgroup: DataGroup = None, *, prefix: str = '', suffix: str = '', number_of_decimals: int = None, status: DataStatus = ..., status_message: str = '', explanation_label: str = '') -> None: ...
    @property
    def subgroup(self) -> DataGroup: ...

class DataGroup(OrderedDict):
    def __init__(self, *args: DataItem, **kwargs: DataItem) -> None: ...
    @classmethod
    def from_data_groups(cls, groups: list['DataGroup']) -> DataGroup: ...

class MapEntityLink:
    def __init__(self, label: str, entity_id: int) -> None: ...

class MapFeature(ABC, metaclass=abc.ABCMeta):
    def __init__(self, *, title: str = None, description: str = None, color: Color = ..., entity_links: list[MapEntityLink] = None, identifier: int | str = None) -> None: ...

class MapPoint(MapFeature):
    def __init__(self, lat: float, lon: float, alt: float = 0, *, icon: str = None, size: Literal['small', 'medium', 'large'] = 'medium', **kwargs: Any) -> None: ...
    @classmethod
    def from_geo_point(cls, point: GeoPoint, *, icon: str = None, size: Literal['small', 'medium', 'large'] = 'medium', **kwargs: Any) -> MapPoint: ...
    @property
    def lat(self) -> float: ...
    @property
    def lon(self) -> float: ...
    @property
    def alt(self) -> float: ...

class MapPolyline(MapFeature):
    def __init__(self, *points: MapPoint, **kwargs: Any) -> None: ...
    @classmethod
    def from_geo_polyline(cls, polyline: GeoPolyline, **kwargs: Any) -> MapPolyline: ...
    @property
    def points(self) -> list[MapPoint]: ...

class MapLine(MapPolyline):
    def __init__(self, start_point: MapPoint, end_point: MapPoint, **kwargs: Any) -> None: ...
    @property
    def start_point(self) -> MapPoint: ...
    @property
    def end_point(self) -> MapPoint: ...

class MapPolygon(MapFeature):
    def __init__(self, points: list[MapPoint], *, holes: list['MapPolygon'] = None, **kwargs: Any) -> None: ...
    @classmethod
    def from_geo_polygon(cls, polygon: GeoPolygon, **kwargs: Any) -> MapPolygon: ...
    @property
    def points(self) -> list[MapPoint]: ...
    @property
    def holes(self) -> list['MapPolygon']: ...

class MapLegend:
    def __init__(self, entries: list[tuple[Color, str]]) -> None: ...

class MapLabel:
    def __init__(self, lat: float, lon: float, text: str, scale: float, *, fixed_size: bool = False) -> None: ...

class Label:
    size_factor: Incomplete
    color: Incomplete
    def __init__(self, point: Point, *text: str, size_factor: float = 1, color: Color = ...) -> None: ...
    @property
    def point(self) -> Point: ...
    @property
    def text(self) -> str | tuple[str, ...]: ...
    def serialize(self) -> dict: ...
TableCellValue = str | float | int | bool | datetime.datetime | datetime.date | None

class TableCell:
    value: Incomplete
    text_color: Incomplete
    background_color: Incomplete
    def __init__(self, value: TableCellValue, *, text_color: Color | None = None, background_color: Color | None = None, text_style: Literal['bold', 'italic'] | None = None) -> None: ...

class TableHeader:
    class _TYPE(Enum):
        STRING: str
        NUMBER: str
        BOOLEAN: str
        DATE: str
        MIXED: str
    class _ALIGN(Enum):
        CENTER: str
        LEFT: str
        RIGHT: str
    title: Incomplete
    def __init__(self, title: str, *, align: Literal['center', 'left', 'right'] | None = None, num_decimals: int | None = None) -> None: ...

class _SubResult(_Result, ABC, metaclass=abc.ABCMeta): ...

class _ViewResult(ABC, metaclass=abc.ABCMeta):
    def __init__(self, version: int) -> None: ...

class _DataSubResult(_SubResult):
    data: Incomplete
    def __init__(self, data: DataGroup) -> None: ...

class _GeometrySubResult(_SubResult):
    geometry: Incomplete
    geometry_type: Incomplete
    labels: Incomplete
    def __init__(self, geometry: TransformableObject | Sequence[TransformableObject] | File, labels: list[Label] = None, *, geometry_type: str = 'gltf') -> None: ...

class _ImageSubResult(_SubResult):
    image: Incomplete
    def __init__(self, image: File, image_type: str | None) -> None: ...

class _GeoJSONSubResult(_SubResult):
    geojson: Incomplete
    labels: Incomplete
    legend: Incomplete
    interaction_groups: Incomplete
    def __init__(self, geojson: dict, labels: list[MapLabel] = None, legend: MapLegend = None, interaction_groups: dict[str, Sequence[int | str | MapFeature]] = None) -> None: ...

class _WebSubResult(_SubResult):
    html: Incomplete
    url: Incomplete
    def __init__(self, *, html: File = None, url: str = None) -> None: ...

class _PlotlySubResult(_SubResult):
    figure: Incomplete
    def __init__(self, figure: str | dict) -> None: ...

class _PDFSubResult(_SubResult):
    url: Incomplete
    file: Incomplete
    def __init__(self, *, file: File = None, url: str = None) -> None: ...

class _IFCSubResult(_SubResult):
    ifc: Incomplete
    def __init__(self, ifc: File | FileResource) -> None: ...

class _TableSubResult(_SubResult):
    data: Incomplete
    column_headers: Incomplete
    row_headers: Incomplete
    enable_sorting_and_filtering: Incomplete
    def __init__(self, data: Sequence[Sequence[TableCellValue | TableCell]], column_headers: Sequence[str | TableHeader] | None, row_headers: Sequence[str | TableHeader] | None, enable_sorting_and_filtering: bool | None) -> None: ...

class GeometryResult(_ViewResult):
    geometry: Incomplete
    geometry_type: Incomplete
    labels: Incomplete
    def __init__(self, geometry: TransformableObject | Sequence[TransformableObject] | File, labels: list[Label] = None, *, geometry_type: str = 'gltf') -> None: ...

class GeometryAndDataResult(_ViewResult):
    geometry: Incomplete
    geometry_type: Incomplete
    labels: Incomplete
    data: Incomplete
    def __init__(self, geometry: TransformableObject | Sequence[TransformableObject] | File, data: DataGroup, labels: list[Label] = None, *, geometry_type: str = 'gltf') -> None: ...

class DataResult(_ViewResult):
    data: Incomplete
    def __init__(self, data: DataGroup) -> None: ...

class ImageResult(_ViewResult):
    image: Incomplete
    def __init__(self, image: StringIO | BytesIO | File) -> None: ...
    @classmethod
    def from_path(cls, file_path: str | bytes | os.PathLike) -> ImageResult: ...

class ImageAndDataResult(_ViewResult):
    image: Incomplete
    data: Incomplete
    def __init__(self, image: StringIO | BytesIO | File, data: DataGroup) -> None: ...

class GeoJSONResult(_ViewResult):
    labels: Incomplete
    legend: Incomplete
    interaction_groups: Incomplete
    def __init__(self, geojson: dict, labels: list[MapLabel] = None, legend: MapLegend = None, *, interaction_groups: dict[str, Sequence[int | str | MapFeature]] = None) -> None: ...
    @property
    def geojson(self) -> dict: ...
    @geojson.setter
    def geojson(self, value: dict) -> None: ...

class GeoJSONAndDataResult(_ViewResult):
    data: Incomplete
    labels: Incomplete
    legend: Incomplete
    interaction_groups: Incomplete
    def __init__(self, geojson: dict, data: DataGroup, labels: list[MapLabel] = None, legend: MapLegend = None, *, interaction_groups: dict[str, Sequence[int | str | MapFeature]] = None) -> None: ...
    @property
    def geojson(self) -> dict: ...
    @geojson.setter
    def geojson(self, value: dict) -> None: ...

class MapResult(GeoJSONResult):
    def __init__(self, features: list[MapFeature], labels: list[MapLabel] = None, legend: MapLegend = None, *, interaction_groups: dict[str, Sequence[int | str | MapFeature]] = None) -> None: ...
    @property
    def features(self) -> list[MapFeature]: ...
    @features.setter
    def features(self, value: list[MapFeature]) -> None: ...
    @property
    def geojson(self) -> dict: ...
    @geojson.setter
    def geojson(self, value: dict) -> None: ...

class MapAndDataResult(GeoJSONAndDataResult):
    def __init__(self, features: list[MapFeature], data: DataGroup, labels: list[MapLabel] = None, legend: MapLegend = None, *, interaction_groups: dict[str, Sequence[int | str | MapFeature]] = None) -> None: ...
    @property
    def features(self) -> list[MapFeature]: ...
    @features.setter
    def features(self, value: list[MapFeature]) -> None: ...
    @property
    def geojson(self) -> dict: ...
    @geojson.setter
    def geojson(self, value: dict) -> None: ...

class WebResult(_ViewResult):
    html: Incomplete
    url: Incomplete
    def __init__(self, *, html: StringIO | File | str = None, url: str = None) -> None: ...
    @classmethod
    def from_path(cls, file_path: str | bytes | os.PathLike) -> WebResult: ...

class WebAndDataResult(_ViewResult):
    html: Incomplete
    url: Incomplete
    data: Incomplete
    def __init__(self, *, html: StringIO | File | str = None, url: str = None, data: DataGroup = None) -> None: ...

class PlotlyResult(_ViewResult):
    figure: Incomplete
    def __init__(self, figure: str | dict) -> None: ...

class PlotlyAndDataResult(_ViewResult):
    figure: Incomplete
    data: Incomplete
    def __init__(self, figure: str | dict, data: DataGroup) -> None: ...

class PDFResult(_ViewResult):
    file: Incomplete
    url: Incomplete
    def __init__(self, *, file: File = None, url: str = None) -> None: ...
    @classmethod
    def from_path(cls, file_path: str | bytes | os.PathLike) -> PDFResult: ...

class IFCResult(_ViewResult):
    ifc: Incomplete
    def __init__(self, ifc: File | FileResource) -> None: ...

class IFCAndDataResult(_ViewResult):
    ifc: Incomplete
    data: Incomplete
    def __init__(self, ifc: File | FileResource, data: DataGroup) -> None: ...

class TableResult(_ViewResult):
    data: Incomplete
    column_headers: Incomplete
    row_headers: Incomplete
    enable_sorting_and_filtering: Incomplete
    def __init__(self, data: Sequence[Sequence[TableCellValue | TableCell]] | pd.DataFrame | Styler, *, column_headers: Sequence[str | TableHeader] | None = None, row_headers: Sequence[str | TableHeader] | None = None, enable_sorting_and_filtering: bool | None = None) -> None: ...

class SummaryItem:
    def __init__(self, label: str, item_type: type[str | float], source: str, value_path: str, *, suffix: str = '', prefix: str = '') -> None: ...

class Summary(OrderedDict):
    def __init__(self, **items: SummaryItem) -> None: ...

class View(ABC, metaclass=abc.ABCMeta):
    def __init__(self, label: str, duration_guess: int = None, *, description: str = None, update_label: str = None, **kwargs: Any) -> None: ...
    def __call__(self, view_function: Callable) -> Callable: ...

class GeometryView(View):
    def __init__(self, label: str, duration_guess: int = None, *, description: str = None, update_label: str = None, view_mode: Literal['2D', '3D'] = '3D', default_shadow: bool = False, up_axis: Literal['Y', 'Z'] = 'Z', x_axis_to_right: bool = None) -> None: ...

class DataView(View): ...

class GeometryAndDataView(View):
    def __init__(self, label: str, duration_guess: int = None, *, description: str = None, update_label: str = None, view_mode: Literal['2D', '3D'] = '3D', default_shadow: bool = False, up_axis: Literal['Y', 'Z'] = 'Z', x_axis_to_right: bool = None) -> None: ...

class GeoJSONView(View): ...
class GeoJSONAndDataView(View): ...
class MapView(View): ...
class MapAndDataView(View): ...
class ImageView(View): ...
class ImageAndDataView(View): ...
class WebView(View): ...
class WebAndDataView(View): ...
class PlotlyView(View): ...
class PlotlyAndDataView(View): ...
class PDFView(View): ...
class IFCView(View): ...
class IFCAndDataView(View): ...
class TableView(View): ...

class InteractionEvent:
    type: Incomplete
    value: Incomplete
    def __init__(self, event_type: str, value: Any) -> None: ...
