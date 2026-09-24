"""
The main function of the package, a single function to convert fluxes,
flux densities, and magnitudes

Brainstorming:
Inputs:
astropy quantity (value + unit)
wavelength, flux file (.dat, .txt, .csv)


Output:
astropy quantity (value + unit)

Separate classes/functions for each type of calculation/conversion
- input validation (check equivalency, convert to one standard unit that we decide on)
- mag to flux density (class)
    - functions for each type of magnitude (AB, Vega, ST) *just write for AB for now*
- flux density to flux (class)
    - function to read transmission curve file (NumPy array)
    - function to do calculation
- flux from/to luminosity (class)
    - function for calculation
- Mag (u.Unit)
- Flux (u.Unit)
- FluxDensity (u.Unit)


"""


def convert_flux():
    return


class Mag:
    """
    1. Input validation
    2. Convert to a stand unit
    Thomas
    """

    def __init__(self, value, unit):
        return


class Flux:
    """
    1. Input validation
    2. Convert to a stand unit
    Robin
    """

    def __init__(self, value, unit):
        return


class FluxDensity:
    """
    1. Input validation
    2. Convert to a stand unit
    Nayera
    """

    def __init__(self, value, unit):
        return


class MagFluxDensity:
    """
    1. Conversion equations/calculation


    """

    def __init__(self, mag, flux_density):
        return


class FluxFluxDensity:
    """
    1. Conversion equations/calculation
    2. Transmission curve file reading function
    3. Call to Source spectrum class

    """

    def __init__(self, flux, flux_density):
        return


class FluxLuminosity:
    """
    1. Conversion equations/calculation
    """

    def __init__(self, flux, luminosity):
        return


class SourceSpec:
    """
    Future implementation for non-flat spectrum
    """

    def __init__(self, wavelength, flux):
        self.flux = 1
