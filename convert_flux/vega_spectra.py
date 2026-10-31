# Import dependencies here
from astropy.io import fits
import astropy.units as u
import numpy as np


def vega_spectra(input_file=None, catalog=None):
    """
    This function queries Vega spectrum from a user-specified or reads a FITS or text
        file and returns the wavelength and flux values of the input spectrum
    Args:
        input_file (str, optional): path to spectrum file (only supports FITS or TXT)
        catalog (str, optional): catalog to query from
    Returns:
        A tuple of two NumPy arrays (wavelength, flux)
    """
    # Do something if user wants to query Vega spectrum from surveys
    if catalog is not None:
        pass

    # Do something if user provides their own Vega spectra
    elif input_file is not None:
        pass

    # Otherwise, read template HST/STIS Vega spectrum from CALSPEC
    else:
        hdul = fits.open("vega_spectra/alpha_lyr_stis_012_template.fits")
        data = hdul[1].data

        ## Convert both wavelength and flux to astropy Quantities
        ## Wavelength is in Angstroms, flux density is in erg / (s cm^2 Angstrom)
        wavelength = u.Quantity(np.array(data["WAVELENGTH"]), unit=u.AA)
        flux_density = u.Quantity(
            np.array(data["FLUX"]), unit=u.erg / u.s / u.cm**2 / u.AA
        )

    # Return the data
    return (wavelength, flux_density)
