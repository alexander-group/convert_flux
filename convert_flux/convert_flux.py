# Import packages here
import astropy.units as u
from astropy.cosmology import Cosmology, Planck18
import numpy as np


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
    1. Conversion equations/calculation


    """

    def __init__(self, mag, flux_density):
        return


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

    def __init__(self, flux=None, luminosity=None, cosmo=None):
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

        if cosmo is None:
            # default cosmology is Planck18
            cosmo = Planck18
        elif not isinstance(cosmo, Cosmology):
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
