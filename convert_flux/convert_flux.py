# Import dependencies here
import numpy as np
import astropy.units as u


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
    This class defines the conversion between Magnitude and Flux Density
    Base units are AB magnitude for Mag and uJy for flux density

    Attributes:
        mag (astropy Quantity): magnitude
        flux_density (astropy Quantity): flux density
    """

    def __init__(self, mag, flux_density):
        """
        Initialize the MagFluxDensity class
        Args:
            mag (astropy Quantity): Magnitude in AB system
            flux_density (astropy Quantity): Flux density in uJy
        """
        # Convert magnitude to Mag class and flux density to Flux Density class
        # if not already
        if not isinstance(mag, Mag):
            mag = Mag(mag)
        if not isinstance(flux_density, FluxDensity):
            flux_density = FluxDensity(flux_density)

        self.mag = mag
        self.fd = flux_density

        return

    # Define the function to convert from magnitude to flux density
    def mag_to_flux_density(self):
        """
        This function converts from magnitude to flux density
        Args:
            None
        Returns:
            Flux density as Flux Density class
        """
        return FluxDensity(3631 * 10 ** (-0.4 * self.mag))

    # Define the function convert from flux density to magnitude
    def flux_density_to_mag(self):
        """
        This function converts from flux density to magnitude
        Args:
            None
        Returns:
            Magnitude as Mag class
        """
        return Mag(-2.5 * np.log10(self.fd / 3631.0))


class FluxFluxDensity:
    """
    1. Conversion equations/calculation
    2. Transmission curve file reading function
    3. Call to Source spectrum class

    """

    def __init__(self, flux, flux_density):
        return


class FluxLuminosity:
    """
    1. Conversion equations/calculation
    """

    def __init__(self, flux, luminosity):
        return


class SourceSpec:
    """
    Future implementation for non-flat spectrum
    """

    def __init__(self, wavelength, flux):
        self.flux = 1
