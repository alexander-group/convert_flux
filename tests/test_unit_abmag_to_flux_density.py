from astropy import units as u

from convert_flux import convert_flux


"""
Unit Test for converting AB mag to flux density
"""


def test_flux_density_output_type():
    # Define test function for output type, expected to be float
    """
    Arguments:
    Magnitude
    unit type of magnitude (AB mag)
    """
    abmag = 20.0 * u.ABmag
    unit_type = u.erg / (u.s * u.cm**2 * u.Hz)

    flux_density = convert_flux(abmag, unit_type)

    assert isinstance(flux_density, u.Quantity)


def test_abmag_to_flux_density():
    # Test case 1: Convert a known AB magnitude to flux_density in Jy = erg/s/cm^2/Hz
    """
    Arguments:
    Magnitude
    unit type of magnitude (AB mag)
    """
    abmag = 20.0 * u.ABmag
    unit_type = u.erg / (u.s * u.cm**2 * u.Hz)
    flux_density = convert_flux(abmag, unit_type)

    expected_flux_density = 3.631e-28 * (u.erg / (u.s * u.cm**2 * u.Hz))
    assert abs(flux_density - expected_flux_density) <= (
        1e-31 * (u.erg / (u.s * u.cm**2 * u.Hz))
    ), f"Expected {expected_flux_density}, but got {flux_density}"
