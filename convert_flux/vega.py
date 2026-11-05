# Import dependencies here
from astropy.io import fits
from astropy.io import ascii
import astropy.units as u
import numpy as np
from pathlib import Path


# Define a function to work with Vega spectrum file
def vega_spectra(
    catalog=None,
    input_file_path=None,
    wavelength_var_name=None,
    fluxdensity_var_name=None,
    hdul_idx=None,
    wavelength_unit=None,
    fluxdensity_unit=None,
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
        wavelength_unit (astropy Units, optional): Wavelength unit in user-inputted
            spectrum file. Must be provided if input_file_path is not None
        fluxdensity_var_name (astropy Units, optional): Flux density unit in
            user-inputted spectrum file. Must be provided if input_file_path is not None
    Returns:
        A tuple of two NumPy arrays (wavelength, flux) of astropy quantities
    Raises:
        ValueError: if the input spectrum file is not FIT/FITS or TXT file
        KeyError: if the keywords for wavelength/ flux density or index of HDUL (of
            FIT/FITS file) with spectru data is missing
        AttributeError: if astropy Units for wavelength or flux density in user-inputted
            spectrum file is missing.
    """
    # Do something if user wants to query Vega spectrum from surveys
    if catalog is not None:
        pass

    # Work with spectrum file from user (if provided)
    elif input_file_path is not None:
        ## Raise error if keyword for wavelength or flux density is missing
        if wavelength_var_name is None or fluxdensity_var_name is None:
            raise KeyError("Please provide keywords for wavelength and flux density.")

        ## Raise error if astropy Units for wavelength or flux density is missing
        if wavelength_unit is None or fluxdensity_unit is None:
            raise AttributeError(
                "Please provide units for wavelength and flux density in astropy Units"
            )

        ## Get file extension for verification
        extension = Path(input_file_path).suffix

        ## Work with FIT/FITS file
        if extension.lower() in (".fit", ".fits"):
            ### Raise error if index of HDUL with spectrum data is missing
            if hdul_idx is None:
                raise KeyError("Please provide index of HDUL with spectrum data.")
            else:
                hdul = fits.open(input_file_path)
                data = hdul[hdul_idx].data

                ## Convert both wavelength and flux to astropy Quantities
                wavelength = u.Quantity(
                    np.array(data[wavelength_var_name]), unit=wavelength_unit
                )
                flux_density = u.Quantity(
                    np.array(data[fluxdensity_var_name]), unit=fluxdensity_unit
                )

        ## Work with TXT file
        elif extension.lower() == ".txt":
            data = ascii.read(input_file_path)

            ## Convert both wavelength and flux to astropy Quantities
            wavelength = u.Quantity(
                np.array(data[wavelength_var_name]), unit=wavelength_unit
            )
            flux_density = u.Quantity(
                np.array(data[fluxdensity_var_name]), unit=fluxdensity_unit
            )

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

    # Convert flux density to erg/s/cm^2/Angstrom if not already
    if flux_density.unit != u.erg / u.s / u.cm**2 / u.AA:
        flux_density = flux_density.to(
            u.erg / u.s / u.cm**2 / u.AA, equivalencies=u.spectral_density(wavelength)
        )

    # Return the data
    return (wavelength, flux_density)


# test = vega_spectra()[0] - [100, 200, 300]* u.AA
# print(np.argmin(test))


# Define the function to look for Vega flux density at specified wavelengths
def spectral_density_vega(wavelengths, vega_spectrum):
    """
    This function takes in a Vega spectrum (wavelength, flux density) and look for
        corresponding flux densities at specified wavelenths
    Args:
        vega_spectrum (tuple): A tuple in the order of (wavelength, flux density) that
            represents the spectrum of Vega. Best if using output by the function
            vega_spectra, but otherwise, both wavelength and flux density must be
            numpy array of astropy Quantities.
        wavelengths (numpy array of astropy Quantities): Wavelength(s) to find the
            corresponding Vega flux density
    Returns:
        Numpy array of Vega flux densities
    """
    ## Array to store Vega flux densities
    wanted_vega_fd = np.zeros_like(wavelengths)

    # Get Vega spectrum (wavelength, flux density)
    vega_wavelength, vega_fd = vega_spectrum[0], vega_spectrum[1]

    # Look for flux densities at specified wavelengths
    for i in range(len(wavelengths)):
        ## Find the closest wavelength in the Vega spectrum to the desired wavelength
        wav = wavelengths[i]
        wavelength_diff = np.abs(vega_wavelength.value - wav)
        wanted_idx = np.argmin(wavelength_diff)

        ## Find the Vega flux density at corresponding wavelength and add to output
        wanted_vega_fd[i] = vega_fd[wanted_idx]

    # Return the array with wanted Vega flux densities
    return wanted_vega_fd
