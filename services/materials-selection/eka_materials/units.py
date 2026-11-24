"""Dimensional validation without replacing the original source units."""

import math

from pint import UnitRegistry
from pint.errors import PintError


REGISTRY = UnitRegistry()
CANONICAL_UNITS = {
    "density": "kg/m^3",
    "tensile_yield_strength": "Pa",
    "tensile_modulus": "Pa",
    "thermal_conductivity": "W/(m*K)",
    "service_temperature": "K",
    "volume_resistivity": "ohm*m",
}


def normalize(value: float, unit: str, property_name: str) -> float:
    try:
        target = CANONICAL_UNITS[property_name]
        parsed_unit = REGISTRY.Unit(unit)
        if property_name == "service_temperature" and parsed_unit not in {
            REGISTRY.kelvin, REGISTRY.degC, REGISTRY.degF, REGISTRY.degR,
        }:
            raise ValueError("service temperature needs an absolute temperature unit")
        result = float(REGISTRY.Quantity(value, parsed_unit).to(target).magnitude)
    except (PintError, ValueError, TypeError, KeyError, OverflowError) as exc:
        raise ValueError(f"invalid unit {unit!r} for {property_name}") from exc
    if not math.isfinite(result) or result < 0:
        raise ValueError(f"{property_name} must normalize to a finite non-negative value")
    return result
