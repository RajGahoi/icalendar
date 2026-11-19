"""Regression tests for issue #2136: FLOAT values must not use an exponent."""

import re

import pytest

from icalendar import Event
from icalendar.prop import vFloat, vGeo

RFC_5545_FLOAT = re.compile(r"[+-]?\d+(\.\d+)?")
"""The FLOAT grammar of RFC 5545, section 3.3.7."""

VALUES = [0.00001, -0.00002, 1.5e-07, 1e16, -1e22, 5e-324, 1.7976931348623157e308]
"""Floats that Python writes with an exponent."""


@pytest.mark.parametrize("value", VALUES)
def test_vfloat_follows_the_float_grammar(value):
    """vFloat writes no exponent."""
    assert RFC_5545_FLOAT.fullmatch(vFloat(value).to_ical().decode())


@pytest.mark.parametrize("value", VALUES)
def test_vfloat_round_trip(value):
    """The value is the same after writing and parsing it."""
    assert vFloat.from_ical(vFloat(value).to_ical().decode()) == value


def test_vfloat_examples():
    """Small and large values are written with all their digits."""
    assert vFloat(0.00001).to_ical() == b"0.00001"
    assert vFloat(1e16).to_ical() == b"10000000000000000"


def test_vgeo_writes_no_exponent():
    """Coordinates close to zero are written with all their digits."""
    assert vGeo((0.00001, -0.00002)).to_ical() == "0.00001;-0.00002"


def test_geo_of_an_event():
    """The GEO property of an event has no exponent."""
    event = Event()
    event.add("GEO", (0.00001, -0.00002))
    assert b"GEO:0.00001;-0.00002" in event.to_ical()


def test_other_values_stay_the_same():
    """Values that had no exponent are written as before."""
    assert vFloat(3.1415).to_ical() == b"3.1415"
    assert vGeo((37.386013, -122.082932)).to_ical() == "37.386013;-122.082932"
