import eradiate.kernel
from eradiate.scenes import SceneDict
from eradiate.solvers.onedim.rayleigh import RayleighSolverApp


def test_rayleigh_solver_app():
    # Default constructor
    app = RayleighSolverApp()
    assert app.config == SceneDict(RayleighSolverApp.DEFAULT_CONFIG)
    assert eradiate.kernel.variant() == "scalar_mono_double"

    # Check that the default scene can be instantiated
    assert app._scene_dict.load() is not None

    # TODO: check and improve following tests

    # run with default configuration
    #assert app.run() == 0.1591796875

    # custom config
    config = {
        "mode": {
            "type": "mono",
            "wavelength": 800.
        },
        "illumination": {
            "type": "directional",
            "zenith": 10.,
            "azimuth": 0.,
            "irradiance": 1.
        },
        "measure": {
            "type": "distant",
            "zenith": 40.,
            "azimuth": 180.
        },
        "surface": {
            "type": "lambertian",
            "reflectance": 0.35
        }
    }
    app = RayleighSolverApp(config)
    assert app.config == config

    # run with custom config
    #assert app.run() == 0.1591796875

    # custom config (with atmosphere)
    config = {
        "mode": {
            "type": "mono",
            "wavelength": 550.
        },
        "illumination": {
            "type": "directional",
            "zenith": 0.,
            "azimuth": 0.,
            "irradiance": 1.
        },
        "measure": {
            "type": "distant",
            "zenith": 30.,
            "azimuth": 180.
        },
        "surface": {
            "type": "lambertian",
            "reflectance": 0.5
        },
        "atmosphere": {
            "sigmas": 1e-6,
            "height": 1e5
        }
    }
    app = RayleighSolverApp(config)
    assert app.config == config

    # run with custom config
    #assert app.run() < 0.1591796875

    # custom config (with custom refractive index)
    config = {
        "mode": {
            "type": "mono",
            "wavelength": 550.
        },
        "illumination": {
            "type": "directional",
            "zenith": 0.,
            "azimuth": 0.,
            "irradiance": 1.
        },
        "measure": {
            "type": "distant",
            "zenith": 30.,
            "azimuth": 180.
        },
        "surface": {
            "type": "lambertian",
            "reflectance": 0.5
        },
        "atmosphere": {
            "refractive_index": 1.0003,
            "height": 1e5
        }
    }
    app = RayleighSolverApp(config)
    assert app.config == config

    # run with custom config
    #assert app.run() < 0.1591796875


def test_rayleigh_solver_app_run():
    """Test the creation of a DataArray from the solver result

    We create a default scene with a set of zenith and azimuth angles,
    render the scene and create the DataArray.

    We assert the correct setting of the DataArray coordinates and dimensions,
    as well as the correct setting of data.
    """
    import xarray as xr
    import numpy as np
    assert eradiate.kernel.variant() == "scalar_mono_double"

    config = {"measure": {
        "type": "distant",
        "zenith": [0, 30, 60, 90],
        "azimuth": [0, 45, 90, 135, 180, 225, 270, 315, 360]
        },
    }

    app = RayleighSolverApp(config)
    app.run()

    for dim in ["theta_i", "phi_i", "theta_o", "phi_o", "wavelength"]:
        assert dim in app.result.dims

    assert np.all(app.result.coords["phi_o"] == config["measure"]["azimuth"])
    assert np.all(app.result.coords["theta_o"] == config["measure"]["zenith"])

    assert np.all(app.result.data > 0)
    assert np.all(app.result == app.result.sel(theta_i=0, phi_i=0, theta_o=0, phi_o=0, wavelength=550))