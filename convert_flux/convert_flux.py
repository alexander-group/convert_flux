# Import dependencies here


def convert_flux(
    input_quantity, output_unit, source_spec_shape=None, transmission_curve=None
):
    """
    This function converts between different brightness units (Flux, FluxDensity,
    Luminosity, Mag) with the supported units listed in convresion_units.rst. The user
    should provide tranmission curve information if using flux density or flux.
    If the user does not provide a transmission curve, a flat transmission curve will be
    assumed. The user should provide the source spectrum shape (flat, lyman alpha break,
    polynomial) if using flux density or flux. If the user does not provide a source
    spectrum shape, a flat source spectrum will be assumed.

    Args:
        input_quantity: The quantity to convert including value and units.
        output_unit: The desired output unit for the conversion.
        source_spec_shape: The name of the shape of the source spectrum (default is
        flat).
        transmission_curve: The transmission curve array (default is flat).

    Returns:
        The converted quantity including value and desired output unit.

    Raises:
        ValueError: If the input quantity is not a supported brightness unit or if the
        output unit is not a supported brightness unit.

    """
    output_quantity = None

    return output_quantity
