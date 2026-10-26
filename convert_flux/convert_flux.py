# Import packages here
import astropy.units as u
import numpy as np
from scipy.integrate import trapezoid
from abc import abstractmethod, ABC


def convert_flux():
    return


class Mag:
    """
    A class to be called on for calculations and conversions involving magnitudes
    This class supports AB, ST, and Vega (to be worked on) magnitude system

    Attributes:
        quantity (astropy Quantity): Input magnitude(s)
        spectral_coordinate (astropy Quantity): central wavelength(s) of the \
            observing band
    """

    def __init__(self, quantity, spectral_coordinate):
        """
        Initialize the Mag class
        Args:
            quantity: input magnitudes
            spectral_coordinate: input central wavelength
        Raises:
            TypeError: If either quantity or spectral_coordinate is not astropy Quantity
        """
        # Look into LogUnit
        # Check if input quantity are astropy quantities
        if not isinstance(quantity, u.Quantity):
            raise TypeError("Input quantity must be astropy Quantities")

        if not isinstance(spectral_coordinate, u.Quantity):
            raise TypeError("Input spectraL_coordinate must be astropy Quantities")

        # Convert to standard photometric system (AB)
        # and standard spectral coordinate (AA)
        self.quantity = quantity.to(
            u.ABmag, equivalencies=u.spectral_density(spectral_coordinate)
        )
        self.spectral_coordinate = spectral_coordinate.to(
            u.Angstrom, equivalencies=u.spectral()
        )


class Flux:
    """
    A class that defines flux as an Astropy Quantity. Base units are in erg/s/cm^2.

    Attributes:
        Astropy Quantity (value + unit)
    """

    def __init__(self, quantity):
        """
        Initialize function that defines the Flux object
        with an Astropy Quantity.

        Parameters:
            quantity (u.Quantity): The flux quantity to be converted to standard
            units in erg/s/cm^2.

        Raises:
            TypeError: If the input is not an Astropy Quantity.
        """
        if not isinstance(quantity, u.Quantity):
            raise TypeError("Quantity input must be an Astropy Quantity.")

        self.quantity = quantity.to(u.erg / u.s / u.cm**2)


class Luminosity:
    """
    A class that defines luminosity as an Astropy Quantity. Base units are in erg/s.

    Attributes:
        Astropy Quantity (value + unit)
    """

    def __init__(self, quantity):
        """
        Initialize function that defines the Luminosity object
        with an Astropy Quantity.

        Parameters:
            quantity (u.Quantity): The luminosity quantity to be
            converted to standard units in erg/s.

        Raises:
            TypeError: If the input is not an Astropy Quantity.
        """
        if not isinstance(quantity, u.Quantity):
            raise TypeError("Quantity input must be an Astropy Quantity.")

        self.quantity = quantity.to(u.erg / u.s)


class FluxDensity:
    """
    A class that defines flux density as an Astropy Quantity and converts
    between wavelength based flux density and frequency based flux density using
    the spectral equivalencies. Base units are in erg / (s cm^2 Angstrom).
    Attributes:
        Astropy Quantity (value + unit),
        Spectral Coordinate (wavelength or frequency)
    """

    def __init__(self, quantity, spectral_coordinate):
        """
        Initialize function that defines the FluxDensity object
        with an Astropy Quantity and spectral coordinate.

        Parameters:
            quantity (u.Quantity): The flux desnity quantity to be converted to standard
            units erg / (s cm^2 Angstrom). Must have units of flux density.
            spectral_coordinate (u.Quantity): represents the wavelength or frequency
            where the flux density is measured. Must have units of wavelength or
            frequency.

        Raises:
            TypeError: If the input is not an Astropy Quantity.
        """
        # Input validation: check if inputs are astropy Quantities
        if not isinstance(quantity, u.Quantity):
            raise TypeError("quantity input must be an astropy Quantity")

        if not isinstance(spectral_coordinate, u.Quantity):
            raise TypeError("spectral_coordinate input must be an astropy Quantity")

        self.spectral_coordinate = spectral_coordinate.to(
            u.Angstrom, equivalencies=u.spectral()
        )  # throws error if not equiv to wavelength/freq
        self.quantity = quantity.to(
            u.erg / (u.s * u.cm**2 * u.Angstrom),
            equivalencies=u.spectral_density(spectral_coordinate),
        )


class MagFluxDensity:
    """
    1. Conversion equations/calculation

    """

    def __init__(self, mag, flux_density):
        return


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


class FluxLuminosity:
    """
    1. Conversion equations/calculation
    """

    def __init__(self, flux, luminosity):
        return


class SourceSpec(ABC):
    """
    Abstract Base Class for all source spectrum types
    The shape is evaluated on the same wavelength grid as the transmission curve.
    """

    def shape(self, wavelength):
        # Return one value per wavelength
        if not isinstance(wavelength, u.Quantity):
            raise TypeError("wavelength must be an astropy Quantity")

        wavelength = wavelength.to(u.Angstrom)

        fluxes = np.asarray(self._shape(wavelength), dtype=float)

        return fluxes

    @abstractmethod
    def _shape(self, wavelength):
        # Evaluate the subclass's dimensionless shape on a validated grid.
        pass


class FlatSpec(SourceSpec):
    """
    Subclass of SourceSpec ABC to define an appromixately flat source spectrum
    """

    def _shape(self, wavelength):
        return np.ones(wavelength.shape, dtype=float)


class LymASpec(SourceSpec):
    """
    Subclass of SourceSpec ABC to define a Lymna alpha break source spectrum
    """

    pass


class PolySpec(SourceSpec):
    """
    Subclass of SourceSpec ABC to define an approximately polynomial source spectrum
    """

    pass


class TransmissionCurve:
    """
    Future implementation for transmission curve
    (In wavelength space)
    Will interact with transmission info package
    """

    def __init__(self, wavelength, transmission):
        # will be an array eventually
        self.transmission = 1
