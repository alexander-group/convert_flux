class TransmissionCurve:
    """
    Future implementation for transmission curve
    (In wavelength space)
    Will interact with transmission info package
    """

    def __init__(self, wavelength, transmission):
        self.transmission = 1


# provide flat transmission curve if user doesn't want to provide specific input
# user should need to explicitly choose flat curve (not a default!)
