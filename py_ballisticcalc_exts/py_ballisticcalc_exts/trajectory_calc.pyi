from dataclasses import dataclass
from py_ballisticcalc.conditions import Atmo, Shot
from py_ballisticcalc.drag_model import DragDataPoint
from py_ballisticcalc.munition import Ammo
from py_ballisticcalc.unit import Angular, Distance
from typing_extensions import NamedTuple, Union

__all__ = ['TrajectoryCalc', 'get_global_max_calc_step_size', 'get_global_use_powder_sensitivity', 'set_global_max_calc_step_size', 'set_global_use_powder_sensitivity', 'reset_globals']

def get_global_max_calc_step_size() -> Distance: ...
def get_global_use_powder_sensitivity() -> bool: ...
def reset_globals() -> None: ...
def set_global_max_calc_step_size(value: Union[float, Distance]) -> None: ...
def set_global_use_powder_sensitivity(value: bool) -> None: ...

class CurvePoint(NamedTuple):
    a: float
    b: float
    c: float

@dataclass
class Vector:
    x: float
    y: float
    z: float
    def magnitude(self) -> float: ...
    def mul_by_const(self, a: float) -> Vector: ...
    def mul_by_vector(self, b: Vector) -> float: ...
    def add(self, b: Vector) -> Vector: ...
    def subtract(self, b: Vector) -> Vector: ...
    def negate(self) -> Vector: ...
    def normalize(self) -> Vector: ...
    def __add__(self, other: Vector) -> Vector: ...
    def __radd__(self, other: Vector) -> Vector: ...
    def __iadd__(self, other: Vector) -> Vector: ...
    def __sub__(self, other: Vector) -> Vector: ...
    def __rsub__(self, other: Vector) -> Vector: ...
    def __isub__(self, other: Vector) -> Vector: ...
    def __mul__(self, other: Union[int, float, 'Vector']) -> Union[float, 'Vector']: ...
    def __rmul__(self, other: Union[int, float, 'Vector']) -> Union[float, 'Vector']: ...
    def __imul__(self, other: Union[int, float, 'Vector']) -> Union[float, 'Vector']: ...
    def __neg__(self) -> Vector: ...
    def __init__(self, x, y, z) -> None: ...

class TrajectoryCalc:
    ammo: Ammo
    gravity_vector: Vector
    barrel_azimuth: float
    barrel_elevation: float
    twist: float
    def __init__(self, ammo: Ammo) -> None: ...
    @property
    def table_data(self) -> list[DragDataPoint]: ...
    @staticmethod
    def get_calc_step(step: float = 0): ...
    def trajectory(self, shot_info: Shot, max_range: Distance, dist_step: Distance, extra_data: bool = False): ...
    def zero_angle(self, shot_info: Shot, distance: Distance) -> Angular: ...
    def drag_by_mach(self, mach: float) -> float: ...
    def spin_drift(self, time) -> float: ...
    def calc_stability_coefficient(self, atmo: Atmo) -> float: ...
