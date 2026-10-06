import pytest
import astropy.units as u
from convert_flux.convert_flux import Flux


def test_flux_quantity_created():
    """
    Test that ensures flux objects are created correctly.

    Attributes:
        flux1 (Flux): First flux object (from SDSS).
        flux2 (Flux): Second flux object (from ZTF).
    """
    flux1 = Flux(quantity=3.22e-14 * (u.erg / u.s / u.cm**2))
    flux2 = Flux(quantity=4.08e-14 * (u.erg / u.s / u.cm**2))
    assert isinstance(flux1, Flux)
    assert isinstance(flux2, Flux)


def test_flux_quantity_created_with_units():
    """
    Test that ensures flux objects are created correctly with units.

    Attributes:
        flux1 (Flux): First flux object (from SDSS).
        flux2 (Flux): Second flux object (from ZTF).
    """
    flux1 = Flux(quantity=3.22e-14 * (u.erg / u.s / u.cm**2))
    flux2 = Flux(quantity=4.08e-14 * (u.erg / u.s / u.cm**2))
    assert isinstance(flux1.quantity, u.Quantity)
    assert isinstance(flux2.quantity, u.Quantity)


def test_wrong_unit_flux():
    """
    Test that ensures a UnitConversionError is raised when an incorrect unit
    is provided.

    Attributes:
        flux (Flux): Flux object with an incorrect unit.
    """
    with pytest.raises(u.UnitConversionError):
        Flux(quantity=3.22e-14 * (u.m))


def test_type_error_for_non_quantity_flux():
    """
    Test that ensures a TypeError is raised when a non-Quantity value
    is provided.

    Attributes:
        flux (Flux): Flux object with a non-Quantity value.
    """
    with pytest.raises(TypeError):
        Flux(quantity=3.22e-14)
