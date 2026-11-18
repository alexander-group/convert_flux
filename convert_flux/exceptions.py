"""
Custom exceptions for the convert_flux package
"""

class TransmissionCurveError(LookupError):
    """Raises when no transmission curve is found."""
