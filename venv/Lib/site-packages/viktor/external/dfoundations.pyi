import abc
import pandas as pd
from ..core import Color, File
from ..geo import GEFData
from .external_program import ExternalProgram
from _typeshed import Incomplete
from abc import ABCMeta, abstractmethod
from datetime import datetime
from enum import Enum
from io import BytesIO, StringIO
from typing import Any

__all__ = ['BearingPilesCalculationOptions', 'BearingPilesModel', 'CPTRule', 'CalculationType', 'ConstructionSequence', 'DFoundationsAnalysis', 'DrivenBasePile', 'HShapedPile', 'HollowOpenPile', 'HollowPile', 'LostTipPile', 'MaxConeResistType', 'Metadata', 'OutputFileParser', 'PileLoadSettlementCurve', 'PileMaterial', 'PileSlipLayer', 'PileType', 'PileTypeClayLoamPeat', 'ProfileLayer', 'RectEnlPile', 'RectPile', 'RoundEnlPile', 'RoundPile', 'SectionPile', 'SoilType', 'TaperPile', 'TensionPilesCalculationOptions', 'TensionPilesModel', 'UserPile']

class DFoundationsAnalysis(ExternalProgram):
    input_file: Incomplete
    def __init__(self, input_file: BytesIO | File) -> None: ...
    def get_output_file(self, extension: str = '.fod', *, as_file: bool = False) -> BytesIO | File | None: ...

class SoilType(Enum):
    GRAVEL: SoilType
    SAND: SoilType
    LOAM: SoilType
    CLAY: SoilType
    PEAT: SoilType

class MaxConeResistType(Enum):
    STANDARD: MaxConeResistType
    MANUAL: MaxConeResistType

class CPTRule(Enum):
    NEN: CPTRule
    NEN_STRESS: CPTRule
    CUR: CPTRule
    TYPE_3: CPTRule
    QC_ONLY: CPTRule

class ConstructionSequence(Enum):
    CPT_EXCAVATION_INSTALL: ConstructionSequence
    INSTALL_CPT_EXCAVATION: ConstructionSequence
    EXCAVATION_CPT_INSTALL: ConstructionSequence
    EXCAVATION_INSTALL_CPT: ConstructionSequence
    INSTALL_EXCAVATION_CPT: ConstructionSequence
    CPT_INSTALL_EXCAVATION: ConstructionSequence
    EXCAVATION_CPT_BOTH_BEFORE_AND_AFTER_INSTALL: ConstructionSequence

class _MainCalculationType(Enum):
    PRELIMINARY_DESIGN: _MainCalculationType
    VERIFICATION: _MainCalculationType

class CalculationType(Enum):
    DESIGN_CALCULATION: CalculationType
    COMPLETE_CALCULATION: CalculationType
    INDICATION_BEARING_CAPACITY: CalculationType
    BEARING_CAPACITY_AT_FIXED_PILE_TIP_LEVEL: CalculationType
    PILE_TIP_LEVEL_AND_NET_BEARING_CAPACITY: CalculationType

class _ReductionConeResistance(Enum):
    SAFE: _ReductionConeResistance
    BEGEMANN: _ReductionConeResistance
    MANUAL: _ReductionConeResistance

class PileType(Enum):
    PREFAB_CONCRETE: PileType
    CLOSED_STEEL: PileType
    DRIVEN_TUBE_BACK_DRIVING: PileType
    DRIVEN_TUBE_BACK_VIBRATION: PileType
    TAPERED_TIMBER: PileType
    STRAIGHT_TIMBER: PileType
    SCREW_LOST_TIP: PileType
    SCREW_WITH_GROUT: PileType
    PREFAB_WITH_GROUT: PileType
    PREFAB_WITHOUT_GROUT: PileType
    STEEL: PileType
    CONTINUOUS_FLIGHT_AUGER: PileType
    BORED_DRILLING: PileType
    BORED_SHELLING: PileType
    OPEN_STEEL: PileType
    MV: PileType
    MICRO_DOUBLE_EXTORTED: PileType
    MICRO_DOUBLE_NOT_EXTORTED: PileType
    MICRO_SINGLE_EXTORTED: PileType
    MICRO_SINGLE_NOT_EXTORTED: PileType
    MICRO_ANCHOR_BORED: PileType
    MICRO_ANCHOR_SCREWED: PileType
    MICRO_VIBRATED: PileType
    GROUTED_STEEL_PROFILE: PileType
    GROUTED_STEEL_PIPE: PileType
    USER_DEFINED_VIBRATING: PileType
    USER_DEFINED_LOW_VIBRATING: PileType
    USER_DEFINED: PileType

class PileTypeClayLoamPeat(Enum):
    ACCORDING_TO_STANDARD: PileTypeClayLoamPeat
    USER_DEFINED: PileTypeClayLoamPeat

class PileLoadSettlementCurve(Enum):
    ONE: PileLoadSettlementCurve
    TWO: PileLoadSettlementCurve
    THREE: PileLoadSettlementCurve

class PileMaterial(Enum):
    CONCRETE: PileMaterial
    STEEL: PileMaterial
    TIMBER: PileMaterial
    WOOD: PileMaterial
    USER_DEFINED: PileMaterial

class PileSlipLayer(Enum):
    NONE: PileSlipLayer
    SYNTHETIC: PileSlipLayer
    BENTONITE: PileSlipLayer
    BITUMEN: PileSlipLayer
    USER_DEFINED: PileSlipLayer

class Metadata:
    def __init__(self, file_name: str = '-', company: str = '-', title_1: str = '-', title_2: str = '-', geotechnical_consultant: str = '', design_engineer: str = '', principal: str = '', project_id: str = '', location: str = '', current_date: bool = False, current_time: bool = False) -> None: ...

class _CalculationOptions:
    def __init__(self, calculation_type: CalculationType, rigid: bool, *, unit_weight_water: float = None, surcharge: float = None, max_allowed_settlement_str_geo: int = None, max_allowed_relative_rotation_str_geo: int = None, max_allowed_settlement_sls: int = None, max_allowed_relative_rotation_sls: int = None, xi3: float = None, xi4: float = None, gamma_b: float = None, gamma_s: float = None, gamma_fnk: float = None, gamma_m_var_qc: float = None, gamma_st: float = None, gamma_gamma: float = None, area: float = None, e_ea_gem: float = None, write_intermediate_results: bool = False, use_pile_group: bool = True, overrule_excavation: bool = False, suppress_qciii_reduction: bool = False, use_almere_rules: bool = False, use_extra_almere_rules: bool = False, use_compaction: bool = False, overrule_excess_pore_pressure: bool = True, trajectory_begin_end_interval: tuple[float, float, float] = None, net_bearing_capacity: int = None, cpt_test_level: float = None) -> None: ...
    @property
    def calculation_type(self) -> CalculationType: ...

class BearingPilesCalculationOptions(_CalculationOptions):
    def __init__(self, calculation_type: CalculationType, rigid: bool, max_allowed_settlement_str_geo: int = 150, max_allowed_settlement_sls: int = 150, max_allowed_relative_rotation_str_geo: int = 100, max_allowed_relative_rotation_sls: int = 300, *, xi3: float = None, xi4: float = None, gamma_b: float = None, gamma_s: float = None, gamma_fnk: float = None, area: float = None, e_ea_gem: float = None, write_intermediate_results: bool = False, use_pile_group: bool = True, overrule_excavation: bool = False, suppress_qciii_reduction: bool = False, use_almere_rules: bool = False, use_extra_almere_rules: bool = False, trajectory_begin_end_interval: tuple[float, float, float] = None, net_bearing_capacity: int = None, cpt_test_level: float = None) -> None: ...

class TensionPilesCalculationOptions(_CalculationOptions):
    def __init__(self, calculation_type: CalculationType, rigid: bool, unit_weight_water: float = 9.81, surcharge: float = 0.0, *, xi3: float = None, xi4: float = None, gamma_m_var_qc: float = None, gamma_st: float = None, gamma_gamma: float = None, use_compaction: bool = False, overrule_excavation: bool = False, overrule_excess_pore_pressure: bool = True, trajectory_begin_end_interval: tuple[float, float, float] = None, net_bearing_capacity: int = None) -> None: ...

class _Material:
    def __init__(self, soil_type: SoilType, gam_dry: float, gam_wet: float, color: Color = None, *, e0: float = 0.001001, diameter_d50: float = 0.2, min_void_ratio: float = 0.4, max_void_ratio: float = 0.8, cohesion: float = 0.0, phi: float = 20.0, cu: float = 0.0, max_cone_resist_type: MaxConeResistType = ..., max_cone_resist: float = 0.0, use_tension: bool = True, ca: float = 1.0, cc: float = 1.0) -> None: ...
    @property
    def color(self) -> Color: ...
    def serialize(self) -> dict[str, Any]: ...

class _CPT:
    def __init__(self, measurements: list[list[float]], ground_level: float, rule: CPTRule = ..., min_layer_thickness: float = 0.1, *, imported: bool, project_name: str = 'Unknown', project_id: str = '', client_name: str = 'Unknown', file_date: datetime = None, gef_version: str = 'Unknown', x: float = 987000000.0, y: float = 987000000.0, excavation_depth: float = 0.0) -> None: ...
    def serialize(self) -> dict[str, Any]: ...

class ProfileLayer:
    def __init__(self, top_level: float, material: str, ad_pore_pressure_at_top: float = 0.0, ad_pore_pressure_at_bottom: float = 0.0, ocr: float = 1.0) -> None: ...
    @property
    def material(self) -> str: ...

class _Profile:
    def __init__(self, cpt: _CPT, layers: list[ProfileLayer], x: float, y: float, phreatic_level: float, *, pile_tip_level: float = None, overconsolidation_ratio: float = None, top_positive_skin_friction: float = None, bottom_negative_skin_friction: float = None, expected_ground_level_settlement: float = None, top_tension_zone: float = None) -> None: ...
    @property
    def layers(self) -> list[ProfileLayer]: ...
    def serialize(self, name: str) -> dict[str, Any]: ...

class _PileShape(metaclass=ABCMeta):
    class _Shape(Enum):
        ROUND: _PileShape._Shape
        RECT: _PileShape._Shape
        ROUND_ENL: _PileShape._Shape
        RECT_ENL: _PileShape._Shape
        TAPER: _PileShape._Shape
        HOLLOW: _PileShape._Shape
        LOST_TIP: _PileShape._Shape
        DRIVEN: _PileShape._Shape
        SECTION: _PileShape._Shape
        HOL_OPEN: _PileShape._Shape
        H: _PileShape._Shape
        USER_DEFINED: _PileShape._Shape

class RectPile(_PileShape):
    width: Incomplete
    length: Incomplete
    def __init__(self, width: float, length: float) -> None: ...

class RectEnlPile(_PileShape):
    base_width: Incomplete
    base_length: Incomplete
    base_height: Incomplete
    shaft_width: Incomplete
    shaft_length: Incomplete
    def __init__(self, base_width: float, base_length: float, base_height: float, shaft_width: float, shaft_length: float) -> None: ...

class SectionPile(RectPile): ...

class UserPile(_PileShape):
    circumference: Incomplete
    cross_section: Incomplete
    def __init__(self, circumference: float, cross_section: float) -> None: ...

class RoundPile(_PileShape):
    diameter: Incomplete
    def __init__(self, diameter: float) -> None: ...

class TaperPile(_PileShape):
    diameter_tip: Incomplete
    increase: Incomplete
    def __init__(self, diameter_tip: float, increase: float) -> None: ...

class HollowPile(_PileShape):
    external_diameter: Incomplete
    wall_thickness: Incomplete
    def __init__(self, external_diameter: float, wall_thickness: float) -> None: ...
    @property
    def internal_diameter(self) -> float: ...

class HollowOpenPile(_PileShape):
    external_diameter: Incomplete
    wall_thickness: Incomplete
    def __init__(self, external_diameter: float, wall_thickness: float) -> None: ...
    @property
    def internal_diameter(self) -> float: ...

class LostTipPile(_PileShape):
    base_diameter: Incomplete
    pile_diameter: Incomplete
    def __init__(self, base_diameter: float, pile_diameter: float) -> None: ...

class RoundEnlPile(LostTipPile):
    base_height: Incomplete
    def __init__(self, base_diameter: float, pile_diameter: float, base_height: float) -> None: ...

class DrivenBasePile(RoundEnlPile): ...

class HShapedPile(_PileShape):
    height: Incomplete
    width: Incomplete
    thickness_web: Incomplete
    thickness_flange: Incomplete
    def __init__(self, height: float, width: float, thickness_web: float, thickness_flange: float) -> None: ...

class _PileTypeConfig(metaclass=ABCMeta):
    def __init__(self, type_sand_gravel: PileType = None, type_clay_loam_peat: PileTypeClayLoamPeat = None, material: PileMaterial = None, factor_sand_gravel: float = None, factor_clay_loam_peat: float = None, material_property: float = None) -> None: ...
    @abstractmethod
    def validate(self, shape: type[_PileShape]) -> None: ...
    def serialize(self) -> dict[str, Any]: ...

class _BearingPileTypeConfig(_PileTypeConfig):
    def __init__(self, pile_type: PileType, slip_layer: PileSlipLayer, type_sand_gravel: PileType = None, type_clay_loam_peat: PileTypeClayLoamPeat = None, type_p: PileType = None, load_settlement_curve: PileLoadSettlementCurve = None, material: PileMaterial = None, factor_sand_gravel: float = None, factor_clay_loam_peat: float = None, factor_pile_class: float = None, e_modulus_material: float = None, slip_layer_adhesion: float = None, use_pre_2016: bool = False, as_prefab: bool = False, qciii_reduction: float = None, overrule_tip_section_factor: float = None, overrule_tip_shape_factor: float = None) -> None: ...
    def validate(self, shape: type[_PileShape]) -> None: ...
    def serialize(self) -> dict[str, Any]: ...

class _TensionPileTypeConfig(_PileTypeConfig):
    def __init__(self, type_sand_gravel: PileType, type_clay_loam_peat: PileTypeClayLoamPeat, material: PileMaterial, factor_sand_gravel: float = None, factor_clay_loam_peat: float = None, unit_weight_material: float = None) -> None: ...
    def validate(self, shape: type[_PileShape]) -> None: ...

class _PileType:
    def __init__(self, shape: _PileShape, config: _PileTypeConfig) -> None: ...
    def serialize(self, name: str) -> dict[str, Any]: ...

class _Pile:
    def __init__(self, x: float, y: float, *, pile_head_level: float = 0.0, surcharge: float = 0.0, limit_state_str_geo: float = 0.0, serviceability_limit_state: float = 0.0, load_max_min: tuple[float, float] = None) -> None: ...
    def serialize(self, name: str) -> dict[str, Any]: ...

class _Model(metaclass=ABCMeta):
    def __init__(self, construction_sequence: ConstructionSequence, calculation_options: _CalculationOptions, excavation_level: float, reduction_cone_resistance: float = None, *, create_default_materials: bool = True) -> None: ...
    @property
    def materials(self) -> dict[str, dict[str, Any]]: ...
    @property
    def profiles(self) -> list[dict[str, Any]]: ...
    @property
    def pile_types(self) -> list[dict[str, Any]]: ...
    @property
    def piles(self) -> list[dict[str, Any]]: ...
    def generate_input_file(self, metadata: Metadata = None, *, as_file: bool = False) -> File | BytesIO: ...

class BearingPilesModel(_Model):
    def __init__(self, construction_sequence: ConstructionSequence, calculation_options: BearingPilesCalculationOptions, excavation_level: float, reduction_cone_resistance: float = None, *, create_default_materials: bool = True) -> None: ...
    def create_material(self, name: str, soil_type: SoilType, gamma_unsat: float, gamma_sat: float, friction_angle: float, diameter_d50: float = 0.2, color: Color = None) -> None: ...
    def create_profile(self, name: str, layers: list[ProfileLayer], x: float, y: float, measurements: list[tuple[float, float]], phreatic_level: float, pile_tip_level: float, overconsolidation_ratio: float, top_positive_skin_friction: float, bottom_negative_skin_friction: float, expected_ground_level_settlement: float, *, cpt_rule: CPTRule = ..., min_layer_thickness: float = 0.1) -> None: ...
    def import_profile(self, cpt: GEFData, layers: list[ProfileLayer], x: float, y: float, phreatic_level: float, pile_tip_level: float, overconsolidation_ratio: float, top_positive_skin_friction: float, bottom_negative_skin_friction: float, expected_ground_level_settlement: float, name: str = None, manual_ground_level: float = None, *, cpt_rule: CPTRule = ..., min_layer_thickness: float = 0.1) -> None: ...
    def create_pile_type(self, name: str, shape: _PileShape, pile_type: PileType, slip_layer: PileSlipLayer, type_sand_gravel: PileType = None, type_clay_loam_peat: PileTypeClayLoamPeat = None, type_p: PileType = None, load_settlement_curve: PileLoadSettlementCurve = None, material: PileMaterial = None, factor_sand_gravel: float = None, factor_clay_loam_peat: float = None, factor_pile_class: float = None, e_modulus: float = None, slip_layer_adhesion: float = None, *, use_pre_2016: bool = False, as_prefab: bool = False, qciii_reduction: float = None, overrule_tip_section_factor: float = None, overrule_tip_shape_factor: float = None) -> None: ...
    def create_pile(self, name: str, x: float, y: float, pile_head_level: float, surcharge: float, limit_state_str_geo: float, serviceability_limit_state: float) -> None: ...

class TensionPilesModel(_Model):
    def __init__(self, construction_sequence: ConstructionSequence, calculation_options: TensionPilesCalculationOptions, excavation_level: float, reduction_cone_resistance: float = None, *, create_default_materials: bool = True) -> None: ...
    def create_material(self, name: str, soil_type: SoilType, gamma_unsat: float, gamma_sat: float, friction_angle: float, diameter_d50: float = 0.2, max_cone_resist_type: MaxConeResistType = ..., max_cone_resist: float = 0.0, apply_tension: bool = True, min_void_ratio: float = 0.4, max_void_ratio: float = 0.8, color: Color = None) -> None: ...
    def create_profile(self, name: str, layers: list[ProfileLayer], x: float, y: float, measurements: list[tuple[float, float]], phreatic_level: float, pile_tip_level: float, top_tension_zone: float, *, cpt_rule: CPTRule = ..., min_layer_thickness: float = 0.1) -> None: ...
    def import_profile(self, cpt: GEFData, layers: list[ProfileLayer], x: float, y: float, phreatic_level: float, pile_tip_level: float, top_tension_zone: float, name: str = None, manual_ground_level: float = None, *, cpt_rule: CPTRule = ..., min_layer_thickness: float = 0.1) -> None: ...
    def create_pile_type(self, name: str, shape: _PileShape, type_sand_gravel: PileType, type_clay_loam_peat: PileTypeClayLoamPeat, material: PileMaterial, factor_sand_gravel: float = None, factor_clay_loam_peat: float = None, unit_weight_material: float = None) -> None: ...
    def create_pile(self, name: str, x: float, y: float, pile_head_level: float, load_max_min: tuple[float, float] = None) -> None: ...

class OutputFileParser(metaclass=abc.ABCMeta):
    def __new__(cls, fod_file: StringIO) -> Any: ...
    def __init__(self, fod_file: StringIO) -> None: ...
    @property
    def raw_results(self) -> str: ...
    @property
    @abstractmethod
    def calculation_parameters(self) -> dict[str, float | bool]: ...
    @abstractmethod
    def results(self, as_pandas: bool = True) -> dict[str, pd.DataFrame | dict[str, Any]]: ...

class _ParserV19: ...

class _PreliminaryBearingParserV17(OutputFileParser):
    @property
    def calculation_parameters(self) -> dict[str, float | bool]: ...
    def results(self, as_pandas: bool = True) -> dict[str, pd.DataFrame | dict[str, Any]]: ...

class _PreliminaryTensionParserV17(OutputFileParser):
    @property
    def calculation_parameters(self) -> dict[str, float | bool]: ...
    def results(self, as_pandas: bool = True) -> dict[str, Any]: ...

class _VerificationParserV17(OutputFileParser):
    def __init__(self, fod_file: StringIO) -> None: ...
    @property
    def calculation_parameters(self) -> dict[str, float | bool]: ...
    def results(self, as_pandas: bool = True) -> dict[str, pd.DataFrame | dict[str, Any]]: ...

class _PreliminaryBearingParserV19(OutputFileParser, _ParserV19):
    def __init__(self, fod_file: StringIO) -> None: ...
    @property
    def calculation_parameters(self) -> dict[str, float | bool]: ...
    def results(self, as_pandas: bool = True) -> dict[str, pd.DataFrame | dict[str, Any]]: ...

class _PreliminaryTensionParserV19(_PreliminaryTensionParserV17, _ParserV19):
    def results(self, as_pandas: bool = True) -> dict[str, pd.DataFrame | dict[str, Any]]: ...

class _VerificationParserV19(OutputFileParser, _ParserV19):
    @property
    def calculation_parameters(self) -> dict[str, float | bool]: ...
    def results(self, as_pandas: bool = True) -> dict[str, pd.DataFrame | dict[str, Any]]: ...
