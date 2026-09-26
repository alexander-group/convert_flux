import pytest

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
    abmag = 20.0
    unit_in = "ABMag"
    unit_out = "erg/s/cm^2/Hz"
    flux_density = convert_flux(abmag, unit_in, unit_out)

    assert isinstance(flux_density, float)


@pytest.mark.xfail(reason="The convert_flux function is not implemented yet.")
def test_abmag_to_flux_density():
    # Test case 1: Convert a known AB magnitude to flux_density in Jy = erg/s/cm^2/Hz
    """
    Arguments:
    Magnitude
    unit type of magnitude (AB mag)
    """
    abmag = 20.0
    unit_in = "ABMag"
    unit_out = "erg/s/cm^2/Hz"
    flux_density = convert_flux(abmag, unit_in, unit_out)

    expected_flux_density = 3.631e-28
    assert (
        abs(flux_density - expected_flux_density) <= 1e-6
    ), f"Expected {expected_flux_density}, but got {flux_density}"
