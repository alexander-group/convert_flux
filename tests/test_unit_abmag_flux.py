from convert_flux import convert_flux
import pytest


@pytest.mark.xfail(reason="The convert_flux function is not implemented yet.")
def test_flux_output_type():
    abmag = 20.0
    telescope = "SDSS"
    bandpass = "r"
    unit_in = "ABMag"
    unit_out = "erg/s/cm^2"
    flux = convert_flux(abmag, telescope, bandpass, unit_in, unit_out)

    assert isinstance(flux, float)


@pytest.mark.xfail(reason="The convert_flux function is not implemented yet.")
def test_abmag_to_flux_for_sdss_rband():
    # Test case 1: Convert a known AB magnitude to flux
    """
    variables:
    magnitude value
    type of magnitude
    telescope
    bandpass
    transmission curve
    """
    abmag = 20.0
    telescope = "SDSS"
    bandpass = "r"
    unit_in = "ABMag"
    unit_out = "erg/s/cm^2"
    flux = convert_flux(abmag, telescope, bandpass, unit_in, unit_out)

    expected_flux = 3.22e-14

    assert (
        abs(flux - expected_flux) < 1e-15
    ), f"Expected {expected_flux}, but got {flux}"


@pytest.mark.xfail(reason="The convert_flux function is not implemented yet.")
def test_abmag_to_flux_for_ztf_rband():
    # Test case 2: Convert a known AB magnitude to flux
    """
    variables:
    magnitude value
    type of magnitude
    telescope
    bandpass
    transmission curve
    """
    abmag = 20.0
    telescope = "ZTF"
    bandpass = "r"
    unit_in = "ABMag"
    unit_out = "erg/s/cm^2"
    flux = convert_flux(abmag, telescope, bandpass, unit_in, unit_out)

    expected_flux = 4.08e-14

    assert (
        abs(flux - expected_flux) < 1e-15
    ), f"Expected {expected_flux}, but got {flux}"
