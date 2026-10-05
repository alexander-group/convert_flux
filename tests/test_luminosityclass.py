import pytest
import astropy.units as u
from convert_flux.convert_flux import Luminosity


def test_luminosity_quantity_created():
    """
    Test that ensures luminosity objects are created correctly.

    Attributes:
        luminosity1 (Luminosity): First luminosity object (from SDSS).
        luminosity2 (Luminosity): Second luminosity object (from ZTF).
    """
    luminosity1 = Luminosity(quantity=1.54e39 * (u.erg / u.s))
    luminosity2 = Luminosity(quantity=1.95e39 * (u.erg / u.s))
    assert isinstance(luminosity1, Luminosity)
    assert isinstance(luminosity2, Luminosity)


def test_luminosity_is_quantity():
    """
    Test that ensures luminosity objects are instances of astropy Quantity.

    Attributes:
        luminosity1 (Luminosity): First luminosity object (from SDSS).
        luminosity2 (Luminosity): Second luminosity object (from ZTF).
    """
    luminosity1 = Luminosity(quantity=1.54e39 * (u.erg / u.s))
    luminosity2 = Luminosity(quantity=1.95e39 * (u.erg / u.s))
    assert isinstance(luminosity1.quantity, u.Quantity)
    assert isinstance(luminosity2.quantity, u.Quantity)


def test_wrong_unit_luminosity():
    """
    Test that ensures a UnitConversionError is raised when an incorrect unit
    is provided by the user.

    Attributes:
        luminosity (Luminosity): Luminosity object with an incorrect unit.
    """
    with pytest.raises(u.UnitConversionError):
        Luminosity(quantity=1.54e39 * (u.m))


def test_type_error_for_non_quantity_luminosity():
    """
    Test that ensures a TypeError is raised when a non-Quantity value
    is provided by the user.

    Attributes:
        luminosity (Luminosity): Luminosity object with a non-Quantity value.
    """
    with pytest.raises(TypeError):
        Luminosity(quantity=1.54e39)
