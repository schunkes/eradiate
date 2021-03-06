.. _sec-user_guide-onedim_solver_app:

One-dimensional solver application
==================================

Eradiate ships with a solver application dedicated to the simulation of
radiative transfer on one-dimensional geometries. While the computation is not
actually one-dimensional (Eradiate's kernel is a 3D Monte Carlo ray tracer),
scene setup ensures that the computed quantities are equivalent to what would
be obtained with a proper 1D code.

As mentioned in the :ref:`sphx_glr_examples_generated_tutorials_01_quick_overview.py`
tutorial, the one-dimensional solver application can be used either through its
command-line interface ``ertonedim`` or through its Python API (see
:class:`.OneDimSolverApp`). This guide goes in more detail on the
features, configuration format and usage of this application.

.. admonition:: Tutorials

   * Basic usage ⇒ :ref:`sphx_glr_examples_generated_tutorials_solver_onedim_01_solver_onedim.py`
   * Heterogeneous atmosphere ⇒ :ref:`sphx_glr_examples_generated_tutorials_solver_onedim_02_heterogeneous_atmospheres.py`

Available features
------------------

Illumination
^^^^^^^^^^^^

As of the current version two types of emitters are available in OneDimSolverApp.

Directional illumination
    An infinitely distant emitter emits light in a single direction (Dirac
    delta distribution of incoming radiance). This type of illumination is
    usually used to simulate incoming Solar radiation.

Constant illumination
    Illuminates the scene from all directions homogeneously (uniform angular
    distribution of incoming radiance). This type of illumination is supported
    for debugging purposes.

In addition, each of these angular distributions can be associated a spectrum.
Both support user-defined spectrum definitions.  The directional illumination
also supports a variety of pre-defined Solar irradiance spectra (see
:mod:`~eradiate.data.solar_irradiance_spectra` for a complete list).

Measure
^^^^^^^

This application currently supports the computation of radiative quantities at
the top of the atmosphere. At the most basic level, it computes the
top-of-atmosphere (TOA) leaving radiance and derived quantities.

TOA leaving radiance
    This is the radiance reflected by the entire scene (surface and atmosphere),
    since the scene only contains infinitely distant illumination.

TOA bidirectional reflectance distribution function (TOA BRDF)
    The TOA leaving radiance can be post-processed together with scene
    illumination parameters to compute the TOA BRDF.

TOA bidirectional reflectance factor (TOA BRF)
    This is simply the TOA BRDF normalised by the BRDF of a non-absorbing
    diffuse (Lambertian) surface.

These quantities can be computed either for the entire hemisphere of leaving
directions, or only in the principal plane so as to save computational resources
and time.

.. note::

   Eradiate includes tools to easily slice hemispherical data sets and extract
   plane views: no need to schedule both hemispherical and principal plane
   measure computations!

Atmosphere
^^^^^^^^^^

An atmosphere can be optionally added to the scene. Currently, two types of
atmosphere are supported.

Homogeneous atmosphere
    The atmosphere has spatially invariant radiative properties.

Heterogeneous atmosphere
    The atmosphere has spatially varying radiative properties along the
    altitude coordinate. Absorption and Rayleigh scattering are currently
    supported.

Surface
^^^^^^^

In this application, surfaces are plane and their geometry cannot be adjusted.
Only the surface's radiative properties can be selected.

Diffuse surface
    A diffuse or Lambertian surface reflects incoming radiation isotropically,
    regardless the incoming direction. This behaviour is modelled by the Lambert
    BRDF, parametrised by a reflectance parameter.

Rahman-Pinty-Verstraete (RPV) surface
    This reflection model features an anisotropic behaviour and is commonly
    used for land surface reflection modelling. Eradiate implements several
    variants of it with 3 or 4 parameters.

Black surface
    The black surface absorbs all incoming radiation, irrespective of
    incident angle or wavelength.

Configuring the application
---------------------------

The application is implemented by the :class:`.OneDimSolverApp` class. Its
constructor can be called in a regular way; in that case, an operational
mode must be selected prior to instantiating the class using the
:func:`~eradiate.set_mode` function. Note that every parameter of the
:class:`.OneDimSolverApp` constructor  is optional and has a default value and
can be passed as an object or a dictionary.

In addition, the :class:`OneDimSolverApp.from_dict() <.OneDimSolverApp.from_dict>`
class method allows for instantiating :class:`.OneDimSolverApp` from a
dictionary. The functionality of the
:class:`OneDimSolverApp.from_dict() <.OneDimSolverApp.from_dict>` is completely
exposed by the ``ertonedim`` command-line interface (CLI). The CLI creates
the configuration dictionary from a YAML configuration file. The following shows
a configuration dictionary and its equivalent YAML specification:

.. tabbed:: Dictionary

   .. code-block:: python

      {
          "mode": {
              "type": "mono",  # Single-precision monochromatic mode
              "wavelength": 577.  # Evaluate optical properties at 577 nm
          },
          "surface": {
              "type": "rpv"  # Use a RPV surface with default parameters
          },
          "atmosphere": {
              "type": "homogeneous",  # Use a homogeneous atmosphere ...
              "toa_altitude": 120.,  # ... with TOA at 120 ...
              "toa_altitude_units": "km",  # ... km ...
              "sigma_s": 1e-4  # ... and a scattering coefficient of 1e-4 m^-1
          },
          "illumination": {
              "type": "directional",  # Use directional illumination ...
              "zenith": 30.,  # ... with a solar zenith angle of 30° ...
              "azimuth": 0.,  # ... and a solar azimuth angle of 0°
              "irradiance": {
                  "type": "uniform",  # Illuminate the scene with a uniform irradiance ...
                  "value": 1.8e6,  # ... of 1.8e6 ...
                  "value_units": "W/km**2/nm" # ... W/km^2/nm
              },
          },
          "measures": [{
              "type": "toa_hsphere",  # ... Record outgoing radiance at TOA ...
              "spp": 32000,  # ... with 32000 samples per angular point ...
              "zenith_res": 5., # ... with one angular point per 5° for zeniths ...
              "azimuth_res": 5.  # ... and one angular point per 5° for azimuths
          }]
      }

.. tabbed:: YAML

   .. code-block:: yaml

      mode:
        type: mono # Single-precision monochromatic mode
        wavelength: 577. # Evaluate optical properties at 577 nm
      surface:
        type: rpv # Use a RPV surface with default parameters
      atmosphere:
        type: homogeneous # Use a homogeneous atmosphere ...
        toa_altitude: 120. # ... with TOA at 120 ...
        toa_altitude_units: km # ... km ...
        sigma_s: 1.e-4 # ... and a scattering coefficient of 1e-4 m^-1
      illumination:
        type: directional # Use directional illumination ...
        zenith: 30. # ... with a solar zenith angle of 30° ...
        azimuth: 0. # ... and a solar azimuth angle of 0°
        irradiance:
          type: uniform # Illuminate the scene with a uniform irradiance ...
          value: 1.8e+6 # ... of 1.8e6 ...
          value_units: W/km**2/nm # ... W/km^2/nm
      measures:
        - type: toa_hsphere # ... Record outgoing radiance at TOA ...
          spp: 32000 # ... with 32000 samples per angular point ...
          zenith_res: 5. # ... with one angular point per 5° for zeniths ...
          azimuth_res: 5. # ... and one angular point per 5° for azimuths

The configuration is divided into sections presented and detailed below. Unless
specified, each section is also a dictionary and should take a ``type``
parameter which selects a programmatic component in Eradiate. In addition to the
``type`` parameter, a section should contain the parameters required to
initialise the corresponding programmatic element. Each allowed option is
referenced, as well as the corresponding class in the Eradiate codebase. Class
documentation details all their parameters and allowed values.

Sections and parameters can be omitted; in that case, they will be assigned
default values. Default section values are documented in the reference
documentation of the :class:`.OneDimSolverApp` class and the other Eradiate
classes.

When parameters are mentioned as "unit-enabled" in the reference documentation,
it means that they can be assigned units in a field bearing the same name with
the suffix ``_units``. See the
:ref:`Unit guide <sec-user_guide-unit_guide_user-field_unit_documentation>`
for more detail. See below for practical usage of this feature.

``mode``
^^^^^^^^

The ``mode`` section configures Eradiate's operational mode. It notably
configures the computational kernel. The ``type`` parameter must be a valid mode
identifier. This application currently supports the ``mono`` mode, which
performs monochromatic simulations. In this mode, only one wavelength is
transported per ray traced by the Monte Carlo engine. The mono ``mode`` is
wavelength-aware and has a single ``wavelength`` parameter. A double-precision
variant ``mono_double`` can also be selected.

.. seealso::

   * Mode reference documentation: :func:`eradiate.set_mode`

``surface``
^^^^^^^^^^^

As previously mentioned, only the radiative properties of the surface can be
selected. The following reflection models (values for ``type``) are currently
supported:

* ``lambertian``: Lambertian surface [:class:`.LambertianSurface`];
* ``rpv``: RPV surface [:class:`.RPVSurface`].

The example configuration dictionary uses the RPV reflection model with default
parameters.

.. seealso::

   * Surface reference documentation: :mod:`eradiate.scenes.surface`

``atmosphere``
^^^^^^^^^^^^^^

The two supported atmosphere models are referenced with the following ``type``
values:

* ``homogeneous``: homogeneous atmosphere [:class:`.HomogeneousAtmosphere`];
* ``heterogeneous``: heterogeneous atmosphere with selectable atmospheric
  profile (defaults to a profile derived from the US76 standard profile)
  [:class:`.HeterogeneousAtmosphere`].

In this example, a homogeneous atmosphere is selected, with a height of 120
kilometers. Its scattering coefficient is forced to
:math:`10^{-4} \mathrm{m}^{-1}`.

.. note::

   In the example, the ``toa_altitude_units`` field is used to specify the units
   of the ``toa_altitude`` field. If ``toa_altitude_units`` is unset,
   ``toa_altitude`` is interpreted in metres.

.. seealso::

   * Atmosphere reference documentation: :mod:`eradiate.scenes.atmosphere`
   * Atmospheric profile reference documentation:
     :mod:`eradiate.radprops.rad_profile`

``illumination``
^^^^^^^^^^^^^^^^

The available ``type`` values to configure the scene's illumination are:

* ``constant``: constant (*i.e.* isotropic) illumination angular distribution
  [:class:`.ConstantIllumination`];
* ``directional``: infinitely distant directional illumination (Dirac delta
  angular distribution) [:class:`.DirectionalIllumination`].

Both these illuminations have a parameter which takes a spectrum as its
argument. Spectra are also specified using dictionaries. Their parameters are
also given in the reference documentation. Allowed spectrum types are mentioned
in the illumination classes' documentation.

When unspecified, the illumination section defaults to a directional
illumination using a Solar irradiance spectrum.

The example uses a directional light source. Section parameters set the
illumination direction through its zenith and azimuth angles (also known as Sun
zenith and azimuth angles) and its irradiance is set to
:math:`1.8 \times 10^6 \mathrm{W}/\mathrm{km}^2/\mathrm{nm}`.

.. seealso::

   * Illumination reference documentation: :mod:`eradiate.scenes.illumination`
   * Spectrum reference documentation: :mod:`eradiate.scenes.spectra`

``measures``
^^^^^^^^^^^^

This section defines observational parameters. The ``measures`` section is
different from the others because it is a list of dictionaries. Each list item
is a dictionary defined the usual way (``type`` and other parameters).

The following ``type`` parameter values are supported:

* ``toa_pplane``: top-of-atmosphere leaving radiance in a plane
  [:class:`.RadianceMeterPlaneMeasure`]

  Valid aliases: ``toa_pplane_lo``, ``toa_pplane_brdf``, ``toa_pplane_brf``

* ``toa_hsphere``: top-of-atmosphere leaving radiance in the entire
  hemisphere [:class:`.RadianceMeterHsphereMeasure`]

  Valid aliases: ``toa_hsphere_lo``, ``toa_hsphere_brdf``, ``toa_hsphere_brf``

These TOA leaving radiance measures are automatically post-processed to compute
the BRDF and BRF.

.. note::

   Both these measures are more constrained than the scene element classes they
   rely on. In particular, the following parameters will have no effect:

   * ``hemisphere`` (orientation of sensor directions);
   * ``origin`` (origin point of sensor).

In the example, a hemispherical measure is chosen, which means that the leaving
radiance will be computed for the entire hemisphere. The ``spp`` parameter
defines the number of samples drawn for each observed direction; ``zenith_res``
and ``azimuth_res`` define the angular resolution with which the zenith and
azimuth ranges are discretised (in degrees, the default unit).

Result output
-------------

Data output depends on the way the application is accessed:

* The CLI outputs results to NetCDF files whose naming pattern is controlled by
  a positional argument ``fname_results``, used as a file name prefix for all
  output data sets. One netCDF file is produced for each measure.
* When using the :class:`.OneDimSolverApp` class directly, the
  :meth:`~.OneDimSolverApp.run()` method stores the computed results in the
  ``results`` attribute as a dictionary mapping measure identifiers to a
  :class:`xarray.Dataset` object. Each data set has one variable for each
  computed physical quantity (*e.g.* TOA radiance, BRDF and BRF for the
  ``toa_hsphere_*`` and ``toa_pplane_*`` measures).

Visualisation
-------------

Visualisation also depends on how the application is accessed:

* The CLI outputs a series of default plots for each measure. The plot file
  naming pattern is controlled by a positional argument ``fname_plots``, used as
  a file name prefix for all plot files.
* When using the :class:`.OneDimSolverApp` class directly, the
  :meth:`~.OneDimSolverApp.run()` method does not produce plots. The plotting is left
  to the user. Eradiate provides facilities to help with plotting.
