import pytest

from convert_flux.transmission import TransmissionCurve


def test_must_give_arguments():
    # there is no way to get a flat curve by accident
    with pytest.raises(TypeError):
        TransmissionCurve()
