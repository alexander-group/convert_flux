# Import dependencies here
import pytest
import astropy.units as u
from convert_flux.convert_flux import Mag, FluxDensity, MagFluxDensity


@pytest.mark.parametrize(
    "central_wavelength",
    [
        (6187 * u.Angstrom),
        (6436 * u.Angstrom),
    ],
    ids=["sdss_r", "ztf_r"],
)
def test_mag_to_fluxdensity(spectral_coordinate):
    """
    This function tests the conversion from magnitude to flux density
    Args:
        spectral_coordinate (astropy Quantity): central wavelength/frequency
    """
    magnitude = Mag(quantity=20 * u.ABmag, spectral_coordinate=spectral_coordinate)
    conversion = MagFluxDensity(mag=magnitude)

    flux_density = conversion.mag_to_flux_density(spectral_coordinate)

    # Test if output is FluxDensity class
    assert isinstance(flux_density, FluxDensity)

    # Test if calculated value is within the tolerance of expected value
    expected_fd = 3.631e-5 * (u.Jy)
    assert (
        abs(flux_density.quantity - expected_fd) / expected_fd <= 1e-3
    ), f"Expected {expected_fd}, but got {flux_density}"


@pytest.mark.parametrize(
    "central_wavelength",
    [
        (6187 * u.Angstrom),
        (6436 * u.Angstrom),
    ],
    ids=["sdss_r", "ztf_r"],
)
def test_fluxdensity_to_mag(spectral_coordinate):
    """
    This function tests the conversion from flux density to magnitude
    Args:
        spectral_coordinate (astropy Quantity): central wavelength/frequency
    """
    flux_density = FluxDensity(
        quantity=36.315 * u.uJy, spectral_coordinate=spectral_coordinate
    )
    conversion = MagFluxDensity(flux_density=flux_density)

    mag = conversion.flux_density_to_mag(spectral_coordinate)

    # Test if output is Mag class
    assert isinstance(mag, Mag)

    # Test if calculated value is within the tolerance of expected value
    expected_mag = 20 * u.ABmag
    assert (
        mag.quantity - expected_mag <= 1e-3
    ), f"Expected {expected_mag}, but got {mag.quantity}"
