# BallisticCalculator
LGPL library for small arms ballistic calculations (Python 3.9+)

### Table of contents
* [Installation](#installation)
* [Usage](#usage)
  * [Units of measure](#unit-manipulation-syntax)
  * [An example of calculations](#an-example-of-calculations)
  * [Output example](#example-of-the-formatted-output)
* [About project](#about-project)

### Installation
**Stable release from pypi, installing from binaries**

(Contains c-extensions which offer higher performance)
```shell
pip install py-ballisticcalc
```

**Build wheel package for your interpreter version by pypi sdist**

Download and install MSVC or GCC depending on target platform
```shell
pip install Cython>=3.0.0a10 
pip install py-ballisticcalc --no-binary :all:
```

**Also use `git clone` to build your own package**

(Contains cython files to build your own c-extensions)
```shell
git clone https://github.com/o-murphy/py_ballisticcalc
```   


### Usage

The library supports all the popular units of measurement, and adds different built-in methods to define and manipulate it
#### Unit manipulation syntax:

```python
from py_ballisticcalc.unit import *

# ways to define value in units
# 1. old syntax
unit_in_meter = Distance(100, Distance.Meter)
# 2. short syntax by Unit type class
unit_in_meter = Distance.Meter(100)
# 3. by Unit enum class
unit_in_meter = Unit.METER(100)

# >>> <Distance>: 100.0 m (3937.0078740157483)

# convert unit
# 1. by method
unit_in_yard = unit_in_meter.convert(Distance.Yard)
# 2. using shift syntax
unit_in_yards = unit_in_meter << Distance.Yard  # '<<=' operator also supports
# >>> <Distance>: 109.36132983377078 yd (3937.0078740157483)

# get value in specified units
# 1. by method
value_in_km = unit_in_yards.get_in(Distance.Kilometer)
# 2. by shift syntax
value_in_km = unit_in_yards >> Distance.Kilometer  # '>>=' operator also supports
# >>> 0.1

# getting unit raw value:
rvalue = Distance.Meter(10).raw_value
rvalue = float(Distance.Meter(10))

# units comparison:
# supports operators like < > <= >= == !=
Distance.Meter(100) == Distance.Centimeter(100)  # >>> False, compare two units by raw value
Distance.Meter(100) > 10  # >>> True, compare unit with float by raw value
```

#### An example of calculations

```python
from py_ballisticcalc import *
from py_ballisticcalc import Settings as Set

# set global library settings
Set.Units.Mach = Velocity.FPS
Set.Units.temperature = Temperature.Celsius
Set.Units.distance = Distance.Meter
Set.Units.sight_height = Distance.Centimeter

# set maximum inner Calculator step size, larger is faster, but accuracy is going down 
Set.set_max_calc_step_size(Distance.Foot(1))  # same as default
# enable muzzle velocity correction by powder temperature
Set.USE_POWDER_SENSITIVITY = True  # default False

# define params with default units
weight, diameter = 168, 0.308
# or define with specified units
length = Distance.Inch(1.282)  # length = Distance(1.282, Distance.Inch)

weapon = Weapon(9, 100, 2)
dm = DragModel(0.223, TableG7, weight, diameter)

bullet = Projectile(dm, length)
ammo = Ammo(bullet, 2750, 15)
ammo.calc_powder_sens(2723, 0)

zero_atmo = Atmo.icao()

# defining calculator instance
calc = Calculator(weapon, ammo, zero_atmo)
calc.update_elevation()

shot = Shot(1500, 100)

current_atmo = Atmo(100, 1000, 15, 72)
winds = [Wind(2, 90)]

data = calc.trajectory(shot, current_atmo, winds)

for p in data:
  print(p.formatted())
```
#### Example of the formatted output:
```shell
python -m py_ballisticcalc.example
```

```
['0.00 s', '0.000 m', '2750.0 ft/s', '2.46 mach', '-9.000 cm', '0.00 mil', '0.000 cm', '0.00 mil', '3825 J']
['0.12 s', '100.000 m', '2528.6 ft/s', '2.26 mach', '0.005 cm', '0.00 mil', '-3.556 cm', '-0.36 mil', '3233 J']
['0.26 s', '200.050 m', '2317.2 ft/s', '2.08 mach', '-7.558 cm', '-0.38 mil', '-13.602 cm', '-0.69 mil', '2715 J']
['0.41 s', '300.050 m', '2116.6 ft/s', '1.90 mach', '-34.843 cm', '-1.18 mil', '-30.956 cm', '-1.05 mil', '2266 J']
['0.57 s', '400.000 m', '1926.5 ft/s', '1.73 mach', '-85.739 cm', '-2.18 mil', '-57.098 cm', '-1.45 mil', '1877 J']
['0.75 s', '500.000 m', '1745.0 ft/s', '1.56 mach', '-165.209 cm', '-3.37 mil', '-94.112 cm', '-1.92 mil', '1540 J']
['0.95 s', '600.000 m', '1571.4 ft/s', '1.41 mach', '-279.503 cm', '-4.74 mil', '-144.759 cm', '-2.46 mil', '1249 J']
```

### About project

The library provides trajectory calculation for projectiles including for various
applications, including air rifles, bows, firearms, artillery and so on.

3DF model that is used in this calculator is rooted in old C sources of version 2 of the public version of JBM
calculator, ported to C#, optimized, fixed and extended with elements described in
Litz's "Applied Ballistics" book and from the friendly project of Alexandre Trofimov
and then ported to Go.

Now it's also ported to python3 and expanded to support calculation trajectory by 
multiple ballistics coefficients and using custom drag data (such as Doppler radar data ©Lapua, etc.)

The online version of Go documentation is located here: https://godoc.org/github.com/gehtsoft-usa/go_ballisticcalc

C# version of the package is located here: https://github.com/gehtsoft-usa/BallisticCalculator1

The online version of C# API documentation is located here: https://gehtsoft-usa.github.io/BallisticCalculator/web-content.html

Go documentation can be obtained using godoc tool.

The current status of the project is ALPHA version.

#### RISK NOTICE

The library performs very limited simulation of a complex physical process and so it performs a lot of approximations. Therefore, the calculation results MUST NOT be considered as completely and reliably reflecting actual behavior or characteristics of projectiles. While these results may be used for educational purpose, they must NOT be considered as reliable for the areas where incorrect calculation may cause making a wrong decision, financial harm, or can put a human life at risk.

THE CODE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE MATERIALS OR THE USE OR OTHER DEALINGS IN THE MATERIALS.
