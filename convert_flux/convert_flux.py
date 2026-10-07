"""
The main function of the package, a single function to convert fluxes,
flux densities, and magnitudes
"""

import astropy.units as u


def convert_flux():
    return


class Mag:
    """
    1. Input validation
    2. Convert to a stand unit
    Thomas
    """

    def __init__(self, value, unit):
        return


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
    1. Input validation
    2. Convert to a stand unit
    Nayera
    """

    def __init__(self, value, unit):
        return


class MagFluxDensity:
    """
    1. Conversion equations/calculation


    """

    def __init__(self, mag, flux_density):
        return


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
