import astropy.units as u
from astropy.units import Equivalency
from ..utils.convert_flux_units import VEGAMAG
import numpy as np
from ..utils.vega import VegaSpec


class VegaMagFluxDensityEquivalency(Equivalency):
    """
    Custom equivalency between Vega magnitude and flux density

    Attributes:
        vega_fd (astropy Quantity): Vega's flux density
    """

    def __init__(self, vega_fd):
        """Initialize the equivalency with Vega's zero-point flux density."""
        self.vega_fd = vega_fd
        self.output_unit = vega_fd.unit

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
    def vegamag_to_fd(self, vega_mag):
        """
        This function converts from Vega magnitude to flux density
        Args:
            vega_mag (floats): magnitude in Vega system
            vega_fd (floats): Vega's flux density at specified wavelength(s)
        Returns:
            Flux density as floats
        """
        return self.vega_fd.value * (10 ** (-0.4 * vega_mag))

    # Define the backward (flux_density -> mag) conversion
    def fd_to_vegamag(self, flux_density):
        """
        This function converts from flux density to Vega magnitude
        Args:
            flux_density (floats): flux density
            vega_fd (floats): Vega's flux density at specified wavelength(s)
        Returns:
            Vega magnitude as floats
        """
        return -2.5 * np.log10(flux_density / self.vega_fd.value)


class Mag:
    """
    A class to be called on for calculations and conversions involving magnitudes
    This class supports AB, ST, and Vega magnitude systems.

    Attributes:
        quantity (u.ABmag/u.STmag/VEGAMAG): Input magnitude(s)
        spectral_coordinate (astropy Quantity): central wavelength/frequency
        chosen_mag_system (astropy Units): Magnitude system to convert to.
            Default is ABmag.
        input_file_path (str, optional): path to spectrum file
        catalog (str, optional): catalog to query spectrum file from
        **spectra_kwargs: Additional keyword arguments forwarded to
            `VegaSpec.spectra()`: `wavelength_var_name`, `fluxdensity_var_name`,
            `hdul_idx`, `wavelength_unit`, `fluxdensity_unit`. See definition for each
            of them in docstrings of VegaSpec class.

    Raises:
        TypeError: if input quantity and/or spectral coordinates
            are not astropy Quantities
        UnitConversionError: if input quantity is not AB, ST, or Vega magnitudes
    """

    def __init__(
        self,
        quantity,
        spectral_coordinate,
        chosen_mag_system=u.ABmag,
        catalog=None,
        input_file_path=None,
        **spectra_kwargs,
    ):
        """Initialize the Mag class"""
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
        vega_spec = VegaSpec(
            catalog=catalog, input_file_path=input_file_path, **spectra_kwargs
        )
        wanted_vega_fd = vega_spec.spectral_density_vega(
            spectral_coordinates=spectral_coordinate
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
