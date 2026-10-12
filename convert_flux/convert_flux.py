# Import packages here
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
    1. Conversion equations/calculation

    """

    def __init__(self, mag, flux_density):
        return


class FluxFluxDensity:
    """
    Variables:
    Flux, FluxDensity, SourceSpec, TransmissionCurve, ?
    function flux_to_fluxdensity(Flux, SourceSpec, TransmissionCurve)
    function flux_density_to_flux(FluxDensity, SourceSpec, TransmissionCurve)
    define an astropy equivalency using the transmission curve
    for now: use a transmission curve of
    *if the source spectrum is flat, multiply the transmission data by 1, if it's not
    (for ex, a lyman alpha break) then it won't be 1 and we want to be able to account
    for that
    use SourceSpec class as if it is already implemented to take in the source spec
    data, use scipy to integrate the transmission curve
    """

    def __init__(self, flux=None, flux_density=None):
        # assume we're getting a validated flux desnity in uJy or a flux  in erg/s/cm^2
        self.flux = flux
        self.fd = flux_density
        return

    def flux_to_fluxdensity(self, convolved_info):
        """
        Convert flux to flux density using the provided convolved info from SourceSpec
        and TransmissionCurve.
        F_nu=F / delta_nu for tophat approximation

        Parameters:
            convolved_info (tuple): A tuple containing the convolved information from
            SourceSpec and TransmissionCurve.

        """
        flux_density = self.flux.quantity / convolved_info[1]  # delta_nu
        return FluxDensity(flux_density)

    def flux_density_to_flux(self, convolved_info):
        """
        Convert flux density to flux using the provided convolved info from SourceSpec
        and TransmissionCurve.
        F=F_nu * delta_nu for tophat approximation

        Parameters:
            convolved_info (tuple): A tuple containing the convolved information from
            SourceSpec and TransmissionCurve.

        """

        flux = self.fd.quantity * convolved_info[1]  # delta_nu
        return Flux(flux)


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


class TransmissionCurve:
    """
    Future implementation for transmission curve
    """

    def __init__(self, wavelength, transmission):
        self.transmission = 1
