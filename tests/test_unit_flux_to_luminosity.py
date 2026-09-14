"""
Unit test for converting flux into luminosity
"""

# Import packages here
import astropy.units as u
import pytest
from convert_flux import convert_flux


@pytest.mark.xfail(reason="The convert_flux function is not implemented yet.")
# Define test function for output type (expected to be float)
def test_luminosity_output_type():
    ## Input values
    flux_value_sdss_r = 3.21e-14 * u.erg * (u.s**-1) * (u.cm**-2)

    ## Luminosity output
    luminosity_sdss_r = convert_flux(flux_value_sdss_r)

    assert isinstance(luminosity_sdss_r, float)


@pytest.mark.xfail(reason="The convert_flux function is not implemented yet.")
# Define test unit for converting SDSS r-band flux to luminosity
def test_flux_to_luminosity_sdss_r():
    """
    Args:
        flux (float): flux value
    """
    flux = 3.21e-14 * u.erg * (u.s**-1) * (u.cm**-2)
    luminosity = convert_flux(flux)
    expected_luminosity = 1.54e39

    assert (
        abs(luminosity - expected_luminosity) <= 1e-5
    ), f"Expected {expected_luminosity}, but got {luminosity}"


@pytest.mark.xfail(reason="The convert_flux function is not implemented yet.")
# Define test unit for converting ZTF r-band flux to luminosity
def test_flux_to_luminosity_ztf_r():
    """
    Args:
        flux (float): flux value
    """
    flux = 4.08e-14 * u.erg * (u.s**-1) * (u.cm**-2)
    luminosity = convert_flux(flux)
    expected_luminosity = 1.95e39

    assert (
        abs(luminosity - expected_luminosity) <= 1e-5
    ), f"Expected {expected_luminosity}, but got {luminosity}"
