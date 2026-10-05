import pytest
import astropy.units as u
from convert_flux.convert_flux import Flux


def test_flux_quantity_created():
    flux1 = Flux(quantity=3.22e-14 * (u.erg / u.s / u.cm**2))
    flux2 = Flux(quantity=4.08e-14 * (u.erg / u.s / u.cm**2))
    assert isinstance(flux1, Flux)
    assert isinstance(flux2, Flux)


def test_flux_is_quantity():
    flux1 = Flux(quantity=3.22e-14 * (u.erg / u.s / u.cm**2))
    flux2 = Flux(quantity=4.08e-14 * (u.erg / u.s / u.cm**2))
    assert isinstance(flux1, u.Quantity)
    assert isinstance(flux2, u.Quantity)


def test_wrong_unit_flux():
    with pytest.raises(u.UnitConversionError):
        Flux(quantity=3.22e-14 * (u.m))


def test_type_error_for_non_quantity_flux():
    with pytest.raises(TypeError):
        Flux(quantity=3.22e-14)
