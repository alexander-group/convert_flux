import astropy.units as u
import numpy as np
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
def test_flux_density_to_flux(central_wavelength, filter_width, expected_flux):
    wavelength_edges = u.Quantity(
        [central_wavelength - filter_width / 2, central_wavelength + filter_width / 2]
    )
    transmission = np.ones(2)

    source_flux_density = FluxDensity(3.631e-5 * u.Jy, central_wavelength)

    # Not sure yet if i like having to define the flux_density in the class call
    # and the transmission, wavelength in the conversion
    converter = FluxFluxDensity(flux_density=source_flux_density)
    flux = converter.flux_density_to_flux(
        transmission=transmission,
        wavelength=wavelength_edges,
    )

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
def test_flux_to_flux_density(central_wavelength, filter_width, measured_flux):
    converter = FluxFluxDensity(flux=Flux(quantity=measured_flux))
    wavelength_edges = u.Quantity(
        [central_wavelength - filter_width / 2, central_wavelength + filter_width / 2]
    )
    transmission = np.ones(2)

    flux_density = converter.flux_to_fluxdensity(
        transmission=transmission, wavelength=wavelength_edges
    )

    assert isinstance(flux_density, FluxDensity)

    flux_density = flux_density.quantity.to(
        u.Jy, equivalencies=u.spectral_density(flux_density.spectral_coordinate)
    )

    assert abs(flux_density - 3.631e-5 * u.Jy) < 1e-6 * u.Jy
