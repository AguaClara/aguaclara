import unittest
import os

import pandas as pd
import numpy as np

from aguaclara.core.units import unit_registry as u
from aguaclara.core import pipes

# TODO: Rewrite this testing class.
# class TestPipes(unittest.TestCase):
#
#     def test_pipes(self):
#         pipe = pipes.Pipe(nd=(7.0 * u.inch), sdr=35.0)
#         pipe_df = pd.read_csv(os.path.join(
#             os.path.dirname(__file__),
#             '../../aguaclara/core/data/pipe_database.csv'
#         ))
#         assert_list_almost_equal = np.vectorize(self.assertAlmostEqual)
#         assert_list_almost_equal(
#             [
#                 pipe.od,
#                 pipe.id_sdr,
#                 pipe.id_sch40,
#             ],
#             [
#                 7.625 * u.inch,
#                 7.1892857 * u.inch,
#                 7.023 * u.inch,
#             ]
#         )
#         assert_list_almost_equal(
#             [
#                 pipes.ND_all_available(),
#                 pipes.ID_SDR_all_available(35.0),
#                 pipes.ND_SDR_available(7.1892857 * u.inch, 35.0),
#                 pipes.ND_available(4.7 * u.inch)
#             ],
#             [
#                 (pipe_df[pipe_df['Used'] == 1]['NDinch'].values) * u.inch,
#                 (pipe_df['NDinch'].values * 0.1142856) * u.inch,
#                 7.0 * u.inch,
#                 6.0 * u.inch
#             ]
#         )
