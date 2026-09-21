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
- flux from/to luminosity (class)
    - function for calculation
- flux density to flux (class)
    - function to read transmission curve file (NumPy array)
    - function to do calculation
- Mag (u.Unit)
- Flux (u.Unit)
- FluxDensity (u.Unit)


"""


def convert_flux():
    return
