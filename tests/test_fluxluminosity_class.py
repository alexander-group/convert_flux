import pytest
import astropy.units as u
from astropy.cosmology import FlatLambdaCDM, Planck18
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
    flux_luminosity = FluxLuminosity(flux=Flux(flux))
    luminosity = flux_luminosity.flux_to_luminosity(distance)

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
    flux_luminosity = FluxLuminosity(luminosity=Luminosity(luminosity))
    flux = flux_luminosity.luminosity_to_flux(distance)

    assert isinstance(flux, Flux)
    assert abs(flux.quantity - expected_flux) < 1e-16 * (u.erg / u.s / u.cm**2)


# Write pytests for cosmology implemented
def test_assert_default_cosmology():
    flux = 3.22e-14 * (u.erg / u.s / u.cm**2)
    flux_luminosity = FluxLuminosity(flux=Flux(flux), cosmo=None)

    assert flux_luminosity.cosmo is Planck18  # Default cosmology is Planck18


def test_custom_cosmology_is_stored():
    cosmo = FlatLambdaCDM(H0=70, Om0=0.3)
    assert FluxLuminosity(cosmo=cosmo).cosmo is cosmo


def test_redshift_distance_returns_distance_when_z_is_none():
    flux_luminosity = FluxLuminosity()
    distance = 20 * u.Mpc
    assert flux_luminosity.redshift_distance(distance, None) is distance


def test_ignore_distance_when_z_is_provided():
    fl = FluxLuminosity(cosmo=Planck18)
    distance = 20 * u.Mpc
    z = 0.01
    assert fl.redshift_distance(distance, z) == Planck18.luminosity_distance(z)


def test_invalid_cosmology_raises_type_error():
    with pytest.raises(TypeError):
        FluxLuminosity(cosmo="not_a_cosmology")


def test_custom_cosmology_changes_result():
    cosmo1 = Planck18
    cosmo2 = FlatLambdaCDM(H0=70, Om0=0.3)
    fl1 = FluxLuminosity(flux=Flux(3.22e-14 * (u.erg / u.s / u.cm**2)), cosmo=cosmo1)
    fl2 = FluxLuminosity(flux=Flux(3.22e-14 * (u.erg / u.s / u.cm**2)), cosmo=cosmo2)

    z = 1.0
    luminosity1 = fl1.flux_to_luminosity(None, z)
    luminosity2 = fl2.flux_to_luminosity(None, z)

    assert luminosity1.quantity != luminosity2.quantity


def test_larger_luminosity_with_larger_redshift():
    flux = 3.22e-14 * (u.erg / u.s / u.cm**2)
    flux_luminosity = FluxLuminosity(flux=Flux(flux), cosmo=Planck18)

    z1 = 0.01
    z2 = 0.1
    luminosity1 = flux_luminosity.flux_to_luminosity(None, z1)
    luminosity2 = flux_luminosity.flux_to_luminosity(None, z2)

    assert luminosity2.quantity > luminosity1.quantity


def test_smaller_flux_with_larger_redshift():
    luminosity = 1.54e39 * (u.erg / u.s)
    flux_luminosity = FluxLuminosity(luminosity=Luminosity(luminosity), cosmo=Planck18)

    z1 = 0.01
    z2 = 0.1
    flux1 = flux_luminosity.luminosity_to_flux(None, z1)
    flux2 = flux_luminosity.luminosity_to_flux(None, z2)

    assert flux2.quantity < flux1.quantity
