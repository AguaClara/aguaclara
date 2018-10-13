from aguaclara.core.units import unit_registry as u
from aguaclara.core.pipeline import *
from aguaclara.core.pipes import *

import numpy as np
import unittest


class PipelineUtilityTest(unittest.TestCase):

    def test_pipeline_flow(self):
        pipes = np.array([
            Pipe(3 * u.inch, 3 * u.m, 3 * u.m),
            Pipe(4 * u.inch, 4 * u.m, 4 * u.m),
            Pipe(5 * u.inch, 5 * u.m, 5 * u.m),
        ])
        pipeline = Pipeline(pipes)

        self.assertAlmostEqual(pipeline.q(5 * u.m), 0.018149097841279497 * u.m**3 / u.s)


if __name__ == '__main__':
    unittest.main()
