# Import dependencies here
import astropy.units as u

from .brightness_models import Flux, FluxDensity, Luminosity, Mag
from .converters import FluxFluxDensity, FluxLuminosity, MagFluxDensity
from .utils import TransmissionCurve

# Brightness quantities in the order the converters connect them. Each converter
# links two neighbors: MagFluxDensity, FluxFluxDensity, then FluxLuminosity.
_CHAIN = ["mag", "flux_density", "flux", "luminosity"]


def _brightness_kind(unit):
    """
    Identify which brightness quantity a unit measures.

    Magnitudes are checked first, because astropy gives ABmag the same physical
    type as frequency-based flux density.

    Args:
        unit: An astropy unit.

    Returns:
        One of "mag", "flux_density", "flux", or "luminosity".

    Raises:
        ValueError: If the unit is not a supported brightness unit.
    """
    if isinstance(unit, u.MagUnit):
        return "mag"

    physical_type = unit.physical_type
    if physical_type in ("spectral flux density", "spectral flux density wav"):
        return "flux_density"
    if physical_type == "energy flux":
        return "flux"
    if physical_type == "power":
        return "luminosity"

    raise ValueError(
        f"{unit} is not a supported brightness unit. Use a magnitude, flux density, "
        "flux, or luminosity unit (see supported_units.rst)."
    )


def _wrap(kind, quantity, ref_wavelength):
    """Wrap a Quantity in the brightness model for its kind."""
    if kind == "mag":
        return Mag(quantity, ref_wavelength)
    if kind == "flux_density":
        return FluxDensity(quantity, ref_wavelength)
    if kind == "flux":
        return Flux(quantity)
    return Luminosity(quantity)


# One-hop conversions. Each takes a brightness model and the conversion context,
# and returns the brightness model for the neighboring kind.
def _mag_to_flux_density(mag, context):
    return MagFluxDensity(mag=mag).mag_to_flux_density(context["ref_wavelength"])


def _flux_density_to_mag(flux_density, context):
    return MagFluxDensity(flux_density=flux_density).flux_density_to_mag(
        flux_density.spectral_coordinate
    )


def _flux_density_to_flux(flux_density, context):
    curve = context["transmission_curve"]
    return FluxFluxDensity(flux_density=flux_density).flux_density_to_flux(
        curve.transmission, curve.wavelength, context["source_spec"]
    )


def _flux_to_flux_density(flux, context):
    curve = context["transmission_curve"]
    return FluxFluxDensity(flux=flux).flux_to_fluxdensity(
        curve.transmission,
        curve.wavelength,
        curve.mean_wavelength,
        context["source_spec"],
    )


def _flux_to_luminosity(flux, context):
    return FluxLuminosity(flux=flux).flux_to_luminosity(
        context["distance"], context["z"]
    )


def _luminosity_to_flux(luminosity, context):
    return FluxLuminosity(luminosity=luminosity).luminosity_to_flux(
        context["distance"], context["z"]
    )


_STEPS = {
    ("mag", "flux_density"): _mag_to_flux_density,
    ("flux_density", "mag"): _flux_density_to_mag,
    ("flux_density", "flux"): _flux_density_to_flux,
    ("flux", "flux_density"): _flux_to_flux_density,
    ("flux", "luminosity"): _flux_to_luminosity,
    ("luminosity", "flux"): _luminosity_to_flux,
}


def convert_flux(
    input_quantity,
    output_unit,
    filter_name=None,
    telescope=None,
    instrument=None,
    source_spec_shape=None,
    distance=None,
    z=None,
    vega_spec=None,
):
    """
    Convert between brightness quantities (magnitude, flux density, flux, and
    luminosity) using the supported units listed in conversion_units.rst.

    The input and output quantities are identified from their units. When astropy
    can convert the input unit to the output unit directly (for example, W/m^2 to
    erg/(s cm^2), or AB magnitude to uJy), it does. Otherwise, the conversion
    steps through mag -> flux density -> flux -> luminosity (or the reverse) and
    only uses the information each step needs.

    A filter is required for any conversion that involves a magnitude or a flux
    density, because its transmission curve sets the reference wavelength (the
    filter's mean wavelength) and the filter used between flux density and flux.
    The filter is looked up with infer_filter_info, which queries the SVO Filter
    Profile Service, using the same filter_name, telescope, and instrument
    arguments. No transmission curve is assumed by default. The source spectrum
    shape (flat, Lyman alpha break, or polynomial) is also used for conversions
    between flux density and flux. If no source spectrum shape is
    given, a flat source spectrum is assumed. A distance or a redshift is required
    for conversions between flux and luminosity.

    Args:
        input_quantity: The quantity to convert, including its value and units.
        output_unit: The desired output unit for the conversion.
        filter_name: The filter name, for example "r". Required for conversions
            that involve a magnitude or a flux density, unless astropy can convert
            the units directly.
        telescope: The telescope name, for example "SLOAN" or "Palomar". Passed to
            infer_filter_info.
        instrument: The instrument name, for example "SDSS" or "ZTF". Passed to
            infer_filter_info.
        source_spec_shape: The shape of the source spectrum. Defaults to a flat
            source spectrum.
        distance: The distance to the source. Used for conversions between flux
            and luminosity.
        z: The redshift of the source. Used instead of distance to compute the
            luminosity distance (Planck18 cosmology).
        vega_spec: The spectrum of the Vega star. Required for conversions with Vega
            mag.

    Returns:
        The converted quantity, including its value and the desired output unit.

    Raises:
        TypeError: If the input quantity is not an astropy Quantity.
        ValueError: If the input quantity or the output unit is not a supported
            brightness unit, if the conversion needs a filter and none is given,
            or if it needs a distance or redshift and neither is given.
        TransmissionCurveError: If no transmission curve is found for the filter.
    """
    if not isinstance(input_quantity, u.Quantity):
        raise TypeError("input_quantity must be an astropy Quantity.")

    kind_in = _brightness_kind(input_quantity.unit)
    kind_out = _brightness_kind(output_unit)

    # Let astropy convert directly when no extra information is needed
    if input_quantity.unit.is_equivalent(output_unit):
        return input_quantity.to(output_unit)

    # Build the path of kinds from the input to the output
    index_in = _CHAIN.index(kind_in)
    index_out = _CHAIN.index(kind_out)
    if index_in <= index_out:
        path = _CHAIN[index_in : index_out + 1]
    else:
        path = _CHAIN[index_out : index_in + 1][::-1]

    # Check that every step on the path has what it needs
    transmission_curve = None
    ref_wavelength = None
    if "mag" in path or "flux_density" in path:
        if filter_name is None:
            raise ValueError(f"Converting {kind_in} to {kind_out} needs a filter_name.")
        transmission_curve = TransmissionCurve.from_filter(
            filter_name, telescope=telescope, instrument=instrument
        )
        ref_wavelength = transmission_curve.mean_wavelength

    if "flux" in path and "luminosity" in path and distance is None and z is None:
        raise ValueError(
            f"Converting {kind_in} to {kind_out} needs a distance or a redshift z."
        )

    context = {
        "transmission_curve": transmission_curve,
        "source_spec": source_spec_shape,
        "ref_wavelength": ref_wavelength,
        "distance": distance,
        "z": z,
    }

    # Step through the converters, one neighboring pair of kinds at a time
    model = _wrap(kind_in, input_quantity, ref_wavelength)
    for kind_from, kind_to in zip(path, path[1:]):
        model = _STEPS[(kind_from, kind_to)](model, context)

    # Convert from the model's internal unit to the requested unit
    if ref_wavelength is None:
        return model.quantity.to(output_unit)
    return model.quantity.to(
        output_unit, equivalencies=u.spectral_density(ref_wavelength)
    )
