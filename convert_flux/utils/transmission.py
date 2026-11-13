import numpy as np
import astropy.units as u
from infer_filter_info import infer_filter_info
from infer_filter_info.exceptions import MissingDefaultError


class TransmissionCurve:
    """
    Future implementation for transmission curve
    (In wavelength space)
    Will interact with transmission info package
    """

    def __init__(self, wavelength, transmission):
        """ """
        if not isinstance(wavelength, u.Quantity):
            raise TypeError("wavelength must be astropy quantity.")
        wavelength = wavelength.to(u.AA, equivalencies=u.spectral())
        transmission = np.asarray(transmission, dtype=float)

        # order wavelengths from smallest to largest
        order = np.argsort(wavelength)

        if isinstance(transmission, np.ndarray):
            if np.size(wavelength) != np.size(transmission):
                # will add smooth/resample if they are not the same shape from new issue
                raise TypeError("wavelength and transmission must have the same size")
        else:
            transmission = np.array(transmission)

        self.wavelength = wavelength[order]
        self.transmission = transmission[order]

    @staticmethod
    def from_filter(filter_name, curve, *args, **kwargs):
        """ """
        try:
            _, sens = infer_filter_info(filter_name, *args, **kwargs)
        except (MissingDefaultError, LookupError, IndexError, KeyError):
            # throw an error if infer_filter_info from SVO can't find a curve
            # fall back to the user-provided curve, if any
            if curve is None:
                # add a wrapper class to make the user pass a wavelength array
                raise LookupError(
                    "Could not find transmission curve. To use a "
                    "standard flat curve, pass"
                    "curve=TransmissionCurve(wavelength, np.ones(wavelength.shape))"
                )
            return curve

        wavelength, transmission = sens
        return TransmissionCurve(wavelength * u.AA, transmission)
