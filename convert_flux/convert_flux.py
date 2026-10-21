# Import dependencies here
import astropy.units as u
from astropy.cosmology import Cosmology, Planck18
import numpy as np
from convert_flux import convert_flux_units


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
    the spectral equivalencies. Base units are in uJy.
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
            units uJy. Must have units of flux density.
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
            u.uJy, equivalencies=u.spectral_density(spectral_coordinate)
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
    1. Conversion equations/calculation
    """

    def __init__(self, flux, flux_density):
        return


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


class SourceSpec:
    """
    Future implementation for non-flat spectrum
    """

    def __init__(self, wavelength, flux):
        self.flux = 1


# utils.py SourceSpec and TransmissionCurve classes
