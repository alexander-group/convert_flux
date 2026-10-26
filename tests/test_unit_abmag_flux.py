from convert_flux import convert_flux
import pytest
import astropy.units as u


@pytest.mark.xfail(reason="The convert_flux function is not implemented yet.")
def test_flux_output_type():
    abmag = 20.0 * u.ABmag
    unit_out = u.erg / (u.s * u.cm**2)
    flux = convert_flux(abmag, unit_out)

    assert isinstance(flux, u.Quantity)


@pytest.mark.xfail(reason="The convert_flux function is not implemented yet.")
def test_abmag_to_flux_and_back_to_ab_mag_for_sdss_rband():
    expected_abmag = 20.0 * u.ABmag
    expected_flux = 3.22e-14 * u.erg / (u.s * u.cm**2)

    unit_out_flux = u.erg / (u.s * u.cm**2)
    unit_out_abmag = u.ABmag

    transmission_curve = "sdss_r"

    flux = convert_flux(expected_abmag, unit_out_flux, transmission_curve)
    abmag = convert_flux(expected_flux, unit_out_abmag, transmission_curve)

    assert (
        abs(flux - expected_flux) < 1e-15
    ), f"Expected {expected_flux}, but got {flux}"
    assert (
        abs(abmag - expected_abmag) < 1e-15
    ), f"Expected {expected_abmag}, but got {abmag}"


@pytest.mark.xfail(reason="The convert_flux function is not implemented yet.")
def test_abmag_to_flux_and_back_to_ab_mag_for_ztf_rband():
    expected_abmag = 20.0 * u.ABmag
    expected_flux = 4.08e-14 * u.erg / (u.s * u.cm**2)

    unit_out_flux = u.erg / (u.s * u.cm**2)
    unit_out_abmag = u.ABmag

    transmission_curve = "ztf_r"

    flux = convert_flux(expected_abmag, unit_out_flux, transmission_curve)
    abmag = convert_flux(expected_flux, unit_out_abmag, transmission_curve)

    assert (
        abs(flux - expected_flux) < 1e-15
    ), f"Expected {expected_flux}, but got {flux}"
    assert (
        abs(abmag - expected_abmag) < 1e-15
    ), f"Expected {expected_abmag}, but got {abmag}"
