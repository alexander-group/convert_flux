Conversion Units Plan
======================

This page is for outlining the working units for ``convert_flux``. It lists the
physical quantities the package will convert between, the default units if none are
specified, and the units we can support for each quantity.

Goals
------

* Use input/output values with Astropy units whenever possible.
* Convert to the default unit internally before doing the subsequent
  conversions/calculations.
* Treat magnitudes as dimensionless but with the tag of AB, Vega, or ST.
* Make useful error messages for invalid input units, unsupported conversions,
  or missing information.

Supported quantities
---------------------

Magnitude
~~~~~~~~~~

Note: Magnitudes in different systems are not interchangeable despite being dimensionless.
The input must state the system used for the value.

Supported magnitude systems:

* ``AB magnitude (AB mag)`` - Default
* ``Vega magnitude (Vega)``
* ``ST magnitude (ST mag)``

Total Flux
~~~~~~~~~~~~~~~~~~~~~

* ``erg / (s cm^2)`` - Default
* ``W / m^2``
* ``J / s m^2``


Flux Density
~~~~~~~~~~~~~~~~~~~~~

Frequency-based

* ``Jy`` - Default
* ``erg / (s cm^2 Hz)``
* ``W / (m^2 Hz)``


Wavelength-based

* ``erg / (s cm^2 Angstrom)`` - Default
* ``W / (m^2 nm)``

Wavelength
~~~~~~~~~~~

* ``Angstrom`` - Default
* ``nm``
* ``m``
* ``um``

Frequency
~~~~~~~~~~~

* ``Hz`` - Default
* ``kHz``
* ``MHz``
* ``GHz``

Luminosity
~~~~~~~~~~~

* ``erg / s`` - Default
* ``W``
* ``Solar luminosity (L_sun)``
