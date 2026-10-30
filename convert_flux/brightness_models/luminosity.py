import astropy.units as u


class Luminosity:
    """
    A class that defines luminosity as an Astropy Quantity. Base units are in erg/s.

    Attributes:
        Astropy Quantity (value + unit)
    """

    def __init__(self, quantity):
        """
        Initialize function that defines the Luminosity object
        with an Astropy Quantity.

        Parameters:
            quantity (u.Quantity): The luminosity quantity to be
            converted to standard units in erg/s.

        Raises:
            TypeError: If the input is not an Astropy Quantity.
        """
        if not isinstance(quantity, u.Quantity):
            raise TypeError("Quantity input must be an Astropy Quantity.")

        self.quantity = quantity.to(u.erg / u.s)
