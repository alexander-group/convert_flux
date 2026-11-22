# Import packages here
import pytest
import astropy.units as u
from convert_flux.brightness_models import Mag
from convert_flux.utils.convert_flux_units import VEGAMAG


# Test if astropy quantity is created
def test_mag_quantity_created():
    mag1 = Mag(
        quantity=17.0 * u.STmag,
        spectral_coordinate=5500 * u.Angstrom,
        chosen_mag_system=VEGAMAG,
    )
    mag2 = Mag(
        quantity=17.2 * u.STmag,
        spectral_coordinate=5750 * u.Angstrom,
        chosen_mag_system=u.STmag,
    )
    mag3 = Mag(
        quantity=17.2 * VEGAMAG,
        spectral_coordinate=5750 * u.Angstrom,
        chosen_mag_system=u.ABmag,
    )
    assert isinstance(mag1, Mag)
    assert isinstance(mag2, Mag)
    assert isinstance(mag3, Mag)


# Test if Magnitude is an astropy Magnitude
def test_inputmag_is_quantity():
    mag1 = Mag(
        quantity=17.0 * u.STmag,
        spectral_coordinate=5500 * u.Angstrom,
        chosen_mag_system=u.ABmag,
    )
    mag2 = Mag(
        quantity=17.0 * u.ABmag,
        spectral_coordinate=5750 * u.Angstrom,
        chosen_mag_system=VEGAMAG,
    )
    mag3 = Mag(
        quantity=17.0 * VEGAMAG,
        spectral_coordinate=5750 * u.Angstrom,
        chosen_mag_system=u.STmag,
    )
    assert isinstance(mag1.quantity, u.Magnitude)
    assert isinstance(mag2.quantity, u.Magnitude)
    assert isinstance(mag3.quantity, u.Magnitude)


# Test if wrong units for magnitude can be detected
def test_wrong_unit_magnitude():
    with pytest.raises(u.UnitsError):
        Mag(quantity=17.0 * u.kg, spectral_coordinate=6187 * u.Angstrom)


# Test if wrong units for spectral_coordinate can be detected
def test_wrong_unit_for_spectral_coordinate():
    with pytest.raises(u.UnitConversionError):
        Mag(quantity=17.0 * u.STmag, spectral_coordinate=6187 * u.kg)


# Test if non-Astropy quantities can be detected
def test_type_error_for_non_quantity_mag():
    with pytest.raises(TypeError):
        Mag(quantity=3.631, spectral_coordinate=6187 * u.Angstrom)


def test_type_error_for_non_quantity_spec_coord():
    with pytest.raises(TypeError):
        Mag(quantity=3.631 * u.STmag, spectral_coordinate=6187)
