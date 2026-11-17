import astropy.units as u
from astropy.units import Equivalency
from ..utils.convert_flux_units import VEGAMAG
import numpy as np
from ..utils.vega import VegaSpec, spectral_density_vega


class VegaMagFluxDensityEquivalency(Equivalency):
    """
    Custom equivalency between Vega magnitude and flux density

    Attributes:
        vega_fd (astropy Quantity): Vega's flux density
    """

    vega_fd = None

    def __init__(self, vega_fd):
        """Initialize the equivalency with Vega's zero-point flux density."""
        self.vega_fd = vega_fd
        self.output_unit = vega_fd.unit

        # Store on the class so @classmethod callbacks can access cls.vega_fd
        type(self).vega_fd = vega_fd.to(self.output_unit)
        self.vega_fd = type(self).vega_fd

        # Define the equivalency tuple
        equivalency_tuple = [
            (
                VEGAMAG.physical_unit,
                self.output_unit,
                self.vegamag_to_fd,
                self.fd_to_vegamag,
            )
        ]

        # Initialize the parent Equivalency class with the list of conversion tuples
        super().__init__(
            equivalency_tuple, name="vega_flux", kwargs={"flux0": self.vega_fd}
        )

    # Define the forward (mag -> flux_density) conversion
    @classmethod
    def vegamag_to_fd(cls, vega_mag):
        """
        This function converts from Vega magnitude to flux density
        Args:
            vega_mag (floats): magnitude in Vega system
            vega_fd (floats): Vega's flux density at specified wavelength(s)
        Returns:
            Flux density as floats
        """
        return cls.vega_fd.value * (10 ** (-0.4 * vega_mag))

    # Define the backward (flux_density -> mag) conversion
    @classmethod
    def fd_to_vegamag(cls, flux_density):
        """
        This function converts from flux density to Vega magnitude
        Args:
            flux_density (floats): flux density
            vega_fd (floats): Vega's flux density at specified wavelength(s)
        Returns:
            Vega magnitude as floats
        """
        return -2.5 * np.log10(flux_density / cls.vega_fd.value)

    # Define the equivalency tuple
    equivalency_tuple = [
        (
            VEGAMAG.physical_unit,
            u.erg / u.s / u.cm**2 / u.AA,
            vegamag_to_fd,
            fd_to_vegamag,
        )
    ]


class Mag:
    """
    A class to be called on for calculations and conversions involving magnitudes
    This class supports AB, ST, and Vega magnitude systems.

    Attributes:
        quantity (u.ABmag/u.STmag/VEGAMAG): Input magnitude(s)
        spectral_coordinate (astropy Quantity): central wavelength/frequency
        chosen_mag_system (astropy Units): Magnitude system to convert to.
            Default is ABmag.
    """

    def __init__(self, quantity, spectral_coordinate, chosen_mag_system=u.ABmag):
        """
        Initialize the Mag class
        Args:
            quantity: input magnitudes
            spectral_coordinate: input central wavelength
            chosen_mag_system: magnitude system to convert to.
        Raises:
            TypeError: If quantity or spectral_coordinate is not astropy Quantity
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

        # Define a custom equivalency for conversions involving Vega magnitudes
        wanted_vega_fd = spectral_density_vega(
            vega_spectrum=VegaSpec().spectra(), spectral_coordinates=spectral_coordinate
        )
        vega_equivalency = VegaMagFluxDensityEquivalency(wanted_vega_fd)

        # Assign the custom equivalency for Vega magnitude
        # Otherwise, assign the default spectral_density equivalency
        input_equiv = (
            vega_equivalency
            if quantity.unit == VEGAMAG
            else u.spectral_density(spectral_coordinate)
        )
        output_equiv = (
            vega_equivalency
            if chosen_mag_system == VEGAMAG
            else u.spectral_density(spectral_coordinate)
        )

        # Convert from input magnitude to output magnitude through flux density
        input_fd = quantity.to(u.erg / u.s / u.cm**2 / u.AA, equivalencies=input_equiv)
        self.quantity = input_fd.to(chosen_mag_system, equivalencies=output_equiv)
