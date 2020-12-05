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
        self.assertEqual(pipe.sch(), (8*u.inch, (pipes.SCH.SCH80.name)))
        self.assertEqual(pipe.sch(NDarr=[10]*u.inch), (10*u.inch, (pipes.SCH.SCH160.name)))


    def test_OD_from_IDSDR(self):
        #test that SDR=2 is undefined.
        with self.assertRaises(ValueError): pipes.OD_SDR(1*u.inch,2)
        #test other cases
        self.assertAlmostEqual(pipes.OD_SDR(1*u.inch,2.5),6.625*u.inch)
        self.assertAlmostEqual(pipes.OD_SDR(1*u.inch,2.25),10.75*u.inch)
        self.assertAlmostEqual(pipes.OD_SDR(.27*u.inch,(.4/.07)),.84*u.inch)
        #one that is already there
        self.assertAlmostEqual(pipes.OD_SDR(4.026*u.inch,(4.5/0.237)),4.5*u.inch)

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

        self.assertEqual(pipe.sch(), (24*u.inch, (pipes.SCH.SCH160.name)))
        self.assertEqual(pipe.sch(NDarr=[24]*u.inch,SCHarr=[pipes.SCH.SCH160]), (24*u.inch, (pipes.SCH.SCH160.name)))

        self.assertEqual(pipe.sch(SCHarr=[pipes.SCH.SCH160, pipes.SCH.SCH40]), (24*u.inch, (pipes.SCH.SCH160.name)))
        self.assertEqual(pipe.sch(NDarr=[20,24]*u.inch), (24*u.inch, (pipes.SCH.SCH160.name)))
        self.assertEqual(pipe.sch(NDarr=[16]*u.inch), None)


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
        self.assertEqual(pipe2.sch(), None)

    def test_ND_all_available(self):
        ndarrsol = [0.5,1,1.5,2,3,4,6,8,10,12,16,18,24,30,36,48,60,72] * u.inch
        ndarr = pipes.ND_all_available()
        np.testing.assert_array_equal(ndarr.magnitude, ndarrsol.magnitude)

    def test_OD_all_available(self):
        odarrsol = [0.84,1.315,1.9,2.375,3.5,4.5,6.625,8.625,10.75,12.75,16,18,24,30,36,48,60,72] * u.inch
        odarr = pipes.OD_all_available()
        np.testing.assert_array_equal(odarr.magnitude, odarrsol.magnitude)

    def test_OD(self): 
        #values on table        
        self.assertAlmostEqual(pipes.OD(.125 * u.inch), .404 * u.inch)
        self.assertAlmostEqual(pipes.OD(2 * u.inch), 2.375 * u.inch)
        self.assertAlmostEqual(pipes.OD(8 * u.inch), 8.625 * u.inch)
        self.assertAlmostEqual(pipes.OD(46 * u.inch), 46 * u.inch)
        self.assertAlmostEqual(pipes.OD(92 * u.inch), 92 * u.inch)

        #values in between official NDs
        self.assertAlmostEqual(pipes.OD(2.25 * u.inch), 2.875 * u.inch)
        self.assertAlmostEqual(pipes.OD(4.1 * u.inch), 5 * u.inch)
        self.assertAlmostEqual(pipes.OD(4.4 * u.inch), 5 * u.inch)
        self.assertAlmostEqual(pipes.OD(4.6 * u.inch), 5.563 * u.inch)
        self.assertAlmostEqual(pipes.OD(33 * u.inch), 34 * u.inch)

    def test_sch_all_available(self):
        ans = [(10*u.inch, pipes.SCH.SCH160.name),(12*u.inch, pipes.SCH.SCH160.name)]
        arr = pipes.SCH_all_available(7.189285714*u.inch,10)
        for i in range(len(ans)):
            self.assertEqual(arr[i], ans[i])


    def test_OD_SDR(self):
        self.assertAlmostEqual(pipes.OD_SDR(5*u.inch, 20), 6.625*u.inch)
        self.assertAlmostEqual(pipes.OD_SDR(10*u.inch, 40), 10.75*u.inch)
        self.assertAlmostEqual(pipes.OD_SDR(2.5*u.inch, 10), 3.5*u.inch)

    def test_ID_SCH(self):
         self.assertAlmostEqual(pipes.ID_sch(20*u.inch, pipes.SCH.SCH40), 19.25 * u.inch)
         self.assertAlmostEqual(pipes.ID_sch(20*u.inch, pipes.SCH.SCH80), 17.938 * u.inch)


"""
functions to write tests for:
Pipe -- DONE
- od
- id_sdr
- id_sch
- sch

- sch_all_available

- fitting_od
- ID_SDR
- ID_sch
- ID_SDR_all_available
- ND_SDR_available
- ND_available
- OD_available
- socket_depth
- cap_thickness

DONE: 
- OD_all_available
- ND_all_available
- makePipe_ND_SDR
- makePipe_minID_SDR
- OD
- OD_from_IDSDR
"""