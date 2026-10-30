import astropy.units as u
from ..convert_flux_units import VEGAMAG


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
        if quantity.unit not in (u.ABmag, u.STmag, VEGAMAG):
            raise u.UnitConversionError(
                "Input magnitude must be in AB, ST, or Vega system"
            )

        # Check if input spectral coordinates are astropy quantities
        if not isinstance(spectral_coordinate, u.Quantity):
            raise TypeError("Input spectral_coordinate must be astropy Quantity")

        # Define separate equivalencies if user wants to convert from/to Vega mag
        if quantity.unit == VEGAMAG:
            ## Do something once we have SourceSpectrum class ready
            return
        elif chosen_mag_system == VEGAMAG:
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
