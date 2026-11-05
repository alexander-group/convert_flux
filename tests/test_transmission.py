import pytest
import astropy.units as u
import numpy as np

from convert_flux.transmission import TransmissionCurve


def test_must_give_arguments():
    # there is no way to get a flat curve by accident
    with pytest.raises(TypeError):
        TransmissionCurve()


def test_custom_curve():
    curve = TransmissionCurve([1000, 2000, 3000] * u.nm, [0.1, 0.3, 0.5])
    assert curve.wavelength.unit == u.Angstrom
    assert isinstance(curve, TransmissionCurve)


def test_wavelength_transmission_same_size():
    with pytest.raises(TypeError):
        TransmissionCurve([1000, 2000] * u.Angstrom, [0.1, 0.3, 0.5])


def test_wavelength_ordering():
    curve = TransmissionCurve([3000, 1000, 2000] * u.AA, [0.5, 0.1, 0.3])
    assert np.array_equal(curve.wavelength.value, [1000, 2000, 3000])
    assert np.array_equal(curve.transmission, [0.1, 0.3, 0.5])


def test_validate_infer_filter_info_query():
    # checks if infer_filter_info query works
    curve = TransmissionCurve.from_filter("g")
    assert isinstance(curve, TransmissionCurve)
    assert curve.wavelength.unit == u.Angstrom
    assert curve.wavelength.shape == curve.transmission.shape


def test_return_initial_curve_when_filter_not_found():
    initial = TransmissionCurve([1000, 2000, 3000] * u.nm, [0.1, 0.3, 0.5])
    new_curve = TransmissionCurve.from_filter("SDSS", curve=initial)
    assert new_curve is initial


def test_flat_curve_must_be_explicit_when_filter_not_found():
    with pytest.raises(LookupError):
        TransmissionCurve.from_filter(
            "SDSS", telescope=None, instrument=None, curve=None
        )


def test_flat_curve():
    wavelength = [1000, 2000, 3000] * u.nm
    flat = TransmissionCurve(wavelength, np.ones(wavelength.shape))
    curve = TransmissionCurve.from_filter("SDSS", curve=flat)
    assert np.array_equal(curve.transmission, np.ones(wavelength.shape))
