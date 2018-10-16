import unittest

from aguaclara.core.units import unit_registry as u
from aguaclara.core import pipes


class TestPipes(unittest.TestCase):
    # TODO: better test coverage (e.g. metric, functions outside Pipe)

    def test_pipes(self):
        pipe = pipes.Pipe(nd=(7.0 * u.inch), sdr=35.0)

        def assert_quantity_equal(a, b):
            self.assertAlmostEqual(a.magnitude, b.magnitude)
            self.assertAlmostEqual(a.units, b.units)

        assert_quantity_equal(pipe.od(), 7.625 * u.inch)
        assert_quantity_equal(pipe.id_sdr(), 7.18928571 * u.inch)
        assert_quantity_equal(pipe.id_sch40(), 7.023 * u.inch)


if __name__ == '__main__':
    unittest.main()
