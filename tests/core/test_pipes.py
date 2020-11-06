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
        self.assertAlmostEqual(pipe.id_sch(pipes.SCH.SCH40), 7.023 * u.inch)

        self.assertAlmostEqual(pipes.ND_SDR_available(7.1892857 * u.inch, 35.0), 8.0 * u.inch)
        self.assertAlmostEqual(pipes.ND_available(4.7 * u.inch), 6.0 * u.inch)



    # def test_OD(self):


    def test_OD_from_IDSDR(self):
        #test that SDR=2 is undefined.
        with self.assertRaises(ValueError): pipes.OD_from_IDSDR(1*u.inch,2)
        #test other cases
        self.assertAlmostEqual(pipes.OD_from_IDSDR(1*u.inch,2.5),6.625*u.inch)
        self.assertAlmostEqual(pipes.OD_from_IDSDR(1*u.inch,2.25),10.75*u.inch)
        self.assertAlmostEqual(pipes.OD_from_IDSDR(.27*u.inch,(.4/.07)),.84*u.inch)
        #one that is already there
        self.assertAlmostEqual(pipes.OD_from_IDSDR(4.026*u.inch,(4.5/0.237)),4.5*u.inch)

    def test_makePipe_ND_SDR(self):
        #used=1 at this nominal diameter
        pipe = pipes.makePipe_ND_SDR(8*u.inch,5.75)
        self.assertAlmostEqual(pipe.od, 8.625 * u.inch)
        self.assertAlmostEqual(pipe.id_sdr, 5.625 * u.inch)
        self.assertAlmostEqual(pipe.id_sch(pipes.SCH.SCH40), 7.981 * u.inch)
        self.assertAlmostEqual(pipe.id_sch(pipes.SCH.SCH80), 7.625 * u.inch)

        #used=0 at this nominal diameter
        pipe = pipes.makePipe_ND_SDR(20*u.inch,20)
        self.assertAlmostEqual(pipe.od, 20 * u.inch)
        self.assertAlmostEqual(pipe.id_sdr, 18 * u.inch)
        self.assertAlmostEqual(pipe.id_sch(pipes.SCH.SCH40), 19.25 * u.inch)
        self.assertAlmostEqual(pipe.id_sch(pipes.SCH.SCH80), 17.938 * u.inch)
        self.assertEqual(pipe.sch(), (24*u.inch, (pipes.SCH.SCH80.name)))
        

    def test_makePipe_minID_SDR(self):
        #used=0, matches with sched40 ID
        pipe = pipes.makePipe_ND_SDR(.824*u.inch,1.05/.113)
        self.assertAlmostEqual(pipe.od, 1.05 * u.inch)
        self.assertAlmostEqual(pipe.id_sdr, .824 * u.inch)
        self.assertAlmostEqual(pipe.id_sch(pipes.SCH.SCH40), .824 * u.inch)
        self.assertAlmostEqual(pipe.id_sch(pipes.SCH.SCH80), .742 * u.inch)
        

        #used=0, does not match with sched40 ID
        pipe2 = pipes.makePipe_minID_SDR(.8*u.inch,5)
        self.assertAlmostEqual(pipe2.od, 1.9 * u.inch)
        self.assertAlmostEqual(pipe2.id_sdr, 1.14 * u.inch)
        self.assertAlmostEqual(pipe2.id_sch(pipes.SCH.SCH40), 1.61 * u.inch)
        self.assertAlmostEqual(pipe2.id_sch(pipes.SCH.SCH80), 1.5 * u.inch)
        print("nd", pipe2.nd)
        print("id", pipe2.id_sdr)
        print("sdr", pipe2.sdr)
        self.assertEqual(pipe2.sch(), (.5*u.inch, (pipes.SCH.SCH160.name)))
