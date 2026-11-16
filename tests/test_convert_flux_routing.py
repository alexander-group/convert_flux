"""
Tests for how convert_flux() identifies brightness quantities and chains the
converters between them.
"""

import astropy.units as u
import pytest

from convert_flux import convert_flux
from convert_flux.convert_flux import _brightness_kind
from convert_flux.utils import VEGAMAG

FLUX_UNIT = u.erg / (u.s * u.cm**2)
LUMINOSITY_UNIT = u.erg / u.s


@pytest.mark.parametrize(
    "unit, expected_kind",
    [
        (u.ABmag, "mag"),
        (u.STmag, "mag"),
        (VEGAMAG, "mag"),
        (u.uJy, "flux_density"),
        (u.erg / (u.s * u.cm**2 * u.Hz), "flux_density"),
        (u.erg / (u.s * u.cm**2 * u.Angstrom), "flux_density"),
        (u.W / (u.m**2 * u.nm), "flux_density"),
        (u.erg / (u.s * u.cm**2), "flux"),
        (u.W / u.m**2, "flux"),
        (u.erg / u.s, "luminosity"),
        (u.Lsun, "luminosity"),
    ],
    ids=[
        "ABmag",
        "STmag",
        "VEGAMAG",
        "uJy",
        "fnu_cgs",
        "flam_cgs",
        "flam_si",
        "flux_cgs",
        "flux_si",
        "luminosity_cgs",
        "luminosity_lsun",
    ],
)
def test_brightness_kind(unit, expected_kind):
    assert _brightness_kind(unit) == expected_kind


def test_brightness_kind_rejects_unsupported_unit():
    with pytest.raises(ValueError):
        _brightness_kind(u.km)


def test_abmag_to_fnu_without_transmission_curve():
    fnu = convert_flux(20.0 * u.ABmag, u.erg / (u.s * u.cm**2 * u.Hz))
    expected = 3.631e-28 * u.erg / (u.s * u.cm**2 * u.Hz)

    assert isinstance(fnu, u.Quantity)
    assert abs(fnu - expected) / expected <= 1e-3, f"Expected {expected}, got {fnu}"


def test_same_kind_unit_change():
    flux = convert_flux(1.0 * u.W / u.m**2, FLUX_UNIT)
    expected = 1000.0 * FLUX_UNIT

    assert abs(flux - expected) / expected <= 1e-3, f"Expected {expected}, got {flux}"


def test_flux_to_luminosity_with_distance():
    flux = 3.21e-14 * FLUX_UNIT
    luminosity = convert_flux(flux, LUMINOSITY_UNIT, distance=20 * u.Mpc)
    expected = 1.536e39 * LUMINOSITY_UNIT

    assert (
        abs(luminosity - expected) / expected <= 1e-3
    ), f"Expected {expected}, got {luminosity}"


def test_luminosity_to_flux_round_trip():
    luminosity = 1.54e39 * LUMINOSITY_UNIT
    flux = convert_flux(luminosity, FLUX_UNIT, distance=20 * u.Mpc)
    luminosity_back = convert_flux(flux, LUMINOSITY_UNIT, distance=20 * u.Mpc)

    assert abs(luminosity_back - luminosity) / luminosity <= 1e-6


def test_flux_density_to_flux_without_transmission_curve_raises():
    with pytest.raises(ValueError, match="transmission_curve"):
        convert_flux(1.0 * u.uJy, FLUX_UNIT)


def test_flux_to_luminosity_without_distance_raises():
    with pytest.raises(ValueError, match="distance"):
        convert_flux(3.21e-14 * FLUX_UNIT, LUMINOSITY_UNIT)


def test_unsupported_output_unit_raises():
    with pytest.raises(ValueError):
        convert_flux(20.0 * u.ABmag, u.km)


@pytest.mark.xfail(reason="TransmissionCurve is not implemented yet.")
@pytest.mark.parametrize(
    "transmission_curve", ["sdss_r", "ztf_r"], ids=["sdss_r", "ztf_r"]
)
def test_abmag_to_flux_and_back(transmission_curve):
    """
    Test that AB magnitude converts to flux and back through flux density.
    """
    abmag = 20.0 * u.ABmag
    flux = convert_flux(abmag, FLUX_UNIT, transmission_curve)
    abmag_back = convert_flux(flux, u.ABmag, transmission_curve)

    assert abs(abmag_back.value - abmag.value) <= 1e-6


@pytest.mark.xfail(reason="TransmissionCurve is not implemented yet.")
def test_abmag_to_luminosity_and_back():
    """
    Test that AB magnitude converts to luminosity and back through all three
    converters.
    """
    abmag = 20.0 * u.ABmag
    luminosity = convert_flux(abmag, LUMINOSITY_UNIT, "sdss_r", distance=20 * u.Mpc)
    abmag_back = convert_flux(luminosity, u.ABmag, "sdss_r", distance=20 * u.Mpc)

    assert luminosity.unit == LUMINOSITY_UNIT
    assert abs(abmag_back.value - abmag.value) <= 1e-6


@pytest.mark.xfail(reason="Vega magnitudes and TransmissionCurve are not implemented.")
def test_abmag_to_vegamag():
    """
    Test that AB magnitude converts to Vega magnitude.
    """
    vegamag = convert_flux(20.0 * u.ABmag, VEGAMAG, "sdss_r")

    assert vegamag.unit == VEGAMAG
