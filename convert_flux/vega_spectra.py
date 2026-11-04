# Import dependencies here
from astropy.io import fits
import astropy.units as u
import numpy as np
from pathlib import Path


# Define a function to work with Vega spectrum file
# and return arrays of wavelength and flux density values
def vega_spectra(
    input_file_path=None,
    wavelength_var_name=None,
    fluxdensity_var_name=None,
    hdul_idx=None,
    catalog=None,
):
    """
    This function queries Vega spectrum from a user-specified or reads a FIT/FITS or TXT
        file and returns the wavelength and flux values of the input spectrum
    Args:
        input_file_path (str, optional): path to spectrum file (FIT/FITS or TXT only)
        catalog (str, optional): catalog to query from
        wavelength_var_name (str, optional): variable for wavelength in user-inputted
            spectrum file. Must be provided if input_file_path is not None
        fluxdensity_var_name (str, optional): variable for flux density in user-inputted
            spectrum file. Must be provided if input_file_path is not None
        hdul_idx (int, optional): index of HDUL in FIT/FITS file with spectrum data.
            Must be provided if input file is .fit/.fits file
    Returns:
        A tuple of two NumPy arrays (wavelength, flux)
    Raises:
        ValueError: if the input spectrum file is not FIT/FITS or TXT file
        KeyError: if the keywords for wavelength and flux density or index of HDUL (of
            FIT/FITS file) with spectru data is missing
    """
    # Do something if user wants to query Vega spectrum from surveys
    if catalog is not None:
        pass

    # Work with spectrum file from user (if provided)
    elif input_file_path is not None:
        ## Raise error if keyword for wavelength or flux density is missing
        if wavelength_var_name is None or fluxdensity_var_name is None:
            raise KeyError("Please provide keyword(s) for wavelength and flux density.")

        ## Get file extension for verification
        extension = Path(input_file_path).suffix

        ## Work with FIT/FITS file
        if extension.lower() in (".fit", ".fits"):
            if hdul_idx is None:
                raise KeyError("Please provide index of HDUL with spectrum data.")
            else:
                hdul = fits.open(input_file_path)
                data = hdul[hdul_idx].data

        ## Work with TXT file
        elif extension.lower() == ".txt":
            pass

        ## Raise error if input spectrum file is not supported
        else:
            raise ValueError(
                "Invalid file extension. Only .fit/.fits or .txt files are supported."
            )

    # Otherwise, use template HST/STIS Vega spectrum (900-3e6 AA) from CALSPEC
    else:
        hdul = fits.open("vega_spectra/alpha_lyr_stis_012_template.fits")
        data = hdul[1].data

        ## Convert both wavelength and flux to astropy Quantities
        ## Wavelength is in Angstrom, flux density is in erg / (s cm^2 Angstrom)
        wavelength = u.Quantity(np.array(data["WAVELENGTH"]), unit=u.AA)
        flux_density = u.Quantity(
            np.array(data["FLUX"]), unit=u.erg / u.s / u.cm**2 / u.AA
        )

    # Return the data
    return (wavelength, flux_density)


print(vega_spectra()[0])
