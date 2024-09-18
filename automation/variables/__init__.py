from .temperature import Temperature
from .length import Length
from .current import Current
from .eng_time import Time
from .pressure import Pressure
from .mass import Mass
from .force import Force
from .power import Power
from .volumetric_flow import VolumetricFlow


temperature_base = Temperature(value=1, unit='K')
length_base = Length(value=1, unit="m")
current_base = Current(value=1, unit="A")
time_base = Time(value=1, unit="s")
pressure_base = Pressure(value=1, unit="bar")
mass_base = Mass(value=1, unit="kg")
force_base = Force(value=1, unit="J/m")
power_base = Power(value=1, unit="kW")
volumetric_flow_base = VolumetricFlow(value=1, unit="BBL/sec")

VARIABLES = {
    f"{temperature_base.__class__.__name__}": temperature_base.Units.serialize(),
    f"{length_base.__class__.__name__}": length_base.Units.serialize(),
    f"{current_base.__class__.__name__}": current_base.Units.serialize(),
    f"{time_base.__class__.__name__}": time_base.Units.serialize(),
    f"{pressure_base.__class__.__name__}": pressure_base.Units.serialize(),
    f"{mass_base.__class__.__name__}": mass_base.Units.serialize(),
    f"{force_base.__class__.__name__}": force_base.Units.serialize(),
    f"{power_base.__class__.__name__}": power_base.Units.serialize(),
    f"{volumetric_flow_base.__class__.__name__}": volumetric_flow_base.Units.serialize()
}

DATATYPES = [
    {'label': 'Float', 'value': 'float'},
    {'label': 'Integer', 'value': 'integer'},
    {'label': 'Boolean', 'value': 'boolean'},
    {'label': 'String', 'value': 'string'}
]