import abc
import datetime
from _typeshed import Incomplete
from abc import ABC, abstractmethod
from enum import Enum
from typing import Any, Literal, Sequence

__all__ = ['BarSurface', 'CalculationSetup', 'CheckMember', 'CheckMember1D', 'CheckSection', 'CheckSectionExtreme', 'CodeSettings', 'ConcAggregateType', 'ConcCementClass', 'ConcDependentParams', 'ConcDiagramType', 'ConcreteMaterial', 'ConcreteMemberDataEc2', 'CrossSection', 'CrossSectionComponent', 'CrossSectionParameter', 'CrossSectionType', 'EvaluationInteractionDiagram', 'ExposureClassEc2Carbonation', 'ExposureClassEc2ChemicalAttack', 'ExposureClassEc2Chlorides', 'ExposureClassEc2ChloridesFromSea', 'ExposureClassEc2FreezeAttack', 'ExposureClassesDataEc2', 'FatigueLoading', 'LoadingSLS', 'LoadingULS', 'MatConcrete', 'MatConcreteEc2', 'MatReinforcement', 'MatReinforcementEc2', 'MemberType', 'NationalAnnex', 'NoResistanceConcreteTension1d', 'ProjectData', 'ReinfClass', 'ReinfDiagramType', 'ReinfFabrication', 'ReinfType', 'ReinforcedBar', 'ReinforcedCrossSection', 'ReinforcementMaterial', 'ResultOfInternalForces', 'StandardCheckSection', 'StandardCheckSectionExtreme', 'Stirrup', 'ThermalState', 'ThermalStateType', 'TwoWaySlabType', 'TypeSLSCalculation']

class ConcreteMaterial(Enum):
    C12_15: ConcreteMaterial
    C16_20: ConcreteMaterial
    C20_25: ConcreteMaterial
    C25_30: ConcreteMaterial
    C30_37: ConcreteMaterial
    C35_45: ConcreteMaterial
    C40_50: ConcreteMaterial
    C45_55: ConcreteMaterial
    C50_60: ConcreteMaterial
    C55_67: ConcreteMaterial
    C60_75: ConcreteMaterial
    C70_85: ConcreteMaterial
    C80_95: ConcreteMaterial
    C90_105: ConcreteMaterial
    C100_115: ConcreteMaterial

class ReinforcementMaterial(Enum):
    B_400A: ReinforcementMaterial
    B_500A: ReinforcementMaterial
    B_600A: ReinforcementMaterial
    B_400B: ReinforcementMaterial
    B_500B: ReinforcementMaterial
    B_600B: ReinforcementMaterial
    B_400C: ReinforcementMaterial
    B_500C: ReinforcementMaterial
    B_600C: ReinforcementMaterial
    B_550A: ReinforcementMaterial
    B_550B: ReinforcementMaterial

class _OpenObject(ABC, metaclass=abc.ABCMeta):
    @abstractmethod
    def __init__(self): ...

class _OpenElementId(ABC):
    def __init__(self, id_: int) -> None: ...
    @property
    def id(self) -> int: ...

class _ReferenceElement:
    def __init__(self, id_: int, type_name: str) -> None: ...
    @property
    def id(self) -> int: ...

class NationalAnnex(Enum):
    NO_ANNEX: NationalAnnex
    DUTCH: NationalAnnex
    BELGIUM: NationalAnnex

class ProjectData(_OpenObject):
    national_annex: Incomplete
    fatigue_check: Incomplete
    name: Incomplete
    number: Incomplete
    description: Incomplete
    author: Incomplete
    date: Incomplete
    design_working_life: Incomplete
    def __init__(self, *, national_annex: NationalAnnex = None, fatigue_check: bool = False, name: str = None, number: str = None, description: str = None, author: str = None, date: datetime.date = None, design_working_life: Literal[50, 75, 100] = None) -> None: ...

class EvaluationInteractionDiagram(Enum):
    NU_MU_MU: EvaluationInteractionDiagram
    NU_M_M: EvaluationInteractionDiagram
    N_MU_MU: EvaluationInteractionDiagram

class NoResistanceConcreteTension1d(Enum):
    EXTREME: NoResistanceConcreteTension1d
    SECTION: NoResistanceConcreteTension1d
    ALWAYS: NoResistanceConcreteTension1d

class TypeSLSCalculation(Enum):
    BOTH: TypeSLSCalculation
    SHORT_TERM: TypeSLSCalculation
    LONG_TERM: TypeSLSCalculation

class CodeSettings(_OpenObject):
    evaluation_interaction_diagram: Incomplete
    theta: Incomplete
    theta_min: Incomplete
    theta_max: Incomplete
    n_cycles_fatigue: Incomplete
    no_resistance_concrete_tension_1d: Incomplete
    type_sls_calculation: Incomplete
    def __init__(self, *, evaluation_interaction_diagram: EvaluationInteractionDiagram = None, theta: float = None, theta_min: float = None, theta_max: float = None, n_cycles_fatigue: float = None, no_resistance_concrete_tension_1d: NoResistanceConcreteTension1d = None, type_sls_calculation: TypeSLSCalculation = None) -> None: ...

class CheckMember(_OpenElementId, ABC, metaclass=abc.ABCMeta):
    @abstractmethod
    def __init__(self, id_: int): ...

class CheckMember1D(CheckMember):
    name: Incomplete
    def __init__(self, id_: int, name: str) -> None: ...

class ThermalStateType(Enum):
    NONE: ThermalStateType
    CODE: ThermalStateType
    USER: ThermalStateType

class ThermalState(_OpenObject):
    def __init__(self, expansion: ThermalStateType = ..., conductivity: ThermalStateType = ..., specific_heat: ThermalStateType = ..., stress_strain: ThermalStateType = ..., strain: ThermalStateType = ...) -> None: ...

class _Material(_OpenElementId, ABC, metaclass=abc.ABCMeta):
    @abstractmethod
    def __init__(self, id_: int, name: str, e_modulus: float, g_modulus: float, poisson: float, unit_mass: float, specific_heat: float, thermal_expansion: float, thermal_conductivity: float, is_default: bool, order_in_code: int, thermal_state: ThermalState): ...

class ReinfClass(Enum):
    A: ReinfClass
    B: ReinfClass
    C: ReinfClass

class ReinfType(Enum):
    BARS: ReinfType
    DECOILED_RODS: ReinfType
    WIRE_FABRICS: ReinfType
    LATTICE_GIRDERS: ReinfType

class BarSurface(Enum):
    SMOOTH: BarSurface
    RIBBED: BarSurface

class ReinfDiagramType(Enum):
    BILINEAR_INCLINED: ReinfDiagramType
    BILINEAR_NOT_INCLINED: ReinfDiagramType
    USER: ReinfDiagramType

class ReinfFabrication(Enum):
    HOT_ROLLED: ReinfFabrication
    COLD_WORKED: ReinfFabrication

class MatReinforcement(_Material, ABC, metaclass=abc.ABCMeta):
    @abstractmethod
    def __init__(self, id_: int, name: str, e_modulus: float, g_modulus: float, poisson: float, unit_mass: float, specific_heat: float, thermal_expansion: float, thermal_conductivity: float, is_default: bool, order_in_code: int, thermal_state: ThermalState, bar_surface: BarSurface): ...

class MatReinforcementEc2(MatReinforcement):
    def __init__(self, id_: int, name: str, e_modulus: float, g_modulus: float, poisson: float, unit_mass: float, specific_heat: float, thermal_expansion: float, thermal_conductivity: float, is_default: bool, order_in_code: int, thermal_state: ThermalState, bar_surface: BarSurface, fyk: float, ftk_by_fyk: float, epsuk: float, ftk: float, class_: ReinfClass, type_: ReinfType, fabrication: ReinfFabrication, diagram_type: ReinfDiagramType) -> None: ...

class ConcDiagramType(Enum):
    BILINEAR: ConcDiagramType
    PARABOLIC: ConcDiagramType
    USER: ConcDiagramType

class ConcAggregateType(Enum):
    QUARTZITE: ConcAggregateType
    LIMESTONE: ConcAggregateType
    SANDSTONE: ConcAggregateType
    BASALT: ConcAggregateType

class ConcCementClass(Enum):
    S: ConcCementClass
    R: ConcCementClass
    N: ConcCementClass

class MatConcrete(_Material, ABC, metaclass=abc.ABCMeta):
    @abstractmethod
    def __init__(self, id_: int, name: str, e_modulus: float, g_modulus: float, poisson: float, unit_mass: float, specific_heat: float, thermal_expansion: float, thermal_conductivity: float, is_default: bool, order_in_code: int, thermal_state: ThermalState): ...

class ConcDependentParams(_OpenObject):
    def __init__(self, E_cm: float, eps_c1: float, eps_c2: float, eps_c3: float, eps_cu1: float, eps_cu2: float, eps_cu3: float, F_ctm: float, F_ctk_0_05: float, F_ctk_0_95: float, n_factor: float, F_cm: float) -> None: ...

class MatConcreteEc2(MatConcrete):
    def __init__(self, id_: int, name: str, e_modulus: float, g_modulus: float, poisson: float, unit_mass: float, specific_heat: float, thermal_expansion: float, thermal_conductivity: float, is_default: bool, order_in_code: int, thermal_state: ThermalState, fck: float, stone_diameter: float, cement_class: ConcCementClass, aggregate_type: ConcAggregateType, diagram_type: ConcDiagramType, silica_fume: bool, plain_concrete_diagram: bool, dep_params: ConcDependentParams = None) -> None: ...

class CrossSectionType(Enum):
    ONE_COMPONENT_CSS: CrossSectionType
    ROLLED_I: CrossSectionType
    ROLLED_ANGLE: CrossSectionType
    ROLLED_T: CrossSectionType
    ROLLED_U: CrossSectionType
    ROLLED_CHS: CrossSectionType
    ROLLED_RHS: CrossSectionType
    ROLLED_DOUBLE_UO: CrossSectionType
    ROLLED_DOUBLE_UC: CrossSectionType
    ROLLED_DOUBLE_LT: CrossSectionType
    ROLLED_DOUBLE_LU: CrossSectionType
    ROLLED_TI: CrossSectionType
    ROLLED_I_PAR: CrossSectionType
    ROLLED_U_PAR: CrossSectionType
    ROLLED_L_PAR: CrossSectionType
    BOX_FL: CrossSectionType
    BOX_WEB: CrossSectionType
    BOX_2I: CrossSectionType
    BOX_2U: CrossSectionType
    BOX_2U_2PI: CrossSectionType
    BOX_2L: CrossSectionType
    BOX_4L: CrossSectionType
    IW: CrossSectionType
    IWN: CrossSectionType
    TW: CrossSectionType
    O: CrossSectionType
    RECT: CrossSectionType
    IGN: CrossSectionType
    IGH: CrossSectionType
    TG: CrossSectionType
    LG: CrossSectionType
    LG_MIRRORED: CrossSectionType
    UG: CrossSectionType
    CHS_G: CrossSectionType
    ZG: CrossSectionType
    RHS_G: CrossSectionType
    OVAL: CrossSectionType
    GENERAL: CrossSectionType
    ROLLED_2I: CrossSectionType
    TRAPEZOID: CrossSectionType
    TTFH: CrossSectionType
    TWH: CrossSectionType
    TGREV: CrossSectionType
    TTFHREV: CrossSectionType
    TWHREV: CrossSectionType
    TCHAMFER_1: CrossSectionType
    TCHAMFER_2: CrossSectionType
    TT: CrossSectionType
    TT1: CrossSectionType
    SG: CrossSectionType
    GENERAL_STEEL: CrossSectionType
    GENERAL_CONCRETE: CrossSectionType
    COMPOSITE_BEAM_BOX: CrossSectionType
    COMPOSITE_BEAM_BOX_1: CrossSectionType
    COMPOSITE_BEAM_IGEN_T: CrossSectionType
    COMPOSITE_BEAM_L_LEFT: CrossSectionType
    COMPOSITE_BEAM_PLATE: CrossSectionType
    COMPOSITE_BEAM_R_RES_T: CrossSectionType
    COMPOSITE_BEAM_R_RES_T_1: CrossSectionType
    COMPOSITE_BEAM_R_T: CrossSectionType
    COMPOSITE_BEAM_SHAPE_CHAMF: CrossSectionType
    COMPOSITE_BEAM_SHAPE_CHAMF_ASYM: CrossSectionType
    COMPOSITE_BEAM_SHAPE_IGEN: CrossSectionType
    COMPOSITE_BEAM_SHAPE_I_T: CrossSectionType
    COMPOSITE_BEAM_SHAPE_I_T_ASYM: CrossSectionType
    COMPOSITE_BEAM_T_LEFT: CrossSectionType
    COMPOSITE_BEAM_TRAPEZOID: CrossSectionType
    COMPOSITE_BEAM_TRES_T: CrossSectionType
    COMPOSITE_BEAM_TREV: CrossSectionType
    COMPOSITE_BEAM_TREV_RES_I: CrossSectionType
    COMPOSITE_BEAM_TREV_RES_I_1: CrossSectionType
    COMPOSITE_BEAM_TREV_RES_R: CrossSectionType
    COMPOSITE_BEAM_TREV_RES_R_1: CrossSectionType
    COMPOSITE_BEAM_TREV_T: CrossSectionType
    COMPOSITE_BEAM_SHAPE_T_T: CrossSectionType
    BEAM_SHAPE_I_HAUNCH_CHAMFER: CrossSectionType
    BEAM_SHAPE_I_HAUNCH_CHAMFER_ASYM: CrossSectionType
    BEAM_SHAPE_REV_U: CrossSectionType
    BEAM_SHAPE_BOX: CrossSectionType
    BEAM_SHAPE_BOX_1: CrossSectionType
    BEAM_SHAPE_TREV_CHAMFER_HAUNCH_S: CrossSectionType
    BEAM_SHAPE_TREV_CHAMFER_HAUNCH_D: CrossSectionType
    BEAM_SHAPE_IREV_DEGEN: CrossSectionType
    BEAM_SHAPE_IREV_DEGEN_ADD: CrossSectionType
    BEAM_SHAPE_TREV_DEGEN: CrossSectionType
    BEAM_SHAPE_TREV_DEGEN_ADD: CrossSectionType
    BEAM_SHAPE_Z_DEGEN: CrossSectionType
    BEAM_SHAPE_I_Z_DEGEN: CrossSectionType
    BEAM_SHAPE_L_DEGEN: CrossSectionType
    CHS_PAR: CrossSectionType
    UNIQUE_NAME: CrossSectionType

class CrossSection(_OpenElementId, ABC, metaclass=abc.ABCMeta):
    @abstractmethod
    def __init__(self, id_: int, name: str): ...

class CrossSectionParameter(CrossSection):
    def __init__(self, id_: int, name: str, cross_section_type: CrossSectionType, material: _ReferenceElement, **parameters: Any) -> None: ...

class CrossSectionComponent(CrossSection):
    def __init__(self, id_: int, name: str) -> None: ...
    def create_component(self, outline: Sequence[tuple[float, float]], material: MatConcrete, *, openings: Sequence[Sequence[tuple[float, float]]] = None) -> None: ...

class _CssComponent(_OpenElementId):
    def __init__(self, id_: int, material: _ReferenceElement, outline: Sequence[tuple[float, float]], openings: Sequence[Sequence[tuple[float, float]]] | None) -> None: ...

class ReinforcedBar(_OpenObject):
    def __init__(self, coordinates: tuple[float, float], diameter: float, material: _ReferenceElement) -> None: ...
    @property
    def coordinates(self) -> tuple[float, float]: ...
    @property
    def diameter(self) -> float: ...
    @property
    def material_id(self) -> int: ...

class Stirrup(_OpenObject):
    diameter: Incomplete
    distance: Incomplete
    def __init__(self, points: Sequence[tuple[float, float] | tuple[tuple[float, float], tuple[float, float]]], diameter: float, material: _ReferenceElement, distance: float, shear_check: bool = None, torsion_check: bool = None, mandrel_diameter_factor: float = None, anchorage_length: float = None) -> None: ...
    @property
    def points(self) -> Sequence[tuple[float, float] | tuple[tuple[float, float], tuple[float, float]]]: ...
    @property
    def material_id(self) -> int: ...
    @property
    def shear_check(self) -> bool: ...
    @property
    def torsion_check(self) -> bool: ...
    @property
    def mandrel_diameter_factor(self) -> float: ...
    @property
    def anchorage_length(self) -> float: ...

class ReinforcedCrossSection(_OpenElementId):
    def __init__(self, id_: int, name: str, cross_section: _ReferenceElement, bars: list[ReinforcedBar] = None, stirrups: list[Stirrup] = None) -> None: ...
    @property
    def bars(self) -> list[ReinforcedBar]: ...
    @property
    def stirrups(self) -> list[Stirrup]: ...
    def create_bar(self, coordinates: tuple[float, float], diameter: float, material: MatReinforcement) -> None: ...
    def create_bar_layer(self, *, origin: tuple[float, float], diameter: float, material: MatReinforcement, number_of_bars: int, delta_y: float = None, delta_z: float = None) -> None: ...
    def create_stirrup(self, points: Sequence[tuple[float, float] | tuple[tuple[float, float], tuple[float, float]]], diameter: float, material: MatReinforcement, distance: float, shear_check: bool = None, torsion_check: bool = None, mandrel_diameter_factor: float = None, anchorage_length: float = None) -> None: ...

class ResultOfInternalForces(_OpenObject):
    def __init__(self, N: float = 0.0, Qy: float = 0.0, Qz: float = 0.0, Mx: float = 0.0, My: float = 0.0, Mz: float = 0.0) -> None: ...

class LoadingULS(_OpenObject):
    def __init__(self, internal_forces: ResultOfInternalForces, internal_forces_second_order: ResultOfInternalForces = None, internal_forces_begin: ResultOfInternalForces = None, internal_forces_end: ResultOfInternalForces = None, internal_forces_imperfection: ResultOfInternalForces = None) -> None: ...

class LoadingSLS(_OpenObject):
    def __init__(self, internal_forces: ResultOfInternalForces, internal_forces_imperfection: ResultOfInternalForces = None) -> None: ...

class FatigueLoading(_OpenObject):
    def __init__(self, max_loading: LoadingULS, min_loading: LoadingULS) -> None: ...

class CheckSectionExtreme(_OpenObject, metaclass=abc.ABCMeta):
    description: Incomplete
    @abstractmethod
    def __init__(self, accidental: LoadingULS = None, fatigue: FatigueLoading = None, frequent: LoadingSLS = None, fundamental: LoadingULS = None, characteristic: LoadingSLS = None, quasi_permanent: LoadingSLS = None, *, description: str): ...

class StandardCheckSectionExtreme(CheckSectionExtreme):
    def __init__(self, *, accidental: LoadingULS = None, frequent: LoadingSLS = None, fundamental: LoadingULS = None, characteristic: LoadingSLS = None, quasi_permanent: LoadingSLS = None, fatigue: FatigueLoading = None, description: str) -> None: ...

class CheckSection(_OpenElementId, ABC, metaclass=abc.ABCMeta):
    @abstractmethod
    def __init__(self, id_: int, description: str, check_member: _ReferenceElement, reinf_section: _ReferenceElement, extremes: list[CheckSectionExtreme] = None): ...
    @property
    def extremes(self) -> list[CheckSectionExtreme]: ...
    def create_extreme(self, *, description: str = None, accidental: LoadingULS = None, fatigue: FatigueLoading = None, frequent: LoadingSLS = None, fundamental: LoadingULS = None, characteristic: LoadingSLS = None, quasi_permanent: LoadingSLS = None) -> None: ...

class StandardCheckSection(CheckSection):
    def __init__(self, id_: int, description: str, check_member: _ReferenceElement, reinf_section: _ReferenceElement, extremes: list[CheckSectionExtreme] = None) -> None: ...

class MemberType(Enum):
    UNDEFINED: MemberType
    BEAM: MemberType
    COLUMN: MemberType
    BEAM_SLAB: MemberType
    HOLLOW_CORE_SLAB: MemberType
    TWO_WAY_SLAB: MemberType
    PLATE: MemberType
    WALL: MemberType

class TwoWaySlabType(Enum):
    SLAB: TwoWaySlabType
    WALL: TwoWaySlabType
    DEEP_BEAM: TwoWaySlabType
    SHELL_AS_PLATE: TwoWaySlabType
    SHELL_AS_WALL: TwoWaySlabType

class CalculationSetup(_OpenObject):
    def __init__(self, *, uls_response: bool = None, uls_diagram: bool = None, uls_shear: bool = None, uls_torsion: bool = None, uls_interaction: bool = None, sls_crack: bool = None, sls_stress_limitation: bool = None, sls_stiffnesses: bool = None, detailing: bool = None, m_n_kappa_diagram: bool = None, fatigue: bool = None, cross_section_characteristics: bool = None) -> None: ...

class ConcreteMemberData(_OpenObject, ABC, metaclass=abc.ABCMeta):
    @abstractmethod
    def __init__(self, element: _ReferenceElement, member_type: MemberType, two_way_slab_type: TwoWaySlabType, calculation_setup: CalculationSetup = None): ...

class ExposureClassEc2Carbonation(Enum):
    XC1: ExposureClassEc2Carbonation
    XC2: ExposureClassEc2Carbonation
    XC3: ExposureClassEc2Carbonation
    XC4: ExposureClassEc2Carbonation

class ExposureClassEc2Chlorides(Enum):
    XD1: ExposureClassEc2Chlorides
    XD2: ExposureClassEc2Chlorides
    XD3: ExposureClassEc2Chlorides

class ExposureClassEc2ChloridesFromSea(Enum):
    XS1: ExposureClassEc2ChloridesFromSea
    XS2: ExposureClassEc2ChloridesFromSea
    XS3: ExposureClassEc2ChloridesFromSea

class ExposureClassEc2FreezeAttack(Enum):
    XF1: ExposureClassEc2FreezeAttack
    XF2: ExposureClassEc2FreezeAttack
    XF3: ExposureClassEc2FreezeAttack
    XF4: ExposureClassEc2FreezeAttack

class ExposureClassEc2ChemicalAttack(Enum):
    XA1: ExposureClassEc2ChemicalAttack
    XA2: ExposureClassEc2ChemicalAttack
    XA3: ExposureClassEc2ChemicalAttack

class ExposureClassesDataEc2(_OpenObject):
    def __init__(self, *, carbonation: ExposureClassEc2Carbonation = None, chlorides: ExposureClassEc2Chlorides = None, chlorides_from_sea: ExposureClassEc2ChloridesFromSea = None, freeze_attack: ExposureClassEc2FreezeAttack = None, chemical_attack: ExposureClassEc2ChemicalAttack = None) -> None: ...

class ConcreteMemberDataEc2(ConcreteMemberData):
    def __init__(self, element: _ReferenceElement, member_type: MemberType, two_way_slab_type: TwoWaySlabType, calculation_setup: CalculationSetup = None, coeff_kx_for_wmax: float = None, exposure_class_data: ExposureClassesDataEc2 = None, creep_coefficient: float = None, relative_humidity: float = None) -> None: ...
