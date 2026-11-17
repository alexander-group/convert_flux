"""
This file is for defining any custom units. This code must be imported for usage of
    Vega magnitude system (and any customized units)
"""

# Import dependencies here
from astropy import units as u

# Define Vega magnitude
_u_vega = u.def_unit("VEGA")
VEGAMAG = u.MagUnit(_u_vega)

# Define FLAM and FNU
FLAM = u.def_unit(
    "flam",
    u.erg / (u.cm**2 * u.s * u.AA),
    format={"generic": "FLAM", "console": "FLAM"},
)
FNU = u.def_unit(
    "fnu", u.erg / (u.cm**2 * u.s * u.Hz), format={"generic": "FNU", "console": "FNU"}
)
