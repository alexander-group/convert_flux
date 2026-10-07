import pytest
import astropy.units as u
from convert_flux.convert_flux import FluxDensity


def test_fluxdensity_quantity_created():
    flux_density1 = FluxDensity(
        quantity=36.31 * u.Jy, spectral_coordinate=6187 * u.Angstrom
    )
    flux_density2 = FluxDensity(
        quantity=2.84e-11 * u.erg / (u.s * u.cm**2 * u.Angstrom),
        spectral_coordinate=6187 * u.Angstrom,
    )
    assert isinstance(flux_density1, FluxDensity)
    assert isinstance(flux_density2, FluxDensity)


def test_flux_density_quantity_is_quantity():
    flux_density1 = FluxDensity(
        quantity=36.31 * u.Jy, spectral_coordinate=6187 * u.Angstrom
    )
    flux_density2 = FluxDensity(
        quantity=2.84e-12 * u.erg / (u.s * u.cm**2 * u.Angstrom),
        spectral_coordinate=6187 * u.Angstrom,
    )
    assert isinstance(flux_density1.quantity, u.Quantity)
    assert isinstance(flux_density2.quantity, u.Quantity)


def test_wrong_unit_flux_density():
    with pytest.raises(u.UnitConversionError):
        FluxDensity(quantity=36.31 * u.kg, spectral_coordinate=6187 * u.Angstrom)


def test_wrong_unit_for_spectral_coordinate():
    with pytest.raises(u.UnitConversionError):
        FluxDensity(quantity=36.31 * u.Jy, spectral_coordinate=6187 * u.kg)


def test_type_error_for_non_quantity_fd():
    with pytest.raises(TypeError):
        FluxDensity(quantity=3.631, spectral_coordinate=6187 * u.Angstrom)


def test_type_error_for_non_quantity_spec_coord():
    with pytest.raises(TypeError):
        FluxDensity(quantity=3.631 * u.Jy, spectral_coordinate=6187)
