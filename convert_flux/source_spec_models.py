from abc import abstractmethod, ABC
import numpy as np
import astropy.units as u

"""
Handles all source spectrum shapes that we support
"""


class SourceSpec(ABC):
    """
    Abstract Base Class for all source spectrum types
    The shape is evaluated on the same wavelength grid as the transmission curve.
    """

    def shape(self, wavelength):
        # Return one value per wavelength
        if not isinstance(wavelength, u.Quantity):
            raise TypeError("wavelength must be an astropy Quantity")

        wavelength = wavelength.to(u.Angstrom)

        fluxes = np.asarray(self._shape(wavelength), dtype=float)

        return fluxes

    @abstractmethod
    def _shape(self, wavelength):
        # Evaluate the subclass's dimensionless shape on a validated grid.
        pass


class FlatSpec(SourceSpec):
    """
    Subclass of SourceSpec ABC to define an appromixately flat source spectrum
    """

    def _shape(self, wavelength):
        return np.ones(wavelength.shape, dtype=float)


class LymASpec(SourceSpec):
    """
    Subclass of SourceSpec ABC to define a Lymna alpha break source spectrum
    """

    pass


class PolySpec(SourceSpec):
    """
    Subclass of SourceSpec ABC to define an approximately polynomial source spectrum
    """

    pass
