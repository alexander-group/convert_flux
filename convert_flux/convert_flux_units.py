"""
This file is for defining any custom units. This code must be imported for usage of
    Vega magnitude system (and any customized units)
"""

# Import dependencies here
from astropy import units as u

# Define Vega magnitude
_u_vega = u.def_unit("VEGA")
VEGAMAG = u.mag(_u_vega)
