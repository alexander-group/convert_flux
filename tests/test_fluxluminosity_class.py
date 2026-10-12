import pytest
import astropy.units as u
from convert_flux.convert_flux import Flux, Luminosity, FluxLuminosity


def test_flux_to_luminosity_creation():
    flux_luminosity = FluxLuminosity()
    assert isinstance(flux_luminosity, FluxLuminosity)


@pytest.mark.parametrize(
    "flux, distance, expected_luminosity",
    [
        (3.22e-14 * (u.erg / u.s / u.cm**2), 20e6 * u.pc, 1.54e39 * (u.erg / u.s)),
        (4.08e-14 * (u.erg / u.s / u.cm**2), 20e6 * u.pc, 1.95e39 * (u.erg / u.s)),
    ],
)
def test_flux_to_luminosity_conversion(flux, distance, expected_luminosity):
    flux_luminosity = FluxLuminosity()
    luminosity = flux_luminosity.flux_to_luminosity(flux, distance)

    assert isinstance(luminosity, Luminosity)
    assert abs(luminosity.quantity - expected_luminosity) < (5e36 * u.erg / u.s)


@pytest.mark.parametrize(
    "luminosity, distance, expected_flux",
    [
        (1.54e39 * (u.erg / u.s), 20e6 * u.pc, 3.22e-14 * (u.erg / u.s / u.cm**2)),
        (1.95e39 * (u.erg / u.s), 20e6 * u.pc, 4.08e-14 * (u.erg / u.s / u.cm**2)),
    ],
)
def test_luminosity_to_flux_conversion(luminosity, distance, expected_flux):
    flux_luminosity = FluxLuminosity()
    flux = flux_luminosity.luminosity_to_flux(luminosity, distance)

    assert isinstance(flux, Flux)
    assert abs(flux.quantity - expected_flux) < 1e-16 * (u.erg / u.s / u.cm**2)
