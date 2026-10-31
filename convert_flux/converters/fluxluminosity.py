import astropy.units as u
from astropy.cosmology import Cosmology, Planck18
import numpy as np
from ..brightness_models import Flux, Luminosity


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
