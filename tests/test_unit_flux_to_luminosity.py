"""
Unit test for converting flux into luminosity
"""

# Import packages here
import astropy.units as u
from convert_flux import convert_flux


def test_luminosity_output_type():
    ## Input values
    flux_value_sdss_r = 3.21e-14 * u.erg * (u.s**-1) * (u.cm**-2)

    ## Luminosity output
    luminosity_sdss_r = convert_flux(
        flux_value_sdss_r, u.erg / u.s, distance=20 * u.Mpc
    )

    assert isinstance(luminosity_sdss_r, u.Quantity)


# Define test unit for converting SDSS r-band flux to luminosity
# Set tolerance to be 0.1% of the expected value
def test_flux_to_luminosity_sdss_r():
    flux = 3.21e-14 * u.erg * (u.s**-1) * (u.cm**-2)
    luminosity = convert_flux(flux, u.erg / u.s, distance=20 * u.Mpc)
    expected_luminosity = 1.536e39 * u.erg * (u.s**-1)

    assert (
        abs(luminosity - expected_luminosity) / expected_luminosity
    ).value <= 1e-3, f"Expected {expected_luminosity}, but got {luminosity}"


# Define test unit for converting ZTF r-band flux to luminosity
# Set tolerance to be 0.1% of the expected value
def test_flux_to_luminosity_ztf_r():
    flux = 4.08e-14 * u.erg * (u.s**-1) * (u.cm**-2)
    luminosity = convert_flux(flux, u.erg / u.s, distance=20 * u.Mpc)
    expected_luminosity = 1.953e39 * u.erg * (u.s**-1)

    assert (
        abs(luminosity - expected_luminosity) / expected_luminosity
    ).value <= 1e-3, f"Expected {expected_luminosity}, but got {luminosity}"
