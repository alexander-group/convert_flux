# Import dependencies here
from astropy import units as u

# Define Vega magnitude
_u_vega = u.def_unit("VEGA")
VEGAMAG = u.mag(_u_vega)
