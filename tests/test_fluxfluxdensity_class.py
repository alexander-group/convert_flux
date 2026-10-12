"""Top-hat flux and flux-density conversions for the two r-band filters."""

import astropy.units as u
import pytest

from convert_flux.convert_flux import Flux, FluxDensity, FluxFluxDensity


@pytest.mark.parametrize(
    "central_wavelength, filter_width, expected_flux",
    [
        (6187 * u.Angstrom, 1130 * u.Angstrom, 3.22e-14 * u.erg / u.s / u.cm**2),
        (6436 * u.Angstrom, 1553 * u.Angstrom, 4.08e-14 * u.erg / u.s / u.cm**2),
    ],
    ids=["sdss_r", "ztf_r"],
)
@pytest.mark.xfail(
    reason="FluxFluxDensity conversion is not implemented yet", strict=True
)
def test_flux_density_to_flux(central_wavelength, filter_width, expected_flux):
    flux_density = FluxDensity(
        quantity=3.631e-5 * u.Jy, spectral_coordinate=central_wavelength
    )
    converter = FluxFluxDensity(flux=None, flux_density=flux_density)

    flux = converter.flux_density_to_flux(filter_width=filter_width)

    assert isinstance(flux, Flux)
    assert abs(flux.quantity - expected_flux) < 1e-15 * u.erg / u.s / u.cm**2


@pytest.mark.parametrize(
    "central_wavelength, filter_width, measured_flux",
    [
        (6187 * u.Angstrom, 1130 * u.Angstrom, 3.22e-14 * u.erg / u.s / u.cm**2),
        (6436 * u.Angstrom, 1553 * u.Angstrom, 4.08e-14 * u.erg / u.s / u.cm**2),
    ],
    ids=["sdss_r", "ztf_r"],
)
@pytest.mark.xfail(
    reason="FluxFluxDensity conversion is not implemented yet", strict=True
)
def test_flux_to_flux_density(central_wavelength, filter_width, measured_flux):
    converter = FluxFluxDensity(flux=Flux(quantity=measured_flux), flux_density=None)

    flux_density = converter.flux_to_fluxdensity(
        spectral_coordinate=central_wavelength, filter_width=filter_width
    )

    assert isinstance(flux_density, FluxDensity)
    assert abs(flux_density.quantity - 3.631e-5 * u.Jy) < 1e-7 * u.Jy
