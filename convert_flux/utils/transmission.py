import numpy as np
import astropy.units as u
from scipy.signal import resample
from infer_filter_info import infer_filter_info
from infer_filter_info.exceptions import MissingDefaultError
from ..exceptions import TransmissionCurveError


class TransmissionCurve:
    """
    A class that defines a transmission curve. Wavelength and transmission arrays are
    stored as attributes. A transmission curve can be created from a filter name or
    from wavelength and transmission arrays.

    Attributes:
        wavelength (u.Quantity): Wavelength array in astropy units.
        transmission (np.ndarray): Transmission array corresponding to wavelengths.
        mean_wavelength (u.Quantity): Mean wavelength of the filter, used as the
            reference wavelength for flux densities.
    """

    def __init__(self, wavelength, transmission, mean_wavelength=None):
        """
        Initialize TransmissionCurve class with wavelength and transmission arrays.

        Parameters:
            wavelength (u.Quantity): Wavelength array in astropy units.
            transmission (np.ndarray): Transmission array corresponding to wavelengths.
            mean_wavelength (u.Quantity): Mean wavelength of the filter.

        Raises:
            TypeError: If wavelength is not an astropy quantity or if wavelength and
            transmission have different sizes.
        """
        if not isinstance(wavelength, u.Quantity):
            raise TypeError("wavelength must be astropy quantity.")
        wavelength = wavelength.to(u.AA, equivalencies=u.spectral())
        transmission = np.asarray(transmission, dtype=float)

        # order wavelengths from smallest to largest
        order = np.argsort(wavelength)

        if transmission.shape != wavelength.shape:
            transmission = resample(transmission, wavelength.size)

        self.wavelength = wavelength[order]
        self.transmission = transmission[order]
        self.mean_wavelength = mean_wavelength

    @staticmethod
    def from_filter(
        filter_name: str, *args, curve: np.ndarray = None, **kwargs
    ) -> "TransmissionCurve":
        """
        Function to create a transmission curve from a filter name. Infers transmission
        curves from SVO using infer_filter_info as a query.

        Parameters:
            filter_name (str): Name of filter to infer the transmission curve for.
            curve (np.ndarray): Optional user-provided transmission curve to use as a
            fallback.

        Returns:
            TransmissionCurve object representing the transmission curve and wavelength
            array. Its mean wavelength is the one infer_filter_info returns,
            integral(wavelength * T) / integral(T).
        """
        try:
            mean_wavelength, sens = infer_filter_info(filter_name, *args, **kwargs)
        except (MissingDefaultError, LookupError, IndexError, KeyError):
            # throw an error if infer_filter_info from SVO can't find a curve
            # fall back to the user-provided curve, if any
            if curve is None:
                # add a wrapper class to make the user pass a wavelength array
                raise TransmissionCurveError(
                    "Could not find a transmission curve. Pass a wavelength "
                    "array instead"
                )
            return curve

        wavelength, transmission = sens
        return TransmissionCurve(wavelength * u.AA, transmission)


class FlatTransmissionCurve(TransmissionCurve):
    """
    A class that defines a flat transmission curve, subclass of TransmissionCurve.
    """

    def __init__(self, lambda_min, lambda_max, num_points=1000, transmission_max=1.0):
        """
        Initialize FlatTransmissionCurve class with wavelength array.

        Parameters:
            wavelength (u.Quantity): Wavelength array in astropy units.
        """
        wavelength = np.linspace(lambda_min, lambda_max, num_points) * u.AA
        transmission = transmission_max * np.ones_like(wavelength.value)
        super().__init__(wavelength, transmission)
