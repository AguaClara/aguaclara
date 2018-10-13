import unittest
import os

import pandas as pd

from aguaclara.core import pipes
from aguaclara.core.units import unit_registry as u


class TestPipes(unittest.TestCase):

    def test_pipes(self):
        pipe = Pipe(nd=(7.0 * u.inch), sdr=35.0)
        pipe_df = pd.read_csv(os.path.join(
            os.path.dirname(__file__),
            'aguaclara/core/data/pipe_database.csv'
        ))
        unittest.assertAlmostEqual(
            [
                pipe.od(),
                pipe.id_sdr(),
                pipe.id_sch40(),
            ],
            [
                7.625 * u.inch,
                7.1892857 * u.inch,
                7.023 * u.inch,
            ]
        )
        unittest.assertAlmostEqual(
            [
                pipes.nd_all_available(),
                pipes.id_sdr_all_available(35.0),
                pipes.nd_sdr_available(7.1892857, 35.0),
                pipes.nd_available(4.7)
            ],
            [
                (pipe_df[pipe_df['Used'] == 1]['NDinch'].values) * u.inch,
                (pipe_df['NDinch'].values * 0.1142856) * u.inch,
                7.0 * u.inch,
                6.0 * u.inch
            ]
        )


if __name__ == '__main__':
    unittest.main()
