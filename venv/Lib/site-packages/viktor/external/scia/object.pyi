import abc
from _typeshed import Incomplete
from abc import ABC, abstractmethod
from enum import Enum
from typing import Sequence

__all__ = ['ArbitraryProfile', 'ArbitraryProfileSpan', 'AveragingStrip', 'Beam', 'CircularComposedCrossSection', 'CircularCrossSection', 'CircularHollowCrossSection', 'ComposedCrossSection', 'Concrete', 'CrossLink', 'CrossSection', 'FreeLineLoad', 'FreeLoad', 'FreePointLoad', 'FreeSurfaceLoad', 'GeneralCrossSection', 'GeneralCrossSectionElement', 'HingeOnBeam', 'HingeOnPlane', 'IntegrationStrip', 'InternalEdge', 'Layer', 'LibraryCrossSection', 'LineForceSurface', 'LineLoad', 'LineMomentOnBeam', 'LineMomentOnPlane', 'LineSupport', 'LineSupportLine', 'LineSupportSurface', 'LoadCase', 'LoadCombination', 'LoadGroup', 'Material', 'MeshSetup', 'Node', 'NonLinearFunction', 'NonLinearLoadCombination', 'NumericalCrossSection', 'OpenSlab', 'Orthotropy', 'PermanentLoadCase', 'Plane', 'PointLoad', 'PointLoadNode', 'PointMomentNode', 'PointSupport', 'PointSupportLine', 'ProjectData', 'RectangularCrossSection', 'ResultClass', 'RigidArm', 'SciaObject', 'SectionOnBeam', 'SectionOnPlane', 'Selection', 'SolverSetup', 'Subsoil', 'SurfaceLoad', 'SurfaceSupportSurface', 'ThermalLoad', 'ThermalSurfaceLoad', 'VariableLoadCase']

class SciaObject(ABC, metaclass=abc.ABCMeta):
    def __init__(self, object_id: int, name: str) -> None: ...
    @property
    def object_id(self) -> int: ...
    @property
    def name(self) -> str: ...

class Layer(SciaObject):
    def __init__(self, object_id: int, name: str, comment: str = None, structural_model_only: bool = None, current_used_activity: bool = None) -> None: ...

class Material:
    object_id: Incomplete
    name: Incomplete
    def __init__(self, object_id: int, name: str) -> None: ...

class NonLinearFunction(SciaObject):
    class Type(Enum):
        TRANSLATION: NonLinearFunction.Type
        ROTATION: NonLinearFunction.Type
        NONLINEAR_SUBSOIL: NonLinearFunction.Type
    class Support(Enum):
        RIGID: NonLinearFunction.Support
        FREE: NonLinearFunction.Support
        FLEXIBLE: NonLinearFunction.Support
    function_type: Incomplete
    positive_end: Incomplete
    negative_end: Incomplete
    def __init__(self, object_id: int, name: str, function_type: Type, positive_end: Support, negative_end: Support, impulse: list[tuple[float, float]]) -> None: ...
    @property
    def impulse(self) -> list[tuple[float, float]]: ...

class Subsoil(SciaObject):
    class C1z(Enum):
        FLEXIBLE: Subsoil.C1z
        NONLINEAR_FUNCTION: Subsoil.C1z
    c1x: Incomplete
    c1y: Incomplete
    c1z: Incomplete
    stiffness: Incomplete
    c2x: Incomplete
    c2y: Incomplete
    is_drained: Incomplete
    water_air_in_clay_subgrade: Incomplete
    specific_weight: Incomplete
    fi: Incomplete
    sigma_oc: Incomplete
    c: Incomplete
    cu: Incomplete
    def __init__(self, object_id: int, name: str, stiffness: float, c1x: float = None, c1y: float = None, c1z: C1z = None, nonlinear_function: NonLinearFunction = None, c2x: float = None, c2y: float = None, is_drained: bool = None, water_air_in_clay_subgrade: bool = None, specific_weight: float = None, fi: float = None, sigma_oc: float = None, c: float = None, cu: float = None) -> None: ...
    @property
    def nonlinear_function(self) -> NonLinearFunction | None: ...

class Orthotropy(SciaObject):
    class _Type(Enum):
        STANDARD: Orthotropy._Type
    thickness: Incomplete
    D11: Incomplete
    D22: Incomplete
    D12: Incomplete
    D33: Incomplete
    D44: Incomplete
    D55: Incomplete
    d11: Incomplete
    d22: Incomplete
    d12: Incomplete
    d33: Incomplete
    kxy: Incomplete
    kyx: Incomplete
    def __init__(self, object_id: int, name: str, material: Material, thickness: float, D11: float = None, D22: float = None, D12: float = None, D33: float = None, D44: float = None, D55: float = None, d11: float = None, d22: float = None, d12: float = None, d33: float = None, kxy: float = None, kyx: float = None) -> None: ...

class Selection(SciaObject):
    def __init__(self, object_id: int, name: str, objects: list[dict]) -> None: ...

class CrossSection(SciaObject, metaclass=abc.ABCMeta):
    material: Incomplete
    @abstractmethod
    def __init__(self, object_id: int, name: str, material: Material): ...

class RectangularCrossSection(CrossSection):
    width: Incomplete
    height: Incomplete
    def __init__(self, object_id: int, name: str, material: Material, width: float, height: float) -> None: ...

class CircularCrossSection(CrossSection):
    diameter: Incomplete
    def __init__(self, object_id: int, name: str, material: Material, diameter: float) -> None: ...

class CircularHollowCrossSection(CrossSection):
    diameter: Incomplete
    thickness: Incomplete
    def __init__(self, object_id: int, name: str, material: Material, diameter: float, thickness: float) -> None: ...

class ComposedCrossSection(CrossSection, metaclass=abc.ABCMeta):
    material_2: Incomplete
    @abstractmethod
    def __init__(self, object_id: int, name: str, material: Material, material_2: Material): ...

class CircularComposedCrossSection(ComposedCrossSection):
    diameter: Incomplete
    thickness: Incomplete
    def __init__(self, object_id: int, name: str, material: Material, material_2: Material, diameter: float, thickness: float) -> None: ...

class NumericalCrossSection(CrossSection):
    A: Incomplete
    Ay: Incomplete
    Az: Incomplete
    AL: Incomplete
    AD: Incomplete
    cYUCS: Incomplete
    cZUCS: Incomplete
    alpha: Incomplete
    Iy: Incomplete
    Iz: Incomplete
    Wely: Incomplete
    Welz: Incomplete
    Wply: Incomplete
    Wplz: Incomplete
    Mply_plus: Incomplete
    Mply_min: Incomplete
    Mplz_plus: Incomplete
    Mplz_min: Incomplete
    dy: Incomplete
    dz: Incomplete
    It: Incomplete
    Iw: Incomplete
    beta_y: Incomplete
    beta_z: Incomplete
    def __init__(self, object_id: int, name: str, material: Material, *, A: float = None, Ay: float = None, Az: float = None, AL: float = None, AD: float = None, cYUCS: float = None, cZUCS: float = None, alpha: float = None, Iy: float = None, Iz: float = None, Wely: float = None, Welz: float = None, Wply: float = None, Wplz: float = None, Mply_plus: float = None, Mply_min: float = None, Mplz_plus: float = None, Mplz_min: float = None, dy: float = None, dz: float = None, It: float = None, Iw: float = None, beta_y: float = None, beta_z: float = None) -> None: ...

class LibraryCrossSection(CrossSection):
    class Section(Enum):
        I: LibraryCrossSection.Section
        RECTANGULAR_HOLLOW: LibraryCrossSection.Section
        CIRCULAR_HOLLOW: LibraryCrossSection.Section
        L: LibraryCrossSection.Section
        CHANNEL: LibraryCrossSection.Section
        T: LibraryCrossSection.Section
        FULL_RECTANGULAR: LibraryCrossSection.Section
        FULL_CIRCULAR: LibraryCrossSection.Section
        ASYMMETRIC_I: LibraryCrossSection.Section
        ROLLED_Z: LibraryCrossSection.Section
        GENERAL_COLD_FORMED: LibraryCrossSection.Section
        COLD_FORMED_ANGLE: LibraryCrossSection.Section
        COLD_FORMED_CHANNEL: LibraryCrossSection.Section
        COLD_FORMED_Z: LibraryCrossSection.Section
        COLD_FORMED_C: LibraryCrossSection.Section
        COLD_FORMED_OMEGA: LibraryCrossSection.Section
        COLD_FORMED_C_EAVES_BEAM: LibraryCrossSection.Section
        COLD_FORMED_C_PLUS: LibraryCrossSection.Section
        COLD_FORMED_ZED: LibraryCrossSection.Section
        COLD_FORMED_ZED_ASYMMETRIC_LIPS: LibraryCrossSection.Section
        COLD_FORMED_ZED_INCLINED_LIP: LibraryCrossSection.Section
        COLD_FORMED_SIGMA: LibraryCrossSection.Section
        COLD_FORMED_SIGMA_STIFFENED: LibraryCrossSection.Section
        COLD_FORMED_SIGMA_PLUS: LibraryCrossSection.Section
        COLD_FORMED_SIGMA_EAVES_BEAM: LibraryCrossSection.Section
        COLD_FORMED_SIGMA_PLUS_EAVES_BEAM: LibraryCrossSection.Section
        COLD_FORMED_ZED_BOTH_LIPS_INCLINED: LibraryCrossSection.Section
        COLD_FORMED_I_PLUS: LibraryCrossSection.Section
        COLD_FORMED_IS_PLUS: LibraryCrossSection.Section
        COLD_FORMED_SIGMA_ASYMMETRIC: LibraryCrossSection.Section
        COLD_FORMED_2C: LibraryCrossSection.Section
        RAIL_TYPE_KA: LibraryCrossSection.Section
        RAIL_TYPE_KF: LibraryCrossSection.Section
        RAIL_TYPE_KG: LibraryCrossSection.Section
        SFB: LibraryCrossSection.Section
        IFBA: LibraryCrossSection.Section
        IFBB: LibraryCrossSection.Section
        THQ: LibraryCrossSection.Section
        VIRTUAL_JOIST: LibraryCrossSection.Section
        MINUS_L: LibraryCrossSection.Section
    section: Incomplete
    profile: Incomplete
    def __init__(self, object_id: int, name: str, material: Material, section: Section, profile: str) -> None: ...

class GeneralCrossSectionElement:
    class Type(Enum):
        POLYGON: GeneralCrossSectionElement.Type
        OPENING: GeneralCrossSectionElement.Type
    def __init__(self, name: str, element_type: Type, points: Sequence[tuple[float, float]], *, material: Material = None) -> None: ...

class GeneralCrossSection(CrossSection):
    def __init__(self, object_id: int, name: str, material: Material, elements: Sequence[GeneralCrossSectionElement]) -> None: ...

class Node(SciaObject):
    x: Incomplete
    y: Incomplete
    z: Incomplete
    def __init__(self, object_id: int, name: str, x: float, y: float, z: float) -> None: ...

class Beam(SciaObject):
    lcs_rotation: Incomplete
    def __init__(self, object_id: int, name: str, begin_node: Node, end_node: Node, cross_section: CrossSection, ez: float = None, lcs_rotation: float = None, layer: Layer = None) -> None: ...
    @property
    def begin_node(self) -> Node: ...
    @property
    def end_node(self) -> Node: ...
    @property
    def cross_section(self) -> CrossSection: ...
    @property
    def ez(self) -> float: ...

class CrossLink(SciaObject):
    beam_1: Incomplete
    beam_2: Incomplete
    def __init__(self, object_id: int, name: str, beam_1: Beam, beam_2: Beam) -> None: ...

class ArbitraryProfileSpan:
    class TypeOfCss(Enum):
        PRISMATIC: ArbitraryProfileSpan.TypeOfCss
        PARAM_HAUNCH: ArbitraryProfileSpan.TypeOfCss
        TWO_CSS: ArbitraryProfileSpan.TypeOfCss
    class Alignment(Enum):
        DEFAULT: ArbitraryProfileSpan.Alignment
        CENTER_LINE: ArbitraryProfileSpan.Alignment
        TOP_SURFACE: ArbitraryProfileSpan.Alignment
        BOTTOM_SURFACE: ArbitraryProfileSpan.Alignment
        LEFT_SURFACE: ArbitraryProfileSpan.Alignment
        RIGHT_SURFACE: ArbitraryProfileSpan.Alignment
        TOP_LEFT: ArbitraryProfileSpan.Alignment
        TOP_RIGHT: ArbitraryProfileSpan.Alignment
        BOTTOM_LEFT: ArbitraryProfileSpan.Alignment
        BOTTOM_RIGHT: ArbitraryProfileSpan.Alignment
    length: Incomplete
    type_of_css: Incomplete
    alignment: Incomplete
    def __init__(self, length: float, type_of_css: TypeOfCss, cross_section_start: CrossSection, cross_section_end: CrossSection, alignment: Alignment) -> None: ...
    @property
    def cross_section_start(self) -> CrossSection: ...
    @property
    def cross_section_end(self) -> CrossSection: ...

class ArbitraryProfile(SciaObject):
    class CDef(Enum):
        ABSOLUTE: ArbitraryProfile.CDef
        RELATIVE: ArbitraryProfile.CDef
    c_def: Incomplete
    def __init__(self, object_id: int, name: str, beam: Beam, c_def: CDef, cross_section: CrossSection, spans: list[ArbitraryProfileSpan]) -> None: ...
    @property
    def beam(self) -> Beam: ...
    @property
    def cross_section(self) -> CrossSection: ...
    @property
    def spans(self) -> list[ArbitraryProfileSpan]: ...

class HingeOnBeam(SciaObject):
    class Position(Enum):
        BEGIN: HingeOnBeam.Position
        END: HingeOnBeam.Position
        BOTH: HingeOnBeam.Position
    class Freedom(Enum):
        FREE: HingeOnBeam.Freedom
        RIGID: HingeOnBeam.Freedom
        FLEXIBLE: HingeOnBeam.Freedom
    position: Incomplete
    def __init__(self, object_id: int, name: str, beam: Beam, position: Position, freedom_ux: Freedom = ..., freedom_uy: Freedom = ..., freedom_uz: Freedom = ..., freedom_fix: Freedom = ..., freedom_fiy: Freedom = ..., freedom_fiz: Freedom = ..., stiffness_ux: float = 0, stiffness_uy: float = 0, stiffness_uz: float = 0, stiffness_fix: float = 0, stiffness_fiy: float = 0, stiffness_fiz: float = 0) -> None: ...
    @property
    def beam(self) -> Beam: ...
    @property
    def freedom(self) -> tuple['HingeOnBeam.Freedom', 'HingeOnBeam.Freedom', 'HingeOnBeam.Freedom', 'HingeOnBeam.Freedom', 'HingeOnBeam.Freedom', 'HingeOnBeam.Freedom']: ...
    @property
    def stiffness(self) -> tuple[float, float, float, float, float, float]: ...

class HingeOnPlane(SciaObject):
    class CDef(Enum):
        ABSOLUTE: HingeOnPlane.CDef
        RELATIVE: HingeOnPlane.CDef
    class Freedom(Enum):
        FREE: HingeOnPlane.Freedom
        RIGID: HingeOnPlane.Freedom
        FLEXIBLE: HingeOnPlane.Freedom
    class Origin(Enum):
        FROM_START: HingeOnPlane.Origin
        FROM_END: HingeOnPlane.Origin
    def __init__(self, object_id: int, name: str, edge: tuple['Plane', int] | InternalEdge, ux: Freedom = None, stiffness_ux: float = None, uy: Freedom = None, stiffness_uy: float = None, uz: Freedom = None, stiffness_uz: float = None, fix: Freedom = None, stiffness_fix: float = None, c_def: CDef = None, position_x1: float = None, position_x2: float = None, origin: Origin = None) -> None: ...
    @property
    def plane(self) -> Plane: ...

class Plane(SciaObject):
    class FEMModel(Enum):
        ISOTROPIC: Plane.FEMModel
        ORTHOTROPIC: Plane.FEMModel
    class Type(Enum):
        PLATE: Plane.Type
        WALL: Plane.Type
        SHELL: Plane.Type
    material: Incomplete
    plane_type: Incomplete
    thickness: Incomplete
    def __init__(self, object_id: int, name: str, thickness: float, material: Material, *, plane_type: Type = None, layer: Layer = None, corner_nodes: list[Node] = None, internal_nodes: list[Node] = None, swap_orientation: bool = None, lcs_rotation: float = None, fem_model: FEMModel = None, orthotropy: Orthotropy = None, center_node: Node = None, vertex_node: Node = None, axis: tuple[float, float, float] = None) -> None: ...
    @property
    def corner_nodes(self) -> list[Node]: ...
    @property
    def internal_nodes(self) -> list[Node]: ...
    @property
    def swap_orientation(self) -> bool: ...
    @property
    def lcs_rotation(self) -> float: ...

class LineSupport(SciaObject, metaclass=abc.ABCMeta):
    class Constraint(Enum):
        FIXED: LineSupport.Constraint
        HINGED: LineSupport.Constraint
        SLIDING: LineSupport.Constraint
        CUSTOM: LineSupport.Constraint
    class Type(Enum):
        LINE: LineSupport.Type
        FOUNDATION_STRIP: LineSupport.Type
        WALL: LineSupport.Type
    class Freedom(Enum):
        FREE: LineSupport.Freedom
        RIGID: LineSupport.Freedom
        FLEXIBLE: LineSupport.Freedom
        RIGID_PRESS_ONLY: LineSupport.Freedom
        RIGID_TENSION_ONLY: LineSupport.Freedom
        FLEXIBLE_PRESS_ONLY: LineSupport.Freedom
        FLEXIBLE_TENSION_ONLY: LineSupport.Freedom
        NONLINEAR: LineSupport.Freedom
    class CSys(Enum):
        GLOBAL: LineSupport.CSys
        LOCAL: LineSupport.CSys
    class CDef(Enum):
        ABSOLUTE: LineSupport.CDef
        RELATIVE: LineSupport.CDef
    class Extent(Enum):
        FULL: LineSupport.Extent
        SPAN: LineSupport.Extent
    class Origin(Enum):
        FROM_START: LineSupport.Origin
        FROM_END: LineSupport.Origin
    c_sys: Incomplete
    c_def: Incomplete
    position_x1: Incomplete
    position_x2: Incomplete
    origin: Incomplete
    @abstractmethod
    def __init__(self, object_id: int, name: str, x: Freedom = None, stiffness_x: float = None, function_x: NonLinearFunction = None, y: Freedom = None, stiffness_y: float = None, function_y: NonLinearFunction = None, z: Freedom = None, stiffness_z: float = None, function_z: NonLinearFunction = None, rx: Freedom = None, stiffness_rx: float = None, function_rx: NonLinearFunction = None, ry: Freedom = None, stiffness_ry: float = None, function_ry: NonLinearFunction = None, rz: Freedom = None, stiffness_rz: float = None, function_rz: NonLinearFunction = None, c_sys: CSys = None, c_def: CDef = None, position_x1: float = None, position_x2: float = None, origin: Origin = None): ...
    @property
    def constraint(self) -> LineSupport.Constraint: ...
    @property
    def freedom(self) -> tuple['LineSupport.Freedom', 'LineSupport.Freedom', 'LineSupport.Freedom', 'LineSupport.Freedom', 'LineSupport.Freedom', 'LineSupport.Freedom']: ...
    @property
    def stiffness(self) -> tuple[float | None, float | None, float | None, float | None, float | None, float | None]: ...
    @property
    def function_x(self) -> NonLinearFunction | None: ...
    @property
    def function_y(self) -> NonLinearFunction | None: ...
    @property
    def function_z(self) -> NonLinearFunction | None: ...
    @property
    def function_rx(self) -> NonLinearFunction | None: ...
    @property
    def function_ry(self) -> NonLinearFunction | None: ...
    @property
    def function_rz(self) -> NonLinearFunction | None: ...

class LineSupportLine(LineSupport):
    extent: Incomplete
    def __init__(self, object_id: int, name: str, beam: Beam, x: LineSupport.Freedom = None, stiffness_x: float = None, function_x: NonLinearFunction = None, y: LineSupport.Freedom = None, stiffness_y: float = None, function_y: NonLinearFunction = None, z: LineSupport.Freedom = None, stiffness_z: float = None, function_z: NonLinearFunction = None, rx: LineSupport.Freedom = None, stiffness_rx: float = None, function_rx: NonLinearFunction = None, ry: LineSupport.Freedom = None, stiffness_ry: float = None, function_ry: NonLinearFunction = None, rz: LineSupport.Freedom = None, stiffness_rz: float = None, function_rz: NonLinearFunction = None, c_sys: LineSupport.CSys = None, extent: LineSupport.Extent = None, c_def: LineSupport.CDef = None, position_x1: float = None, position_x2: float = None, origin: LineSupport.Origin = None) -> None: ...
    @property
    def beam(self) -> Beam: ...
    @property
    def spring_type(self) -> LineSupport.Type: ...

class LineSupportSurface(LineSupport):
    def __init__(self, object_id: int, name: str, edge: tuple[Plane, int] | InternalEdge, x: LineSupport.Freedom = None, stiffness_x: float = None, y: LineSupport.Freedom = None, stiffness_y: float = None, z: LineSupport.Freedom = None, stiffness_z: float = None, rx: LineSupport.Freedom = None, stiffness_rx: float = None, ry: LineSupport.Freedom = None, stiffness_ry: float = None, rz: LineSupport.Freedom = None, stiffness_rz: float = None, c_sys: LineSupport.CSys = None, c_def: LineSupport.CDef = None, position_x1: float = None, position_x2: float = None, origin: LineSupport.Origin = None) -> None: ...
    @property
    def plane(self) -> Plane: ...

class SurfaceSupportSurface(SciaObject):
    def __init__(self, object_id: int, name: str, plane: Plane, subsoil: Subsoil) -> None: ...
    @property
    def plane(self) -> Plane: ...
    @property
    def subsoil(self) -> Subsoil: ...

class OpenSlab(SciaObject):
    def __init__(self, object_id: int, name: str, plane: Plane, corner_nodes: list[Node]) -> None: ...
    @property
    def plane(self) -> Plane: ...
    @property
    def corner_nodes(self) -> list[Node]: ...

class InternalEdge(SciaObject):
    def __init__(self, object_id: int, name: str, plane: Plane, node_1: Node, node_2: Node) -> None: ...
    @property
    def plane(self) -> Plane: ...
    @property
    def node_1(self) -> Node: ...
    @property
    def node_2(self) -> Node: ...

class PointSupport(SciaObject):
    class Constraint(Enum):
        FIXED: PointSupport.Constraint
        HINGED: PointSupport.Constraint
        SLIDING: PointSupport.Constraint
        CUSTOM: PointSupport.Constraint
    class Type(Enum):
        STANDARD: PointSupport.Type
        PAD_FOUNDATION: PointSupport.Type
        COLUMN: PointSupport.Type
    class Freedom(Enum):
        FREE: PointSupport.Freedom
        RIGID: PointSupport.Freedom
        FLEXIBLE: PointSupport.Freedom
    class CSys(Enum):
        GLOBAL: PointSupport.CSys
        LOCAL: PointSupport.CSys
    spring_type: Incomplete
    freedom: Incomplete
    stiffness: Incomplete
    default_size: Incomplete
    c_sys: Incomplete
    def __init__(self, object_id: int, name: str, node: Node, spring_type: Type, freedom: tuple[Freedom, Freedom, Freedom, Freedom, Freedom, Freedom], stiffness: tuple[float, float, float, float, float, float], c_sys: CSys, default_size: float = 0.2, angle: tuple[float, float, float] = None) -> None: ...
    @property
    def node(self) -> Node: ...
    @property
    def constraint(self) -> PointSupport.Constraint: ...

class PointSupportLine(SciaObject):
    class Freedom(Enum):
        FREE: PointSupportLine.Freedom
        RIGID: PointSupportLine.Freedom
        FLEXIBLE: PointSupportLine.Freedom
    class CSys(Enum):
        GLOBAL: PointSupportLine.CSys
        LOCAL: PointSupportLine.CSys
    class CDef(Enum):
        ABSOLUTE: PointSupportLine.CDef
        RELATIVE: PointSupportLine.CDef
    class Origin(Enum):
        FROM_START: PointSupportLine.Origin
        FROM_END: PointSupportLine.Origin
    def __init__(self, object_id: int, name: str, beam: Beam, x: PointSupportLine.Freedom = None, stiffness_x: float = None, y: PointSupportLine.Freedom = None, stiffness_y: float = None, z: PointSupportLine.Freedom = None, stiffness_z: float = None, rx: PointSupportLine.Freedom = None, stiffness_rx: float = None, ry: PointSupportLine.Freedom = None, stiffness_ry: float = None, rz: PointSupportLine.Freedom = None, stiffness_rz: float = None, default_size: float = None, c_sys: PointSupportLine.CSys = None, c_def: PointSupportLine.CDef = None, position_x: float = None, origin: PointSupportLine.Origin = None, repeat: int = None, delta_x: float = None) -> None: ...

class RigidArm(SciaObject):
    hinge_on_master: Incomplete
    hinge_on_slave: Incomplete
    def __init__(self, object_id: int, name: str, master_node: Node, slave_node: Node, hinge_on_master: bool, hinge_on_slave: bool) -> None: ...
    @property
    def master_node(self) -> Node: ...
    @property
    def slave_node(self) -> Node: ...

class SectionOnBeam(SciaObject):
    class CDef(Enum):
        ABSOLUTE: SectionOnBeam.CDef
        RELATIVE: SectionOnBeam.CDef
    class Origin(Enum):
        FROM_START: SectionOnBeam.Origin
        FROM_END: SectionOnBeam.Origin
    c_def: Incomplete
    position_x: Incomplete
    origin: Incomplete
    repeat: Incomplete
    delta_x: Incomplete
    def __init__(self, object_id: int, name: str, beam: Beam, c_def: CDef, position_x: float, origin: Origin, repeat: int, delta_x: float) -> None: ...
    @property
    def beam(self) -> Beam: ...

class LoadGroup(SciaObject):
    class LoadOption(Enum):
        PERMANENT: LoadGroup.LoadOption
        VARIABLE: LoadGroup.LoadOption
        ACCIDENTAL: LoadGroup.LoadOption
        SEISMIC: LoadGroup.LoadOption
    class RelationOption(Enum):
        STANDARD: LoadGroup.RelationOption
        EXCLUSIVE: LoadGroup.RelationOption
        TOGETHER: LoadGroup.RelationOption
    class LoadTypeOption(Enum):
        CAT_A: LoadGroup.LoadTypeOption
        CAT_B: LoadGroup.LoadTypeOption
        CAT_C: LoadGroup.LoadTypeOption
        CAT_D: LoadGroup.LoadTypeOption
        CAT_E: LoadGroup.LoadTypeOption
        CAT_F: LoadGroup.LoadTypeOption
        CAT_G: LoadGroup.LoadTypeOption
        CAT_H: LoadGroup.LoadTypeOption
        SNOW: LoadGroup.LoadTypeOption
        WIND: LoadGroup.LoadTypeOption
        TEMPERATURE: LoadGroup.LoadTypeOption
        RAIN_WATER: LoadGroup.LoadTypeOption
        CONSTRUCTION_LOADS: LoadGroup.LoadTypeOption
    load_option: Incomplete
    def __init__(self, object_id: int, name: str, load_option: LoadOption, relation: RelationOption = None, load_type: LoadTypeOption = None) -> None: ...
    @property
    def relation(self) -> LoadGroup.RelationOption | None: ...
    @property
    def load_type(self) -> LoadGroup.LoadTypeOption | None: ...

class LoadCase(SciaObject, metaclass=abc.ABCMeta):
    class ActionType(Enum):
        PERMANENT: LoadCase.ActionType
        VARIABLE: LoadCase.ActionType
    class PermanentLoadType(Enum):
        SELF_WEIGHT: LoadCase.PermanentLoadType
        STANDARD: LoadCase.PermanentLoadType
        PRIMARY_EFFECT: LoadCase.PermanentLoadType
    class VariableLoadType(Enum):
        STATIC: LoadCase.VariableLoadType
        PRIMARY_EFFECT: LoadCase.VariableLoadType
    class Specification(Enum):
        STANDARD: LoadCase.Specification
        TEMPERATURE: LoadCase.Specification
        STATIC_WIND: LoadCase.Specification
        EARTHQUAKE: LoadCase.Specification
        SNOW: LoadCase.Specification
    class Duration(Enum):
        LONG: LoadCase.Duration
        MEDIUM: LoadCase.Duration
        SHORT: LoadCase.Duration
        INSTANTANEOUS: LoadCase.Duration
    class Direction(Enum):
        NEG_Z: LoadCase.Direction
        POS_Z: LoadCase.Direction
        NEG_Y: LoadCase.Direction
        POS_Y: LoadCase.Direction
        NEG_X: LoadCase.Direction
        POS_X: LoadCase.Direction
    description: Incomplete
    action_type: Incomplete
    @abstractmethod
    def __init__(self, object_id: int, name: str, description: str, action_type: ActionType, load_group: LoadGroup): ...
    @property
    def load_group(self) -> LoadGroup: ...
    @property
    @abstractmethod
    def load_type(self) -> LoadCase.PermanentLoadType | LoadCase.VariableLoadType: ...
    @property
    @abstractmethod
    def direction(self) -> LoadCase.Direction | None: ...
    @property
    @abstractmethod
    def specification(self) -> LoadCase.Specification | None: ...
    @property
    @abstractmethod
    def duration(self) -> LoadCase.Duration | None: ...
    @property
    @abstractmethod
    def master(self) -> str | None: ...
    @property
    @abstractmethod
    def primary_effect(self) -> LoadCase | None: ...

class PermanentLoadCase(LoadCase):
    def __init__(self, object_id: int, name: str, description: str, load_group: LoadGroup, load_type: LoadCase.PermanentLoadType, direction: LoadCase.Direction = None, primary_effect: LoadCase = None) -> None: ...
    @property
    def load_type(self) -> LoadCase.PermanentLoadType: ...
    @property
    def direction(self) -> LoadCase.Direction | None: ...
    @property
    def specification(self) -> None: ...
    @property
    def duration(self) -> None: ...
    @property
    def master(self) -> None: ...
    @property
    def primary_effect(self) -> LoadCase | None: ...

class VariableLoadCase(LoadCase):
    def __init__(self, object_id: int, name: str, description: str, load_group: LoadGroup, load_type: LoadCase.VariableLoadType, specification: LoadCase.Specification = None, duration: LoadCase.Duration = None, primary_effect: LoadCase = None, master: str = None) -> None: ...
    @property
    def load_type(self) -> LoadCase.VariableLoadType: ...
    @property
    def master(self) -> str | None: ...
    @property
    def specification(self) -> LoadCase.Specification | None: ...
    @property
    def duration(self) -> LoadCase.Duration | None: ...
    @property
    def direction(self) -> None: ...
    @property
    def primary_effect(self) -> LoadCase | None: ...

class LoadCombination(SciaObject):
    class Type(Enum):
        ENVELOPE_ULTIMATE: LoadCombination.Type
        ENVELOPE_SERVICEABILITY: LoadCombination.Type
        LINEAR_ULTIMATE: LoadCombination.Type
        LINEAR_SERVICEABILITY: LoadCombination.Type
        EN_ULS_SET_B: LoadCombination.Type
        EN_ACC_ONE: LoadCombination.Type
        EN_ACC_TWO: LoadCombination.Type
        EN_SEISMIC: LoadCombination.Type
        EN_SLS_CHAR: LoadCombination.Type
        EN_SLS_FREQ: LoadCombination.Type
        EN_SLS_QUASI: LoadCombination.Type
        EN_ULS_SET_C: LoadCombination.Type
    combination_type: Incomplete
    def __init__(self, object_id: int, name: str, combination_type: Type, load_cases: dict[LoadCase, float], *, description: str = None) -> None: ...
    @property
    def load_cases(self) -> dict[LoadCase, float]: ...

class NonLinearLoadCombination(SciaObject):
    class Type(Enum):
        ULTIMATE: NonLinearLoadCombination.Type
        SERVICEABILITY: NonLinearLoadCombination.Type
    combination_type: Incomplete
    def __init__(self, object_id: int, name: str, combination_type: Type, load_cases: dict[LoadCase, float], *, description: str = None) -> None: ...
    @property
    def load_cases(self) -> dict[LoadCase, float]: ...

class ResultClass(SciaObject):
    def __init__(self, object_id: int, name: str, combinations: list[LoadCombination], nonlinear_combinations: list[NonLinearLoadCombination]) -> None: ...
    @property
    def combinations(self) -> list[LoadCombination]: ...
    @property
    def nonlinear_combinations(self) -> list[NonLinearLoadCombination]: ...

class IntegrationStrip(SciaObject):
    class _EffectiveWidthGeometry(Enum):
        CONSTANT_SYMMETRIC: IntegrationStrip._EffectiveWidthGeometry
        CONSTANT_ASYMMETRIC: IntegrationStrip._EffectiveWidthGeometry
    class _EffectiveWidthDefinition(Enum):
        WIDTH: IntegrationStrip._EffectiveWidthDefinition
        NUMBER_OF_THICKNESS: IntegrationStrip._EffectiveWidthDefinition
    point_1: Incomplete
    point_2: Incomplete
    width: Incomplete
    def __init__(self, object_id: int, name: str, plane: Plane, point_1: tuple[float, float, float], point_2: tuple[float, float, float], width: float, effective_width_geometry: _EffectiveWidthGeometry = ..., effective_width_definition: _EffectiveWidthDefinition = ...) -> None: ...
    @property
    def plane(self) -> Plane: ...

class AveragingStrip(SciaObject):
    class Type(Enum):
        POINT: AveragingStrip.POINT
    class Direction(Enum):
        LONGITUDINAL: AveragingStrip.Direction
        PERPENDICULAR: AveragingStrip.Direction
        BOTH: AveragingStrip.Direction
        NONE: AveragingStrip.Direction
    point_1: Incomplete
    width: Incomplete
    length: Incomplete
    angle: Incomplete
    direction: Incomplete
    def __init__(self, object_id: int, name: str, plane: Plane, strip_type: Type, point_1: tuple[float, float, float], width: float, length: float, angle: float, direction: Direction) -> None: ...
    @property
    def plane(self) -> Plane: ...

class SectionOnPlane(SciaObject):
    class Draw(Enum):
        UPRIGHT_TO_ELEMENT: SectionOnPlane.Draw
        ELEMENT_PLANE: SectionOnPlane.Draw
        X_DIRECTION: SectionOnPlane.Draw
        Y_DIRECTION: SectionOnPlane.Draw
        Z_DIRECTION: SectionOnPlane.Draw
    point_1: Incomplete
    point_2: Incomplete
    def __init__(self, object_id: int, name: str, point_1: tuple[float, float, float], point_2: tuple[float, float, float], draw: SectionOnPlane.Draw = None, direction_of_cut: tuple[float, float, float] = None) -> None: ...

class ProjectData(SciaObject):
    name_: Incomplete
    part: Incomplete
    description: Incomplete
    author: Incomplete
    date: Incomplete
    def __init__(self, *, name: str = None, part: str = None, description: str = None, author: str = None, date: str = None) -> None: ...

class MeshSetup(SciaObject):
    average_1d: Incomplete
    average_2d: Incomplete
    division_2d_1d: Incomplete
    def __init__(self, *, average_1d: float = 1.0, average_2d: float = 1.0, division_2d_1d: int = 50) -> None: ...

class SolverSetup(SciaObject):
    neglect_shear_force_deformation: Incomplete
    bending_theory: Incomplete
    solver_type: Incomplete
    number_of_sections: Incomplete
    reinforcement_coefficient: Incomplete
    def __init__(self, *, neglect_shear_force_deformation: bool = None, bending_theory: str = None, solver_type: str = None, number_of_sections: float = None, reinforcement_coefficient: float = None) -> None: ...

class Concrete(SciaObject):
    class ECPart(Enum):
        GENERAL: Concrete.ECPart
        BRIDGES: Concrete.ECPart
    thermal_expansion: Incomplete
    unit_mass: Incomplete
    wet_density: Incomplete
    e_modulus: Incomplete
    poisson: Incomplete
    g_modulus: Incomplete
    log_decrement: Incomplete
    specific_heat: Incomplete
    thermal_conductivity: Incomplete
    fck: Incomplete
    def __init__(self, object_id: int, name: str, part: ECPart, thermal_expansion: float = None, unit_mass: float = None, wet_density: float = None, e_modulus: float = None, poisson: float = None, g_modulus: float = None, log_decrement: float = None, specific_heat: float = None, thermal_conductivity: float = None, *, fck: float = None) -> None: ...
    @property
    def ec_part(self) -> Concrete.ECPart: ...

class FreeLoad(SciaObject, metaclass=abc.ABCMeta):
    class Direction(Enum):
        X: FreeLoad.Direction
        Y: FreeLoad.Direction
        Z: FreeLoad.Direction
    class Select(Enum):
        AUTO: FreeLoad.Select
        SELECT: FreeLoad.Select
    class Type(Enum):
        FORCE: FreeLoad.Type
    class Validity(Enum):
        ALL: FreeLoad.Validity
        NEG_Z: FreeLoad.Validity
        POS_Z: FreeLoad.Validity
        FROM_TO: FreeLoad.Validity
        ZERO_Z: FreeLoad.Validity
        NEG_Z_INCL_ZERO: FreeLoad.Validity
        POS_Z_INCL_ZERO: FreeLoad.Validity
    class CSys(Enum):
        GLOBAL: FreeLoad.CSys
        MEMBER_LCS: FreeLoad.CSys
        LOAD_LCS: FreeLoad.CSys
    class Location(Enum):
        LENGTH: FreeLoad.Location
        PROJECTION: FreeLoad.Location
    direction: Incomplete
    @abstractmethod
    def __init__(self, object_id: int, name: str, load_case: LoadCase, direction: Direction, select: Select, validity: Validity = None, load_type: Type = None, c_sys: CSys = None): ...
    @property
    def load_case(self) -> LoadCase: ...

class FreeLineLoad(FreeLoad):
    class Distribution(Enum):
        UNIFORM: FreeLineLoad.Distribution
        TRAPEZOIDAL: FreeLineLoad.Distribution
    point_1: Incomplete
    point_2: Incomplete
    magnitude_1: Incomplete
    magnitude_2: Incomplete
    def __init__(self, object_id: int, name: str, load_case: LoadCase, point_1: tuple[float, float], point_2: tuple[float, float], direction: FreeLoad.Direction, magnitude_1: float, magnitude_2: float, distribution: Distribution = ..., validity: FreeLoad.Validity = ..., load_type: FreeLoad.Type = ..., select: FreeLoad.Select = ..., system: FreeLoad.CSys = ..., location: FreeLoad.Location = ...) -> None: ...

class FreePointLoad(FreeLoad):
    magnitude: Incomplete
    position: Incomplete
    def __init__(self, object_id: int, name: str, load_case: LoadCase, direction: FreeLoad.Direction, magnitude: float, position: tuple[float, float], load_type: FreeLoad.Type = ..., validity: FreeLoad.Validity = ..., select: FreeLoad.Select = ..., system: FreeLoad.CSys = ...) -> None: ...

class FreeSurfaceLoad(FreeLoad):
    class Distribution(Enum):
        UNIFORM: FreeSurfaceLoad.Distribution
        DIR_X: FreeSurfaceLoad.Distribution
        DIR_Y: FreeSurfaceLoad.Distribution
        POINTS: FreeSurfaceLoad.Distribution
    q1: Incomplete
    def __init__(self, object_id: int, name: str, load_case: LoadCase, direction: FreeLoad.Direction, q1: float, q2: float = None, q3: float = None, points: list[tuple[float, float]] = None, distribution: Distribution = None, load_type: FreeLoad.Type = None, validity: FreeLoad.Validity = None, system: FreeLoad.CSys = None, location: FreeLoad.Location = None, selection: list[Plane] = None) -> None: ...
    @property
    def q2(self) -> float | None: ...
    @property
    def q3(self) -> float | None: ...
    @property
    def points(self) -> list[tuple[float, float]] | None: ...
    @property
    def distribution(self) -> FreeSurfaceLoad.Distribution: ...
    @property
    def selection(self) -> list[Plane] | None: ...

class LineLoad(SciaObject):
    class CSys(Enum):
        GLOBAL: LineLoad.CSys
        LOCAL: LineLoad.CSys
    class CDef(Enum):
        ABSOLUTE: LineLoad.CDef
        RELATIVE: LineLoad.CDef
    class Direction(Enum):
        X: LineLoad.Direction
        Y: LineLoad.Direction
        Z: LineLoad.Direction
    class Distribution(Enum):
        UNIFORM: LineLoad.Distribution
        TRAPEZOIDAL: LineLoad.Distribution
    class Origin(Enum):
        FROM_START: LineLoad.Origin
        FROM_END: LineLoad.Origin
    class Type(Enum):
        FORCE: LineLoad.Type
        SELF_WEIGHT: LineLoad.Type
    load_type: Incomplete
    distribution: Incomplete
    load_start: Incomplete
    load_end: Incomplete
    direction: Incomplete
    c_sys: Incomplete
    position_start: Incomplete
    position_end: Incomplete
    c_def: Incomplete
    origin: Incomplete
    ey: Incomplete
    ez: Incomplete
    def __init__(self, object_id: int, name: str, load_case: LoadCase, beam: Beam, load_type: Type, distribution: Distribution, load_start: float, load_end: float, direction: Direction, c_sys: CSys, position_start: float, position_end: float, c_def: CDef, origin: Origin, ey: float, ez: float) -> None: ...
    @property
    def beam(self) -> Beam: ...
    @property
    def load_case(self) -> LoadCase: ...

class LineMomentOnBeam(SciaObject):
    class CDef(Enum):
        ABSOLUTE: LineMomentOnBeam.CDef
        RELATIVE: LineMomentOnBeam.CDef
    class Direction(Enum):
        X: LineMomentOnBeam.Direction
        Y: LineMomentOnBeam.Direction
        Z: LineMomentOnBeam.Direction
    class Origin(Enum):
        FROM_START: LineMomentOnBeam.Origin
        FROM_END: LineMomentOnBeam.Origin
    m1: Incomplete
    m2: Incomplete
    def __init__(self, object_id: int, name: str, beam: Beam, load_case: LoadCase, m1: float, m2: float = None, direction: Direction = None, c_def: CDef = None, position_x1: float = None, position_x2: float = None, origin: Origin = None) -> None: ...

class LineMomentOnPlane(SciaObject):
    class CDef(Enum):
        ABSOLUTE: LineMomentOnPlane.CDef
        RELATIVE: LineMomentOnPlane.CDef
    class Direction(Enum):
        X: LineMomentOnPlane.Direction
        Y: LineMomentOnPlane.Direction
        Z: LineMomentOnPlane.Direction
    class Origin(Enum):
        FROM_START: LineMomentOnPlane.Origin
        FROM_END: LineMomentOnPlane.Origin
    m1: Incomplete
    m2: Incomplete
    def __init__(self, object_id: int, name: str, edge: tuple[Plane, int] | InternalEdge, load_case: LoadCase, m1: float, m2: float = None, direction: Direction = None, c_def: CDef = None, position_x1: float = None, position_x2: float = None, origin: Origin = None) -> None: ...
    @property
    def plane(self) -> Plane: ...

class LineForceSurface(SciaObject):
    class CSys(Enum):
        GLOBAL: LineForceSurface.CSys
        LOCAL: LineForceSurface.CSys
    class Direction(Enum):
        X: LineForceSurface.Direction
        Y: LineForceSurface.Direction
        Z: LineForceSurface.Direction
    class Distribution(Enum):
        UNIFORM: LineForceSurface.Distribution
        TRAPEZOIDAL: LineForceSurface.Distribution
    class Location(Enum):
        LENGTH: LineForceSurface.Location
        PROJECTION: LineForceSurface.Location
    class CDef(Enum):
        ABSOLUTE: LineForceSurface.CDef
        RELATIVE: LineForceSurface.CDef
    class Origin(Enum):
        FROM_START: LineForceSurface.Origin
        FROM_END: LineForceSurface.Origin
    direction: Incomplete
    p1: Incomplete
    p2: Incomplete
    def __init__(self, object_id: int, name: str, edge: tuple['Plane', int] | InternalEdge, load_case: LoadCase, p1: float, p2: float = None, direction: Direction = None, location: Location = None, c_sys: CSys = None, c_def: CDef = None, position_x1: float = None, position_x2: float = None, origin: Origin = None) -> None: ...
    @property
    def plane(self) -> Plane: ...
    @property
    def load_case(self) -> LoadCase: ...
    @property
    def c_sys(self) -> LineForceSurface.CSys: ...
    @property
    def location(self) -> LineForceSurface.Location: ...
    @property
    def distribution(self) -> LineForceSurface.Distribution: ...
    @property
    def c_def(self) -> LineForceSurface.CDef: ...
    @property
    def position_x1(self) -> float | None: ...
    @property
    def position_x2(self) -> float | None: ...
    @property
    def origin(self) -> LineForceSurface.Origin: ...

class PointLoadNode(SciaObject):
    class CSys(Enum):
        GLOBAL: PointLoadNode.CSys
        LOCAL: PointLoadNode.CSys
    class Direction(Enum):
        X: PointLoadNode.Direction
        Y: PointLoadNode.Direction
        Z: PointLoadNode.Direction
    load: Incomplete
    direction: Incomplete
    c_sys: Incomplete
    angle: Incomplete
    def __init__(self, object_id: int, name: str, node: Node, load_case: LoadCase, load: float, direction: Direction = None, c_sys: CSys = None, angle: tuple[float, float, float] = None) -> None: ...
    @property
    def node(self) -> Node: ...
    @property
    def load_case(self) -> LoadCase: ...

class PointLoad(SciaObject):
    class CSys(Enum):
        GLOBAL: PointLoad.CSys
        LOCAL: PointLoad.CSys
    class CDef(Enum):
        ABSOLUTE: PointLoad.CDef
        RELATIVE: PointLoad.CDef
    class Direction(Enum):
        X: PointLoad.Direction
        Y: PointLoad.Direction
        Z: PointLoad.Direction
    class Distribution(Enum):
        UNIFORM: PointLoad.Distribution
        TRAPEZOIDAL: PointLoad.Distribution
    class Origin(Enum):
        FROM_START: PointLoad.Origin
        FROM_END: PointLoad.Origin
    class Type(Enum):
        FORCE: PointLoad.Type
    direction: Incomplete
    load_type: Incomplete
    load_value: Incomplete
    c_sys: Incomplete
    c_def: Incomplete
    position_x: Incomplete
    origin: Incomplete
    repeat: Incomplete
    ey: Incomplete
    ez: Incomplete
    angle: Incomplete
    def __init__(self, object_id: int, name: str, load_case: LoadCase, beam: Beam, direction: Direction, load_type: Type, load_value: float, c_sys: CSys = None, c_def: CDef = None, position_x: float = None, origin: Origin = None, repeat: int = None, ey: float = None, ez: float = None, *, angle: tuple[float, float, float] = None) -> None: ...
    @property
    def beam(self) -> Beam: ...
    @property
    def load_case(self) -> LoadCase: ...

class PointMomentNode(SciaObject):
    class CSys(Enum):
        GLOBAL: PointMomentNode.CSys
        LOCAL: PointMomentNode.CSys
    class Direction(Enum):
        X: PointMomentNode.Direction
        Y: PointMomentNode.Direction
        Z: PointMomentNode.Direction
    load: Incomplete
    direction: Incomplete
    c_sys: Incomplete
    def __init__(self, object_id: int, name: str, node: Node, load_case: LoadCase, load: float, direction: Direction, c_sys: CSys) -> None: ...
    @property
    def node(self) -> Node: ...
    @property
    def load_case(self) -> LoadCase: ...

class SurfaceLoad(SciaObject):
    class Direction(Enum):
        X: SurfaceLoad.Direction
        Y: SurfaceLoad.Direction
        Z: SurfaceLoad.Direction
    class Type(Enum):
        FORCE: SurfaceLoad.Type
        SELF_WEIGHT: SurfaceLoad.Type
    class CSys(Enum):
        GLOBAL: SurfaceLoad.CSys
        LOCAL: SurfaceLoad.CSys
    class Location(Enum):
        LENGTH: SurfaceLoad.Location
        PROJECTION: SurfaceLoad.Location
    direction: Incomplete
    load_type: Incomplete
    load_value: Incomplete
    c_sys: Incomplete
    location: Incomplete
    def __init__(self, object_id: int, name: str, load_case: LoadCase, plane: Plane, direction: Direction, load_type: Type, load_value: float, c_sys: CSys, location: Location) -> None: ...
    @property
    def plane(self) -> Plane: ...
    @property
    def load_case(self) -> LoadCase: ...

class ThermalLoad(SciaObject):
    class Distribution(Enum):
        CONSTANT: ThermalLoad.Distribution
        LINEAR: ThermalLoad.Distribution
    class CDef(Enum):
        ABSOLUTE: ThermalLoad.CDef
        RELATIVE: ThermalLoad.CDef
    class Origin(Enum):
        FROM_START: ThermalLoad.Origin
        FROM_END: ThermalLoad.Origin
    distribution: Incomplete
    delta: Incomplete
    left_delta: Incomplete
    right_delta: Incomplete
    top_delta: Incomplete
    bottom_delta: Incomplete
    c_def: Incomplete
    position_start: Incomplete
    position_end: Incomplete
    origin: Incomplete
    def __init__(self, object_id: int, name: str, load_case: LoadCase, beam: Beam, distribution: Distribution, delta: float, left_delta: float, right_delta: float, top_delta: float, bottom_delta: float, position_start: float, position_end: float, c_def: CDef, origin: Origin) -> None: ...
    @property
    def beam(self) -> Beam: ...
    @property
    def load_case(self) -> LoadCase: ...

class ThermalSurfaceLoad(SciaObject):
    class Distribution(Enum):
        CONSTANT: ThermalSurfaceLoad.Distribution
        LINEAR: ThermalSurfaceLoad.Distribution
    delta: Incomplete
    top_delta: Incomplete
    bottom_delta: Incomplete
    def __init__(self, object_id: int, name: str, load_case: LoadCase, plane: Plane, delta: float = None, top_delta: float = None, bottom_delta: float = None) -> None: ...
