"""
This Python source code file will include handling for Vega magnitude system,
    including defining the magnitude system and downloading & storing Vega spectra
"""

# Import dependencies here
from astropy.coordinates import SkyCoord

# Discuss which source of spectra to query from during stand-up
# Current list includes MAST, ALMA, SDSS
# Use MAST for spectra with space telescopes right now

# Query Vega's coordinate
vega_pos = SkyCoord.from_name("Vega")


class VegaSpec:
    def __init__(self):
        pass
