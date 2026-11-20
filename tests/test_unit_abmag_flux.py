from convert_flux import convert_flux
import astropy.units as u


def test_flux_output_type():
    abmag = 20.0 * u.ABmag
    unit_out = u.erg / (u.s * u.cm**2)
    transmission_band = "r"
    transmission_instrument = "SDSS"
    transmission_telescope = "SLOAN"
    flux = convert_flux(
        abmag,
        unit_out,
        transmission_band,
        transmission_telescope,
        transmission_instrument,
    )

    assert isinstance(flux, u.Quantity)


def test_abmag_to_flux_and_back_to_ab_mag_for_sdss_rband():
    expected_abmag = 20.0 * u.ABmag
    expected_flux = 1.554e-14 * u.erg / (u.s * u.cm**2)

    unit_out_flux = u.erg / (u.s * u.cm**2)
    unit_out_abmag = u.ABmag

    transmission_band = "r"
    transmission_instrument = "SDSS"
    transmission_telescope = "SLOAN"

    flux = convert_flux(
        expected_abmag,
        unit_out_flux,
        transmission_band,
        transmission_telescope,
        transmission_instrument,
    )
    abmag = convert_flux(
        expected_flux,
        unit_out_abmag,
        transmission_band,
        transmission_telescope,
        transmission_instrument,
    )

    assert (
        abs(flux.value - expected_flux.value) / expected_flux.value <= 1e-3
    ), f"Expected {expected_flux}, but got {flux}"
    assert (
        abs(abmag.value - expected_abmag.value) < 5e-3
    ), f"Expected {expected_abmag}, but got {abmag}"


def test_abmag_to_flux_and_back_to_ab_mag_for_ztf_rband():
    expected_abmag = 20.0 * u.ABmag
    expected_flux = 3.455e-14 * u.erg / (u.s * u.cm**2)

    unit_out_flux = u.erg / (u.s * u.cm**2)
    unit_out_abmag = u.ABmag

    transmission_band = "r"
    transmission_instrument = "ZTF"
    transmission_telescope = "Palomar"

    flux = convert_flux(
        expected_abmag,
        unit_out_flux,
        transmission_band,
        transmission_telescope,
        transmission_instrument,
    )
    abmag = convert_flux(
        expected_flux,
        unit_out_abmag,
        transmission_band,
        transmission_telescope,
        transmission_instrument,
    )

    assert (
        abs(flux.value - expected_flux.value) / expected_flux.value <= 1e-3
    ), f"Expected {expected_flux}, but got {flux}"
    assert (
        abs(abmag.value - expected_abmag.value) < 5e-3
    ), f"Expected {expected_abmag}, but got {abmag}"
