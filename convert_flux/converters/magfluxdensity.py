import astropy.units as u
from ..brightness_models import FluxDensity, Mag


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
