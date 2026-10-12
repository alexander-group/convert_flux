# Import dependencies here
import astropy.units as u


def convert_flux():
    return


# Set cosmology for the entire package (in the future)
# Write convert_flux function
# Implemenent Vega
# Integrate convert_flux with transmission curve package (Slack Noah before doing)


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
        # Check if input quantity are astropy quantities
        if not isinstance(quantity, u.Quantity):
            raise TypeError("Input quantity must be astropy Quantities")

        if not isinstance(spectral_coordinate, u.Quantity):
            raise TypeError("Input spectraL_coordinate must be astropy Quantities")

        # Convert to standard photometric system (AB)
        # and standard spectral coordinate (AA) if not already
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
        spectral_coordinate (astropy Quantity): central wavelength
        flux_density (astropy Quantity): flux density
    """

    def __init__(self, mag=None, flux_density=None, central_wavelength=None):
        """
        Initialize the MagFluxDensity class
        Args:
            mag (Mag class or astropy Quantity): Magnitude in AB system
            spectral_coordinate (astropy Quantity): central wavelength
            flux_density (FluxDensity class or astropy Quantity): Flux density in uJy
        """
        # Convert magnitude to Mag class and flux density to Flux Density class
        # if not already
        if (mag is not None) and (not isinstance(mag, Mag)):
            mag = Mag(mag, central_wavelength)
        if (flux_density is not None) and (not isinstance(flux_density, FluxDensity)):
            flux_density = FluxDensity(flux_density, central_wavelength)

        self.mag = mag
        self.fd = flux_density

        return

    # Define the function to convert from magnitude to flux density
    def mag_to_flux_density(self, central_wavelength):
        """
        This function converts from magnitude to flux density
        Args:
            central_wavelength (astropy Quantity): central wavelength/frequency
        Returns:
            Flux density as FluxDensity class
        """
        # Use astropy conversion from magnitude to flux density
        astropy_mag = self.mag.quantity
        flux_density = astropy_mag.to(
            u.uJy, equivalencies=u.spectral_density(central_wavelength)
        )

        # Return output as FluxDensity class
        return FluxDensity(flux_density, spectral_coordinate=central_wavelength)

    # Define the function convert from flux density to magnitude
    def flux_density_to_mag(self, central_wavelength):
        """
        This function converts from flux density to magnitude
        Args:
            central_wavelength (astropy Quantity): central wavelength/frequency
        Returns:
            Magnitude as Mag class
        """
        # Use astropy conversion from flux density to magnitude
        astropy_flux_density = self.fd.quantity
        mag = astropy_flux_density.to(
            u.ABmag, equivalencies=u.spectral_density(central_wavelength)
        )

        # Return output as Mag class
        return Mag(mag, central_wavelength)


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


# utils.py SourceSpec and TransmissionCurve classes
