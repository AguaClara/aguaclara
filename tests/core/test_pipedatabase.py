import unittest
from aguaclara.core.units import u
from aguaclara.core import pipes as pipe


class PipeTest(unittest.TestCase):
    def test_OD(self):
        checks = [[1.0 * u.inch, 1.315 * u.inch]]
        for i in checks:
            with self.subTest(i=i):
                self.assertAlmostEqual(pipe.OD(i[0]), i[1])

if __name__ == '__main__':
    unittest.main()
