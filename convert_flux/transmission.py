import numpy as np
import astropy.units as u
from infer_filter_info import infer_filter_info


class TransmissionCurve:
    """
    Future implementation for transmission curve
    (In wavelength space)
    Will interact with transmission info package
    """

    def __init__(self, wavelength, transmission):
        if not isinstance(wavelength, u.Quantity):
            raise TypeError("wavelength must be astropy quantity.")
        wavelength = wavelength.to(u.AA, equivalencies=u.spectral())
        transmission = np.asarray(transmission, dtype=float)

        # order wavelengths from smallest to largest
        order = np.argsort(wavelength)

        self.wavelength = wavelength[order]
        self.transmission = transmission[order]

    def from_filter(
        self, filter_name, telescope=None, instrument=None, obs_type="uvoir"
    ):
        _, curve = infer_filter_info(
            filter_name,
            telescope=telescope,
            instrument=instrument,
            obs_type=obs_type,
            out_wave_unit=u.Angstrom,
        )

        # throw an error if infer_filter_info from SVO can't find a transmission curve
        # the user needs to explicitly choose flat curve.

        wavelength, transmission = curve
        return wavelength * u.Angstrom, transmission
