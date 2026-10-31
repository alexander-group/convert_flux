import numpy as np
from ..brightness_models import FluxDensity, Flux
from scipy.integrate import trapezoid
from ..source_spec_models import FlatSpec


class FluxFluxDensity:
    """
    A class that defines the conversion between flux and flux density using the provided
    source spectrum and transmission curve data. Flux is assumed to be in units of
    erg/s/cm^2 and flux density is assumed to be in units of erg / (s cm^2 Angstrom).
    Currently, the conversions support a flat source spectrum and a top hat
    approximation for the transmission curve. Future implementation will include support
    for Lyman alpha break and power law source spectra, as well as real tranmission
    curve data using the associated package.

    Attributes:
        flux (Flux): The total flux in units of erg/s/cm^2.
        flux_density (FluxDensity): The flux density in units of erg / (s cm^2 Angstrom)
    """

    def __init__(self, flux=None, flux_density=None):
        # assume we're getting a validated flux density in erg / (s cm^2 Angstrom) or a
        # flux in erg/s/cm^2
        if flux is not None and not isinstance(flux, Flux):
            raise TypeError("flux must be a Flux object")

        if flux_density is not None and not isinstance(flux_density, FluxDensity):
            raise TypeError("flux_density must be a FluxDensity object")

        self.flux = flux
        self.fd = flux_density

    def flux_to_fluxdensity(self, transmission, wavelength, source_spec=None):
        """
        Convert Flux to FluxDensity object using the provided source spectrum and
        transmission curve.

        Parameters:
            transmission: The transmission array from TransmissionCurve (dimensionless).
            wavelength: The wavelength array corresponding to the overlapping ranges of
            source_flux and transmission (in Angstrom).
            source_spec: SourceSpec instance. Defaults to FlatSpec.

        """
        if isinstance(transmission, np.ndarray):
            if np.size(wavelength) != np.size(transmission):
                # add smooth or resample if they are not the same shape
                # (open enhancement issue)
                raise TypeError("Wavelength and transmission must have the same size")
        else:
            transmission = np.array(transmission)

        source_spec = FlatSpec() if source_spec is None else source_spec
        weighted_tranmission = transmission * source_spec.shape(wavelength)

        delta_nu = trapezoid(weighted_tranmission, wavelength)  # (bandwidth)

        flux_density = self.flux.quantity / delta_nu

        ref_wavelength = (wavelength.min() + wavelength.max()) / 2
        return FluxDensity(flux_density, ref_wavelength)

    def flux_density_to_flux(self, transmission, wavelength, source_spec=None):
        """
        Convert FluxDensity to Flux object using the provided arrays from SourceSpec
        and TransmissionCurve.

        Parameters:
            transmission: The transmission array from TransmissionCurve.
            wavelength: The wavelength array corresponding to the overlapping ranges of
            source_spec and transmission.
            source_spec: SourceSpec instance. Defaults to FlatSpec.

        """
        if isinstance(transmission, np.ndarray):
            if np.size(wavelength) != np.size(transmission):
                raise TypeError("wavelength and transmission must have the same size")
        else:
            transmission = np.array(transmission)

        source_spec = FlatSpec() if source_spec is None else source_spec
        weighted_transmission = transmission * source_spec.shape(wavelength)
        transmitted_flux = self.fd.quantity * weighted_transmission

        total_flux = trapezoid(transmitted_flux, wavelength)
        return Flux(total_flux)
