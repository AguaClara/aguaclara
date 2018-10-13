from aguaclara.core import drills


def test_drill():
    print(
        "Imperial drill bit diameters: \n"
        + repr(drills.DRILL_BITS_D_IMPERIAL) + "\n"
    )
    print(
        "Metric drill bit diameters: \n"
        + repr(drills.DRILL_BITS_D_METRIC) + "\n"
    )
