import pytest
from astropy import units as u

from convert_flux import convert_flux


"""
Unit Test for converting AB mag to flux density
"""


@pytest.mark.xfail(reason="The convert_flux function is not implemented yet.")
def test_flux_density_output_type():
    # Define test function for output type, expected to be float
    """
    Arguments:
    Magnitude
    unit type of magnitude (AB mag)
    """
    abmag = 20.0 * u.ABmag
    unit_type = u.erg / (u.s * u.cm**3)
    transmission_curve = ""

    flux_density = convert_flux(abmag, unit_type, transmission_curve)

    assert isinstance(flux_density, u.Quantity)


@pytest.mark.xfail(reason="The convert_flux function is not implemented yet.")
def test_abmag_to_flux_density():
    # Test case 1: Convert a known AB magnitude to flux_density in Jy = erg/s/cm^3
    """
    Arguments:
    Magnitude
    unit type of magnitude (AB mag)
    """
    abmag = 20.0 * u.ABmag
    unit_type = u.erg / (u.s * u.cm**3)
    transmission_curve = ""
    flux_density = convert_flux(abmag, unit_type, transmission_curve)

    expected_flux_density = 3.631e-28 * (u.erg / (u.s * u.cm**3))
    assert (
        abs(flux_density - expected_flux_density) <= 1e-31
    ), f"Expected {expected_flux_density}, but got {flux_density}"
