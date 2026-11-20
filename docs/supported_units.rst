Conversion Units Plan
======================

This page is a reference for users of ``convert_flux``. It lists the
physical quantities the package will convert between, the units used internally,
and all the units we can support for each quantity, following closely with Astropy's
supported quantities.


Supported quantities
---------------------

Magnitude
~~~~~~~~~~~

* ``AB magnitude (astropy.units.ABmag)`` - Default
* ``Vega magnitude (VEGA)`` - Defined in convert_flux_units.py
* ``ST magnitude (STmag)``

Note: Magnitudes in different systems are not interchangeable despite being dimensionless.
The input must state the system used for the value as its unit.

Total Flux
~~~~~~~~~~~~~~

* ``erg / (s cm^2)`` - Default
* ``W / m^2``
* ``J / s m^2``
* All other equivalent units supported in Astropy


Flux Density
~~~~~~~~~~~~~~~

Frequency-based

* ``uJy`` - Default
* ``erg / (s cm^2 Hz)``
* ``W / (m^2 Hz)``
* All other equivalent units supported in Astropy


Wavelength-based

* ``erg / (s cm^2 Angstrom)`` - Default
* ``W / (m^2 nm)``
* All other equivalent units supported in Astropy

Luminosity
~~~~~~~~~~~

* ``erg / s`` - Default
* All other equivalent units supported in Astropy
