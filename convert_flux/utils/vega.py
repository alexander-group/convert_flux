# Import dependencies here
from astropy.io import fits
from astropy.io import ascii
import astropy.units as u
import numpy as np
from pathlib import Path


class VegaSpec:
    """
    A class that loads input file from user/ query from online catalogs and
        returns Vega's spectrum (wavelength, flux density)

    Attributes:
        input_file (str, optional): path to spectrum file (FIT/FITS or TXT only)
        catalog (str, optional): catalog to query spectrum file from

    Returns:
        Numpy array of Vega flux densities
    """

    def __init__(self, catalog=None, input_file_path=None):
        """
        Initialize the class
        Args:
            input_file_path (str, optional): path to spectrum file
            catalog (str, optional): catalog to query spectrum file from
        """
        self.catalog = catalog
        self.input_file = input_file_path

        return

    # Define the function to load our template HST/STIS Vega spectrum from CALSPEC
    def load_template_vega_spectrum(self):
        """
        This function loads the template HST/STIS CALSPEC Vega spectrum file
            to avoid redundant disk I/O on repeated calls
        Returns:
            NumPy arrays of astropy Quantities in order of (wavelength, flux_density)
        """
        template_spectrum_path = Path(
            "convert_flux/vega_spectra/alpha_lyr_stis_012_template.fits"
        )
        hdul = fits.open(template_spectrum_path)
        data = hdul[1].data

        ## Convert both wavelength and flux to astropy Quantities
        ## Wavelength is in Angstrom, flux density is in erg / (s cm^2 Angstrom)
        wavelength = u.Quantity(np.array(data["WAVELENGTH"]), unit=u.AA)
        flux_density = u.Quantity(
            np.array(data["FLUX"]), unit=u.erg / u.s / u.cm**2 / u.AA
        )

        return wavelength, flux_density

    def spectra(
        self,
        wavelength_var_name=None,
        fluxdensity_var_name=None,
        hdul_idx=None,
        wavelength_unit=None,
        fluxdensity_unit=None,
    ):
        """
        This function queries Vega spectrum from a user-specified or reads a FIT/FITS
            or TXT file and returns the wavelength and flux values of the  spectrum
        Args:
            wavelength_var_name (str, optional): variable for wavelength in
                spectrum file. Must be provided if input_file_path is not None
            fluxdensity_var_name (str, optional): variable for flux density in
                spectrum file. Must be provided if input_file_path is not None
            hdul_idx (int, optional): index of HDUL in FIT/FITS file with spectrum data.
                Must be provided if input file is .fit/.fits file
            wavelength_unit (astropy Units, optional): Wavelength unit in
                spectrum file. Must be provided if input_file_path is not None
            fluxdensity_var_name (astropy Units, optional): Flux density unit in
                spectrum file. Must be provided if input_file_path is not None
        Returns:
            A tuple of two NumPy arrays (wavelength, flux) of astropy quantities
        Raises:
            ValueError: if the input spectrum file is not FIT/FITS or TXT file
            KeyError: if the keywords for wavelength/ flux density or index of HDUL (of
                FIT/FITS file) with spectru data is missing
            AttributeError: if astropy Units for wavelength or flux density in
                spectrum file is missing.
        """
        # Catalog querying is not supported right now.
        # Come back to this after pitch.
        if self.catalog is not None:
            raise NotImplementedError("Query option is not supported currently.")

        # Return template spectrum if no file is specified
        if self.input_file is None:
            return self.load_template_vega_spectrum()

        # Raise errors for missing information related to user input file
        if not wavelength_var_name or not fluxdensity_var_name:
            raise KeyError("Please provide keywords for wavelength and flux density.")

        if wavelength_unit is None or fluxdensity_unit is None:
            raise AttributeError(
                "Please provide units for wavelength and flux density in astropy Units."
            )

        # Check input file
        path = Path(self.input_file)
        extension = path.suffix.lower()

        # OPTIMIZE THIS PORTION AS MUCH AS POSSIBLE. COME BACK AFTER PITCH IF NECESSARY.

        # Work with FIT/FITS file
        if extension in (".fit", ".fits"):
            try:
                with fits.open(path, memmap=True) as hdul:
                    data = hdul[hdul_idx].data
                    wavelength = u.Quantity(
                        data[wavelength_var_name], unit=wavelength_unit, copy=True
                    )
                    flux_density = u.Quantity(
                        data[fluxdensity_var_name], unit=fluxdensity_unit, copy=True
                    )
            except hdul_idx is None:
                raise KeyError("Please provide index of HDUL with spectrum data.")

        # Work on TXT file
        elif extension == ".txt":
            data = ascii.read(path)
            wavelength = u.Quantity(
                data[wavelength_var_name], unit=wavelength_unit, copy=False
            )
            flux_density = u.Quantity(
                data[fluxdensity_var_name], unit=fluxdensity_unit, copy=False
            )

        # Raise error for unsupported file types
        else:
            raise ValueError(
                "Invalid file extension. Only .fit/.fits or .txt files are supported."
            )

        # Convert flux density and wavelength to our standard units if necessary
        if flux_density.unit != u.erg / u.s / u.cm**2 / u.AA:
            flux_density = flux_density.to(
                u.erg / u.s / u.cm**2 / u.AA,
                equivalencies=u.spectral_density(wavelength),
            )

        return wavelength, flux_density


# Define the function to look for Vega flux density at specified wavelengths
def spectral_density_vega(vega_spectrum, spectral_coordinates):
    """
    This function takes in a Vega spectrum (wavelength, flux density) and look for
        corresponding flux densities at specified wavelenths
    Args:
        vega_spectrum (tuple): A tuple in the order of
            (wavelength/frequency, flux density) representing Vega's spectrum.
            Both must be numpy arrays of astropy Quantities.
        spectral_coordinates (numpy array of astropy Quantities): Spectral coordinate(s)
            to find the corresponding Vega flux density
    Returns:
        Numpy array of Vega flux densities
    """
    # Get Vega spectrum (wavelength, flux density)
    vega_spectral_coord, vega_fd = vega_spectrum

    # Match input spectral coordinates to Vega spectrum's spectral coordinates
    converted_spectral_coordinates = u.Quantity(spectral_coordinates).to(
        vega_spectral_coord.unit, equivalencies=u.spectral_density(vega_spectral_coord)
    )

    # Create a 2D pairwise difference matrix
    diff_matrix = np.abs(
        vega_spectral_coord[None, :]
        - np.atleast_1d(converted_spectral_coordinates)[:, None]
    )

    # Find the closest Vega index for every target wavelength simultaneously
    wanted_idx = np.argmin(diff_matrix, axis=1)

    # Return scalar if input was scalar, otherwise return array
    result = vega_fd[wanted_idx]
    return result


# wavelength, flux_density = VegaSpec().spectra()
# print(flux_density)
# vega_fd = spectral_density_vega(
#     vega_spectrum=VegaSpec().spectra(), spectral_coordinates=[1500] * (u.AA)
# )
