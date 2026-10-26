# Import dependencies here
import astropy.units as u
from astropy.cosmology import Cosmology, Planck18
import numpy as np
from convert_flux import convert_flux_units
from scipy.integrate import trapezoid
from abc import abstractmethod, ABC


def convert_flux():
    return


class Mag:
    """
    A class to be called on for calculations and conversions involving magnitudes
    This class supports AB, ST, and Vega magnitude systems.

    Attributes:
        quantity (ABmag/STmag/VEGAmag): Input magnitude(s)
        spectral_coordinate (astropy Quantity): central wavelength/frequency
        chosen_mag_system (astropy Units): Magnitude system to convert to.
            Default is ABmag.
    """

    def __init__(self, quantity, spectral_coordinate, chosen_mag_system=None):
        """
        Initialize the Mag class
        Args:
            quantity: input magnitudes
            spectral_coordinate: input central wavelength
            chosen_mag_system: magnitude system to convert to.
        Raises:
            TypeError: If either quantity or spectral_coordinate is not astropy Quantity
        """
        # Check if input magnitudes are astropy Quantities
        if not isinstance(quantity, u.Quantity):
            raise TypeError("Input magnitude must be astropy Quantity")

        # Check if input magnitudes are in AB, ST, or Vega magnitude system
        if quantity.unit not in (u.ABmag, u.STmag, convert_flux_units.VEGAMAG):
            raise u.UnitConversionError(
                "Input magnitude must be in AB, ST, or Vega system"
            )

        # Check if input spectral coordinates are astropy quantities
        if not isinstance(spectral_coordinate, u.Quantity):
            raise TypeError("Input spectral_coordinate must be astropy Quantity")

        # Define separate equivalencies if user wants to convert from/to Vega mag
        if quantity.unit == convert_flux_units.VEGAMAG:
            ## Do something once we have SourceSpectrum class ready
            return
        elif chosen_mag_system == convert_flux_units.VEGAMAG:
            ## Do something once we have SourceSpectrum class ready
            return

        # Convert from non-Vega magnitude to AB magnitude by default
        # or (non-Vega) user-specified system
        else:
            if chosen_mag_system is not None:
                self.quantity = quantity.to(
                    chosen_mag_system,
                    equivalencies=u.spectral_density(spectral_coordinate),
                )
            else:
                self.quantity = quantity.to(
                    u.ABmag, equivalencies=u.spectral_density(spectral_coordinate)
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
    This class defines the conversion between Magnitude and Flux Density
    Base units are AB magnitude for Mag and uJy for flux density

    Attributes:
        mag (astropy Quantity): magnitude
        spectral_coordinate (astropy Quantity): central wavelength
        flux_density (astropy Quantity): flux density
    """

    def __init__(self, mag=None, flux_density=None, spectral_coordinate=None):
        """
        Initialize the MagFluxDensity class
        Args:
            mag (Mag class or astropy Quantity): Magnitude in AB system
            spectral_coordinate (astropy Quantity): central wavelength/frequency
            flux_density (FluxDensity class or astropy Quantity): Flux density in uJy
        """
        # Convert magnitude to Mag class and flux density to Flux Density class
        # if not already
        if (mag is not None) and (not isinstance(mag, Mag)):
            mag = Mag(mag, spectral_coordinate)
        if (flux_density is not None) and (not isinstance(flux_density, FluxDensity)):
            flux_density = FluxDensity(flux_density, spectral_coordinate)

        self.mag = mag
        self.fd = flux_density

        return

    # Define the function to convert from magnitude to flux density
    def mag_to_flux_density(self, spectral_coordinate):
        """
        This function converts from magnitude to flux density
        Args:
            spectral_coordinate (astropy Quantity): central wavelength/frequency
        Returns:
            Flux density as FluxDensity class
        """
        # Use astropy conversion from magnitude to flux density
        astropy_mag = self.mag.quantity
        flux_density = astropy_mag.to(
            u.uJy, equivalencies=u.spectral_density(spectral_coordinate)
        )

        # Return output as FluxDensity class
        return FluxDensity(flux_density, spectral_coordinate=spectral_coordinate)

    # Define the function convert from flux density to magnitude
    def flux_density_to_mag(self, spectral_coordinate):
        """
        This function converts from flux density to magnitude
        Args:
            spectral_coordinate (astropy Quantity): central wavelength/frequency
        Returns:
            AB Magnitude as Mag class
        """
        # Use astropy conversion from flux density to magnitude
        astropy_flux_density = self.fd.quantity
        mag = astropy_flux_density.to(
            u.ABmag, equivalencies=u.spectral_density(spectral_coordinate)
        )

        # Return output as Mag class
        return Mag(mag, spectral_coordinate)


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
     A class that defines the conversion between flux and luminosity using the distance
    to the source. Base units are in erg/s/cm^2 for flux and erg/s for luminosity. Unit
    classes from Flux and Luminosity are used to ensure proper unit conversions, and
    input validation for distance is conducted to ensure it is an astropy Quantity.
    If not, a TypeError is raised. The conversion equations are then applied to
    calculate the corresponding luminosity or flux value. An option to provide a
    cosmology model and redshift is also available if desired for luminosity distance
    calculations. If no cosmology is provided, the default Planck18 cosmology is used.

    Attributes:
       flux (Flux): The flux value to be converted.
       luminosity (Luminosity): The luminosity value to be converted.
       cosmo (astropy.cosmology.Cosmology or None): Cosmology used to compute
       luminosity distance when a redshift is given.
    """

    def __init__(self, flux=None, luminosity=None, cosmo=Planck18):
        """
        Initialize the FluxLuminosity class with desired flux/luminosity quantity to
        convert and cosmology.

        Parameters:
            flux (Flux, optional): The flux value to be converted.
            luminosity (Luminosity, optional): The luminosity value to be converted.
            cosmo (astropy.cosmology.Cosmology, optional): Cosmology used to compute
            luminosity distance when a redshift is given. If None, defaults to Planck18.

        Raises:
            TypeError: If flux is not a Flux object or luminosity is not a Luminosity
            object, or if cosmo is not an instance of astropy.cosmology.Cosmology.
        """
        if flux is not None and not isinstance(flux, Flux):
            raise TypeError("flux must be a Flux object")
        if luminosity is not None and not isinstance(luminosity, Luminosity):
            raise TypeError("luminosity must be a Luminosity object")
        self.flux = flux
        self.luminosity = luminosity

        if not isinstance(cosmo, Cosmology):
            raise TypeError("cosmo must be an instance of astropy.cosmology.Cosmology")
        self.cosmo = cosmo

    def redshift_distance(self, distance, z):
        """
        Calculate the luminosity distance based on the provided redshift and cosmology
        model. If the redshift is not provided, the function returns the input distance.

        Parameters:
            distance (u.Quantity): Inputted distance to the source.
            z (float): The redshift of the source.

        Returns:
            luminosity_distance (u.Quantity): The luminosity distance based on
            the redshift and cosmology model.
        """
        if z is None:
            return distance
        return self.cosmo.luminosity_distance(z)

    def flux_to_luminosity(self, distance=None, z=None):
        """
        Convert flux to luminosity using the distance to the source.

        Parameters:
            distance (u.Quantity): The distance to the source in an Astropy Quantity.
            z (float): The redshift of the source.

        Returns:
            luminosity (Luminosity): The corresponding luminosity value.
        """
        distance = self.redshift_distance(distance, z)

        if not isinstance(distance, u.Quantity):
            raise TypeError("distance must be an Astropy quantity.")
        if not distance.unit.physical_type == "length":
            raise TypeError("distance must be a length quantity.")

        luminosity_value = self.flux.quantity * 4 * np.pi * (distance**2)
        return Luminosity(luminosity_value)

    def luminosity_to_flux(self, distance=None, z=None):
        """
        Convert luminosity to flux using the distance to the source.

        Parameters:
            distance (u.Quantity): The distance to the source in an Astropy Quantity.
            z (float): The redshift of the source.

        Returns:
            flux (Flux): The corresponding flux value.
        """
        distance = self.redshift_distance(distance, z)

        if not isinstance(distance, u.Quantity):
            raise TypeError("distance must be an Astropy quantity.")
        if not distance.unit.physical_type == "length":
            raise TypeError("distance must be a length quantity.")

        flux_value = self.luminosity.quantity / (4 * np.pi * (distance**2))
        return Flux(flux_value)


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


# utils.py SourceSpec and TransmissionCurve classes
