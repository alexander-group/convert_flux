# Import dependencies here
from astropy.io import fits
import astropy.units as u
import numpy as np
from pathlib import Path


def vega_spectra(
    input_file_path=None,
    wavelength_var_name=None,
    fluxdensity_var_name=None,
    catalog=None,
):
    """
    This function queries Vega spectrum from a user-specified or reads a FITS or text
        file and returns the wavelength and flux values of the input spectrum
    Args:
        input_file_path (str, optional): path to spectrum file (FITS or TXT only)
        catalog (str, optional): catalog to query from
    Returns:
        A tuple of two NumPy arrays (wavelength, flux)
    Raises:
        ValueError: if the input spectrum file is not FIT/FITS or TXT file
    """
    # Do something if user wants to query Vega spectrum from surveys
    if catalog is not None:
        pass

    # Work with spectrum file from user (if provided)
    elif input_file_path is not None:
        extension = Path(input_file_path).suffix  ## Get file extension for verification
        if extension.lower() in (".fit", ".fits"):
            pass
        elif extension.lower() == ".txt":
            pass
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
