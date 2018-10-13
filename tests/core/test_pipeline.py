from aguaclara.core.units import unit_registry as u
from aguaclara.core.pipeline import *
from aguaclara.core.pipes import *

import numpy as np
import unittest


class PipelineUtilityTest(unittest.TestCase):

    def test_pipeline_flow(self):
        pipes = np.array([
            Pipe(3 * u.inch, 3 * u.m, 3 * u.m),
        ])
        pipeline = Pipeline(pipes)
        flow = pipeline.flow_pipeline(np.array([3,4,5])*u.inch, np.array([3,4,5])*u.m, np.array([3,4,5]), 5 *u.m)
        self.assertAlmostEqual(flow.magnitude, 0.018149097841279497 * u.m**3 / u.s)


if __name__ == '__main__':
    unittest.main()
