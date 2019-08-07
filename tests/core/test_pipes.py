import unittest
import os

import pandas as pd
import numpy as np

from aguaclara.core.units import u
from aguaclara.core import pipes

class TestPipes(unittest.TestCase):

    def test_pipes(self):
        pipe = pipes.Pipe(nd=(7.0 * u.inch), sdr=35.0)
        pipe_df = pd.read_csv(os.path.join(
            os.path.dirname(__file__),
            '../../aguaclara/core/data/pipe_database.csv'
        ))
        self.assertAlmostEqual(pipe.od, 7.625 * u.inch)
        self.assertAlmostEqual(pipe.id_sdr, 7.189285714285714 * u.inch)
        self.assertAlmostEqual(pipe.id_sch40, 7.023 * u.inch)

        self.assertAlmostEqual(pipes.ND_SDR_available(7.1892857 * u.inch, 35.0), 8.0 * u.inch)
        self.assertAlmostEqual(pipes.ND_available(4.7 * u.inch), 6.0 * u.inch)

