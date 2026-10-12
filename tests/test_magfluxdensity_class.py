# Import dependencies here
import numpy as np
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
# Test the conversion from magnitude to flux density
def test_mag_to_fluxdensity(central_wavelength):
    magnitude = Mag(quantity=20 * u.ABmag, spectral_coordinate=central_wavelength)
    conversion = MagFluxDensity(mag=magnitude)

    flux_density = conversion.mag_to_flux_density(central_wavelength)

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

# Test the conversion from flux density to magnitude
def test_fluxdensity_to_mag(central_wavelength):
    flux_density = FluxDensity(
        quantity=36.315 * u.uJy, spectral_coordinate=central_wavelength
    )
    conversion = MagFluxDensity(flux_density=flux_density)

    mag = conversion.flux_density_to_mag(central_wavelength)

    # Test if output is Mag class
    assert isinstance(mag, Mag)

    # Test if calculated value is within the tolerance of expected value
    expected_mag = 20 * u.ABmag
    assert (
        np.abs(mag.quantity.value - expected_mag.value) / expected_mag.value <= 1e-3
    ), f"Expected {expected_mag}, but got {mag.quantity}"


# test = 20 * u.ABmag
# print(test.unit)
