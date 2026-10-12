from convert_flux.convert_flux import FluxLuminosity


def test_flux_to_luminosity_creation():
    """
    Test that ensures the FluxLuminosity class is created correctly.

    Attributes:
        flux_luminosity (FluxLuminosity): FluxLuminosity object.
    """
    flux_luminosity = FluxLuminosity()
    assert isinstance(flux_luminosity, FluxLuminosity)
