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

        if self.catalog is not None:
            raise NotImplementedError("Query option is not supported currently.")

        if self.input_file is None:
            return self.load_template_vega_spectrum()

        # Validate if the user inputs the required arguments
        self._validate_file_inputs(
            wavelength_var_name,
            fluxdensity_var_name,
            wavelength_unit,
            fluxdensity_unit,
        )

        # Validate file type
        path = Path(self.input_file)
        extension = path.suffix.lower()

        # Work with FIT/FITS file
        if extension in (".fit", ".fits"):
            wavelength, flux_density = self._read_fits_spectrum(
                path,
                hdul_idx,
                wavelength_var_name,
                fluxdensity_var_name,
                wavelength_unit,
                fluxdensity_unit,
            )

        # Work with TXT file
        elif extension == ".txt":
            wavelength, flux_density = self._read_ascii_spectrum(
                path,
                wavelength_var_name,
                fluxdensity_var_name,
                wavelength_unit,
                fluxdensity_unit,
            )

        # Raise error if user inputs unsupported file types
        else:
            raise ValueError(
                "Invalid file extension. Only .fit/.fits or .txt files are supported."
            )

        return self._standardize_units(wavelength, flux_density)

    @classmethod
    def spectral_density_vega(
        cls,
        spectral_coordinates,
        catalog=None,
        input_file_path=None,
        **spectra_kwargs,
    ):
        """Finds Vega flux densities at specified spectral coordinates

        Args:
            spectral_coordinates (astropy.units.Quantity): Wavelength or frequency
                at which to evaluate Vega's flux density.
            **spectra_kwargs: Optional keyword arguments forwarded to `self.spectra()`
                when loading a custom input file.

        Returns:
            astropy.units.Quantity: Vega flux density
        """
        instance = cls(catalog=catalog, input_file_path=input_file_path)
        vega_spectral_coord, vega_fd = instance.spectra(**spectra_kwargs)

        converted_spectral_coordinates = u.Quantity(spectral_coordinates).to(
            vega_spectral_coord.unit,
            equivalencies=u.spectral_density(vega_spectral_coord),
        )

        diff_matrix = np.abs(
            vega_spectral_coord[None, :]
            - np.atleast_1d(converted_spectral_coordinates)[:, None]
        )
        wanted_idx = np.argmin(diff_matrix, axis=1)

        result = vega_fd[wanted_idx]
        return result

    @staticmethod
    def _validate_file_inputs(
        wavelength_var_name,
        fluxdensity_var_name,
        wavelength_unit,
        fluxdensity_unit,
    ):
        """Validates required column names and Astropy units for user-supplied files."""
        if not wavelength_var_name or not fluxdensity_var_name:
            raise KeyError("Please provide keywords for wavelength and flux density.")

        if wavelength_unit is None or fluxdensity_unit is None:
            raise AttributeError(
                "Please provide units for wavelength and flux density in astropy Units."
            )

    @staticmethod
    def _read_fits_spectrum(
        path,
        hdul_idx,
        wavelength_var_name,
        fluxdensity_var_name,
        wavelength_unit,
        fluxdensity_unit,
    ):
        """Extracts wavelength and flux density Quantities from a FITS HDU."""
        if hdul_idx is None:
            raise KeyError("Please provide index of HDUL with spectrum data.")

        with fits.open(path, memmap=True) as hdul:
            data = hdul[hdul_idx].data
            wavelength = u.Quantity(
                data[wavelength_var_name], unit=wavelength_unit, copy=True
            )
            flux_density = u.Quantity(
                data[fluxdensity_var_name], unit=fluxdensity_unit, copy=True
            )
        return wavelength, flux_density

    @staticmethod
    def _read_ascii_spectrum(
        path,
        wavelength_var_name,
        fluxdensity_var_name,
        wavelength_unit,
        fluxdensity_unit,
    ):
        """Extracts wavelength and flux density Quantities from an ASCII/TXT table."""
        data = ascii.read(path)
        wavelength = u.Quantity(
            data[wavelength_var_name], unit=wavelength_unit, copy=False
        )
        flux_density = u.Quantity(
            data[fluxdensity_var_name], unit=fluxdensity_unit, copy=False
        )
        return wavelength, flux_density

    @classmethod
    def _standardize_units(cls, wavelength, flux_density):
        """Converts flux density to erg / (s cm^2 Angstrom) if needed."""
        if flux_density.unit != cls.STANDARD_FLUX_UNIT:
            flux_density = flux_density.to(
                cls.STANDARD_FLUX_UNIT,
                equivalencies=u.spectral_density(wavelength),
            )
        return wavelength, flux_density
