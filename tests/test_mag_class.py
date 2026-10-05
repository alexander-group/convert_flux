# Import packages here
import astropy.units as u
from convert_flux.convert_flux import Mag


# Test if Magnitude quantity is created
def test_mag_quantity_created():
    mag1 = Mag(quantity=17.0 * u.STmag, spectral_coordinate=5500 * u.Angstrom)
    mag2 = Mag(quantity=17.2 * u.STmag, spectral_coordinate=5750 * u.Angstrom)
    assert isinstance(mag1, Mag)
    assert isinstance(mag2, Mag)


# Test if Magnitude is an astropy Magnitude
def test_mag_is_quantity():
    mag1 = Mag(quantity=17.0 * u.STmag, spectral_coordinate=5500 * u.Angstrom)
    mag2 = Mag(quantity=17.2 * u.STmag, spectral_coordinate=5750 * u.Angstrom)
    assert isinstance(mag1.quantity, u.Magnitude)
    assert isinstance(mag2.quantity, u.Magnitude)
