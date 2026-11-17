# Import dependencies here
from astropy.io import fits
from astropy.io import ascii
import astropy.units as u
from astropy.units import Equivalency
from convert_flux_units import VEGAMAG
import numpy as np
from pathlib import Path


# Define the equivalency between magnitudes and flux densities for Vega system
class VegaMagFluxDensityEquivalency(Equivalency):
    """
    Custom equivalency between Vega magnitude and flux density

    Attributes:
        vega_fd (astropy Quantity): Vega's flux density
    """

    def __init__(self, vega_fd):
        """
        (Super) initialize the class
        Args:
            vega_fd (astropy Quantity): Vega's flux density at specified wavelength
        Raises:
            UnitConversionError: If input flux density and Vega's flux density are not
                equivalent astropy Quantities (e.g., wavelength and frequency-based)
        """

        # Define forward (mag -> flux_density) and
        # backward (flux_density -> mag) conversions
        def vegamag_to_fd(vega_mag):
            """
            This function converts from Vega magnitude to flux density
            Args:
                vega_mag (floats): magnitude in Vega system
                vega_fd (floats): Vega's flux density at specified wavelength(s)
            Returns:
                Flux density as floats
            """
            return vega_fd.value * (10 ** (-0.4 * vega_mag))

        def fd_to_vegamag(flux_density):
            """
            This function converts from flux density to Vega magnitude
            Args:
                flux_density (floats): flux density
                vega_fd (floats): Vega's flux density at specified wavelength(s)
            Returns:
                Vega magnitude as floats
            """
            return -2.5 * np.log10(flux_density / vega_fd.value)

        # Define the equivalency tuple
        equivalency_tuple = [
            (VEGAMAG, u.erg / u.s / u.cm**2 / u.AA, vegamag_to_fd, fd_to_vegamag)
        ]

        # Initialize the parent Equivalency class with the list of conversion tuples
        super().__init__(equivalency_tuple)


# Define the function to load our template HST/STIS Vega spectrum from CALSPEC
def load_template_vega_spectrum():
    """
    This function loads the template HST/STIS CALSPEC Vega spectrum file
        to avoid redundant disk I/O on repeated calls
    Returns:
        NumPy arrays of astropy Quantities in order of (wavelength, flux_density)
    """
    template_spectrum_path = Path("vega_spectra/alpha_lyr_stis_012_template.fits")
    hdul = fits.open(template_spectrum_path)
    data = hdul[1].data

    ## Convert both wavelength and flux to astropy Quantities
    ## Wavelength is in Angstrom, flux density is in erg / (s cm^2 Angstrom)
    wavelength = u.Quantity(np.array(data["WAVELENGTH"]), unit=u.AA)
    flux_density = u.Quantity(np.array(data["FLUX"]), unit=u.erg / u.s / u.cm**2 / u.AA)

    return wavelength, flux_density


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
            return load_template_vega_spectrum()

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
            except KeyError:
                raise KeyError(
                    "Please specify keywords for wavelength and/or flux density. "
                )

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


wavelength, flux_density = VegaSpec().spectra()
print(flux_density)
vega_fd = spectral_density_vega(
    vega_spectrum=VegaSpec().spectra(), spectral_coordinates=[1500] * (u.AA)
)
