# Import dependencies here


def convert_flux(
    input_quantity, output_unit, source_spec_shape=None, transmission_curve=None
):
    """
    Convert between brightness quantities (magnitude, flux density, flux, and
    luminosity) using the supported units listed in conversion_units.rst.

    A transmission curve is required for any conversion between flux density and
    flux. No transmission curve is assumed by default. To use a flat transmission
    curve, the user must choose it explicitly. The source spectrum shape (flat,
    Lyman alpha break, or polynomial) is also used for conversions between flux
    density and flux. If no source spectrum shape is given, a flat source spectrum
    is assumed.

    Args:
        input_quantity: The quantity to convert, including its value and units.
        output_unit: The desired output unit for the conversion.
        source_spec_shape: The shape of the source spectrum. Defaults to a flat
            source spectrum.
        transmission_curve: The transmission curve of the filter. Required for
            conversions between flux density and flux. A flat transmission curve
            must be chosen explicitly; it is not the default.

    Returns:
        The converted quantity, including its value and the desired output unit.

    Raises:
        ValueError: If the input quantity or the output unit is not a supported
            brightness unit, or if the conversion needs a transmission curve and
            none is given.

    """
    output_quantity = None

    return output_quantity
