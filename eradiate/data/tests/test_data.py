import eradiate.data as data


def test_get():
    # We expect the data to load successfully from the hard drive
    ds = data.get("spectra/thuillier2003.nc")