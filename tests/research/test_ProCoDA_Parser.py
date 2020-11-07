"""
Tests for the research package's ProCoDA parsing functions
"""

import unittest
import aguaclara.research.procoda_parser as pp
from aguaclara.core.units import u
import pandas as pd
import numpy as np
import os
from matplotlib.testing.compare import compare_images
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt


class TestProCoDAParser(unittest.TestCase):

    def test_column_of_data(self):
        '''''
        Extract other columns of data and append units.
        '''''
        path = os.path.join(os.path.dirname(__file__), '.', 'data', 'example datalog.xls')
        answer = pp.column_of_data(path, 50, 1, units='mg/L')
        answer = np.round(answer, 5)
        self.assertSequenceEqual(
        answer.tolist(),
        np.round(np.array([ 21.61681747,  21.31163216,  20.80215263,  20.46752739,
        20.1048584 ,  19.7037487 ,  19.4194355 ,  18.95934677,
        18.65832138,  18.24054337,  17.93864632,  17.591259  ,
        17.25979805,  16.98148346,  16.60666656,  16.28514862,
        15.99366856,  15.72474861,  15.35812187,  15.11634636,
        14.75801468,  14.53341103,  14.20829868,  13.94124603,
        13.69845104,  13.42016983,  13.17064667,  12.94155121,
        12.66110611,  12.36821651,  12.1641016 ,  11.91081715,
        11.69137764,  11.46448898,  11.2214098 ,  11.03143692,
        10.78680801,  10.56936836,  10.36802101,  10.17097855,
         9.95537758,   9.78312111,   9.55150509,   9.3843832 ,
         9.21883678,   9.03395939,   8.85475636,   8.68857765,
         8.47574997,   8.33256149,   8.13628197,   7.96697569,
         7.80458403,   7.68562984,   7.4511261 ,   7.34629679,
         7.17365456,   7.03930044,   6.88661861,   6.73307562,
         6.60730886,   6.45987988,   6.30656338,   6.18089199,
         6.05378485,   5.90268421,   5.81327915,   5.68042564,
         5.57657337,   5.40122986,   5.33153057,   5.19660377,
         5.09033108,   4.96228552,   4.85437012,   4.76652002,
         4.66415834,   4.54592991,   4.43500376,   4.34614754,
         4.24292231,   4.16423607,   4.06328297,   3.96581864,
         3.88231015,   3.7828486 ,   3.74253488,   3.62953901,
         3.53508115,   3.46755266,   3.36818004,   3.30672598,
         3.22161722,   3.13899183,   3.08345532,   2.98398542,
         2.94956589,   2.8504107 ,   2.79215455,   2.72924852,
         2.66635823,   2.60831141,   2.53093195,   2.47217631,
         2.42190933,   2.36228228,   2.30094266,   2.24602866,
         2.19216943,   2.14143515,   2.10641694,   2.07170939,
         2.04412961,   2.0158174 ,   2.00059986,   1.98546684,
         1.97646523,   1.96455812,   1.95887971,   1.94987118])*u('mg/L'), 5).tolist()
        )

        path = os.path.join(os.path.dirname(__file__), '.', 'data', 'example datalog.xls')
        answer = pp.column_of_data(path, 50, "red dye (mg/L)", units='mg/L')
        answer = np.round(answer, 5)
        self.assertSequenceEqual(
        answer.tolist(),
        np.round(np.array([ 21.61681747,  21.31163216,  20.80215263,  20.46752739,
        20.1048584 ,  19.7037487 ,  19.4194355 ,  18.95934677,
        18.65832138,  18.24054337,  17.93864632,  17.591259  ,
        17.25979805,  16.98148346,  16.60666656,  16.28514862,
        15.99366856,  15.72474861,  15.35812187,  15.11634636,
        14.75801468,  14.53341103,  14.20829868,  13.94124603,
        13.69845104,  13.42016983,  13.17064667,  12.94155121,
        12.66110611,  12.36821651,  12.1641016 ,  11.91081715,
        11.69137764,  11.46448898,  11.2214098 ,  11.03143692,
        10.78680801,  10.56936836,  10.36802101,  10.17097855,
         9.95537758,   9.78312111,   9.55150509,   9.3843832 ,
         9.21883678,   9.03395939,   8.85475636,   8.68857765,
         8.47574997,   8.33256149,   8.13628197,   7.96697569,
         7.80458403,   7.68562984,   7.4511261 ,   7.34629679,
         7.17365456,   7.03930044,   6.88661861,   6.73307562,
         6.60730886,   6.45987988,   6.30656338,   6.18089199,
         6.05378485,   5.90268421,   5.81327915,   5.68042564,
         5.57657337,   5.40122986,   5.33153057,   5.19660377,
         5.09033108,   4.96228552,   4.85437012,   4.76652002,
         4.66415834,   4.54592991,   4.43500376,   4.34614754,
         4.24292231,   4.16423607,   4.06328297,   3.96581864,
         3.88231015,   3.7828486 ,   3.74253488,   3.62953901,
         3.53508115,   3.46755266,   3.36818004,   3.30672598,
         3.22161722,   3.13899183,   3.08345532,   2.98398542,
         2.94956589,   2.8504107 ,   2.79215455,   2.72924852,
         2.66635823,   2.60831141,   2.53093195,   2.47217631,
         2.42190933,   2.36228228,   2.30094266,   2.24602866,
         2.19216943,   2.14143515,   2.10641694,   2.07170939,
         2.04412961,   2.0158174 ,   2.00059986,   1.98546684,
         1.97646523,   1.96455812,   1.95887971,   1.94987118])*u('mg/L'), 5).tolist()
        )


    def test_column_of_time(self):
        '''''
        Extract the time column from a data file.
        '''''
        path = os.path.join(os.path.dirname(__file__), '.', 'data', 'example datalog.xls')
        answer = pp.column_of_time(path, 50)
        answer = np.round(answer, 5)
        self.assertSequenceEqual(
         answer.tolist(),
         np.round(np.array([0.00000000e+00,   5.78662000e-05,   1.15725500e-04,
         1.73586900e-04,   2.31470400e-04,   2.89325100e-04,
         3.47199600e-04,   4.05070800e-04,   4.62941200e-04,
         5.20805100e-04,   5.78682300e-04,   6.36541000e-04,
         6.94405500e-04,   7.52295200e-04,   8.10152600e-04,
         8.68025100e-04,   9.25879200e-04,   9.83766900e-04,
         1.04163170e-03,   1.09949610e-03,   1.15736260e-03,
         1.21522990e-03,   1.27310590e-03,   1.33096560e-03,
         1.38884810e-03,   1.44671260e-03,   1.50456890e-03,
         1.56244910e-03,   1.62031940e-03,   1.67819090e-03,
         1.73605480e-03,   1.79390590e-03,   1.85178640e-03,
         1.90965780e-03,   1.96752080e-03,   2.02538760e-03,
         2.08325540e-03,   2.14113380e-03,   2.19899280e-03,
         2.25686180e-03,   2.31473400e-03,   2.37261100e-03,
         2.43048170e-03,   2.48834570e-03,   2.54620210e-03,
         2.60408890e-03,   2.66194550e-03,   2.71981170e-03,
         2.77768240e-03,   2.83556180e-03,   2.89342620e-03,
         2.95130110e-03,   3.00916580e-03,   3.06704400e-03,
         3.12490300e-03,   3.18278490e-03,   3.24064920e-03,
         3.29852180e-03,   3.35638230e-03,   3.41425150e-03,
         3.47212870e-03,   3.52999870e-03,   3.58786830e-03,
         3.64572740e-03,   3.70359810e-03,   3.76146930e-03,
         3.81933520e-03,   3.87721010e-03,   3.93506860e-03,
         3.99295440e-03,   4.05082240e-03,   4.10868470e-03,
         4.16654890e-03,   4.22442890e-03,   4.28230160e-03,
         4.34016650e-03,   4.39804130e-03,   4.45591720e-03,
         4.51377060e-03,   4.57164920e-03,   4.62952340e-03,
         4.68739510e-03,   4.74524320e-03,   4.80312930e-03,
         4.86098350e-03,   4.91887450e-03,   4.97673430e-03,
         5.03459310e-03,   5.09248050e-03,   5.15033640e-03,
         5.20820950e-03,   5.26607440e-03,   5.32394690e-03,
         5.38181660e-03,   5.43967960e-03,   5.49755470e-03,
         5.55543130e-03,   5.61330110e-03,   5.67117330e-03,
         5.72903190e-03,   5.78690100e-03,   5.84477570e-03,
         5.90264880e-03,   5.96051240e-03,   6.01837960e-03,
         6.07625150e-03,   6.13413050e-03,   6.19199110e-03,
         6.24987260e-03,   6.30772900e-03,   6.36560880e-03,
         6.42346920e-03,   6.48135320e-03,   6.53921020e-03,
         6.59709090e-03,   6.65494290e-03,   6.71281870e-03,
         6.77069570e-03,   6.82855640e-03,   6.88642010e-03])*u.day, 5).tolist()
        )

        answer = pp.column_of_time(path, 50, end=60, units='hr')
        answer = np.round(answer, 5)
        self.assertSequenceEqual(
         answer.tolist(),
         np.round(np.array([0.00000000e+00,   5.78662000e-05,   1.15725500e-04,
         1.73586900e-04,   2.31470400e-04,   2.89325100e-04,
         3.47199600e-04,   4.05070800e-04,   4.62941200e-04,
         5.20805100e-04])*24*u.hr, 5).tolist()
        )


    def test_notes(self):
        '''''
        Test function that extracts meta information from data file.
        '''''
        path = os.path.join(os.path.dirname(__file__), '.', 'data', 'example datalog.xls')
        answer = pp.notes(path)['Day fraction since midnight on ']
        x = pd.DataFrame(index=[1, 29, 35],
                         columns=['Day fraction since midnight on ', 'red dye (mg/L)', 'Run Pump ()', 'Pump ()'])
        x.iloc[0][0] = 'Start'
        x.iloc[1][0] = 'Start'
        x.iloc[2][0] = '30 mg/L'
        self.assertSequenceEqual(
        answer.tolist(),
        x['Day fraction since midnight on '].tolist())


    def test_remove_notes(self):
        '''
        Return a DataFrame without any lines that originally contained text
        '''
        path = os.path.join(os.path.dirname(__file__), '.', 'data')

        output = pp.remove_notes(pd.read_csv(path + '/example datalog.xls', delimiter='\t'))

        self.assertSequenceEqual(np.round(pd.to_numeric(output.iloc[:, 0]), 5).tolist(), np.round(np.array(
            [0.6842773323, 0.6843351954, 0.6843930789, 0.6844509555, 0.6845088278,
                0.6845666989, 0.6846245615, 0.6846824172, 0.6847402968, 0.6847981752,
                0.6848560403, 0.6849139126, 0.6849717883, 0.6850296562, 0.6850875147,
                0.6851453919, 0.6852032725, 0.6852611229, 0.6853190069, 0.6853768753,
                0.6854347496, 0.6854926132, 0.6855504820, 0.6856083520, 0.6856662182,
                0.6857240844, 0.6857819618, 0.6858398270, 0.6858977139, 0.6859555700,
                0.6860134505, 0.6860713232, 0.6861291842, 0.6861870457, 0.6862449249,
                0.6863027915, 0.6863606668, 0.6864185391, 0.6864764071, 0.6865342703,
                0.6865921393, 0.6866500041, 0.6867078679, 0.6867657506, 0.6868236041,
                0.6868814757, 0.6869393510, 0.6869972210, 0.6870550872, 0.6871129465,
                0.6871708079, 0.6872286914, 0.6872865461, 0.6873444206, 0.6874022918,
                0.6874601622, 0.6875180261, 0.6875759033, 0.6876337620, 0.6876916265,
                0.6877495162, 0.6878073736, 0.6878652461, 0.6879231002, 0.6879809879,
                0.6880388527, 0.6880967171, 0.6881545836, 0.6882124509, 0.6882703269,
                0.6883281866, 0.6883860691, 0.6884439336, 0.6885017899, 0.6885596701,
                0.6886175404, 0.6886754119, 0.6887332758, 0.6887911269, 0.6888490074,
                0.6889068788, 0.6889647418, 0.6890226086, 0.6890804764, 0.6891383548,
                0.6891962138, 0.6892540828, 0.6893119550, 0.6893698320, 0.6894277027,
                0.6894855667, 0.6895434231, 0.6896013099, 0.6896591665, 0.6897170327,
                0.6897749034, 0.6898327828, 0.6898906472, 0.6899485221, 0.6900063868,
                0.6900642650, 0.6901221240, 0.6901800059, 0.6902378702, 0.6902957428,
                0.6903536033, 0.6904114725, 0.6904693497, 0.6905272197, 0.6905850893,
                0.6906429484, 0.6907008191, 0.6907586903, 0.6908165562, 0.6908744311,
                0.6909322896, 0.6909901754, 0.6910480434, 0.6911059057, 0.6911637699,
                0.6912216499, 0.6912795226, 0.6913373875, 0.6913952623, 0.6914531382,
                0.6915109916, 0.6915688702, 0.6916267444, 0.6916846161, 0.6917424642,
                0.6918003503, 0.6918582045, 0.6919160955, 0.6919739553, 0.6920318141,
                0.6920897015, 0.6921475574, 0.6922054305, 0.6922632954, 0.6923211679,
                0.6923790376, 0.6924369006, 0.6924947757, 0.6925526523, 0.6926105221,
                0.6926683943, 0.6927262529, 0.6927841220, 0.6928419967, 0.6928998698,
                0.6929577334, 0.6930156006, 0.6930734725, 0.6931313515, 0.6931892121,
                0.6932470936, 0.6933049500, 0.6933628298, 0.6934206902, 0.6934785742,
                0.6935364312, 0.6935943119, 0.6936521639, 0.6937100397, 0.6937679167,
                0.6938257774, 0.6938836411]), 5).tolist())


    def test_get_data_by_time(self):
        '''
        Extract column(s) of data between given starting and ending days and times
        '''
        path = os.path.join(os.path.dirname(__file__), '.', 'data')

        data_day1 = pd.read_csv(path + '/datalog_6-14-2018.xls', delimiter='\t')
        data_day1 = np.round([pd.to_numeric(data_day1.iloc[:, 0]), pd.to_numeric(data_day1.iloc[:, 4])], 5)
        data_day1 = [data_day1[0].tolist(), data_day1[1].tolist()]

        data_day2 = pd.read_csv(path + '/datalog_6-15-2018.xls', delimiter='\t')
        data_day2 = np.round([pd.to_numeric(data_day2.iloc[:, 0]), pd.to_numeric(data_day2.iloc[:, 4])], 5)
        data_day2 = [data_day2[0].tolist(), data_day2[1].tolist()]
        data_day2[0][0] = 0  # to remove scientific notation "e-"

        # SINGLE COLUMN, ONE DAY
        output = pp.get_data_by_time(path=path, columns=0, dates="6-14-2018", start_time="12:20",
                                  end_time="13:00", extension=".xls")
        self.assertSequenceEqual(np.round(output, 5).tolist(), data_day1[0][1041:1282])

        # SINGLE COLUMN, TWO DAYS
        output = pp.get_data_by_time(path=path, columns=0, dates=["6-14-2018", "6-15-2018"],
                                  start_time="12:20", end_time="10:50", extension=".xls")
        time_column = data_day1[0][1041:] + np.round(np.array(data_day2[0][:3901])+1, 5).tolist()
        self.assertSequenceEqual(np.round(output, 5).tolist(), time_column)

        # MULTI COLUMN, ONE DAY
        output = pp.get_data_by_time(path=path, columns=[0, 4], dates=["6-14-2018"], start_time="12:20",
                                  end_time="13:00", extension=".xls")
        self.assertSequenceEqual(np.round(output[0], 5).tolist(), data_day1[0][1041:1282])
        self.assertSequenceEqual(np.round(output[1], 5).tolist(), data_day1[1][1041:1282])

        # MULTI COLUMN, TWO DAYS
        output = pp.get_data_by_time(path=path, columns=[0, 4], dates=["6-14-2018", "6-15-2018"],
                                  start_time="12:20", end_time="10:50", extension=".xls")
        time_column = data_day1[0][1041:] + np.round(np.array(data_day2[0][:3901])+1, 5).tolist()
        self.assertSequenceEqual(np.round(output[0], 5).tolist(), time_column)
        self.assertSequenceEqual(np.round(output[1], 5).tolist(), data_day1[1][1041:]+data_day2[1][:3901])

        # MULTI COLUMN, TWO DAYS, WITH UNITS
        output = pp.get_data_by_time(path=path, columns=[0, 4], dates=["6-14-2018", "6-15-2018"],
                                  start_time="12:20", end_time="10:50", extension=".xls", units=['day', 'mg/L'])
        time_column = data_day1[0][1041:] + np.round(np.array(data_day2[0][:3901])+1, 5).tolist()
        self.assertEqual(output[0].units, u.day)
        self.assertSequenceEqual(np.round(output[0].magnitude, 5).tolist(), time_column)
        self.assertEqual(output[1].units, u.mg/u.L)
        self.assertSequenceEqual(np.round(output[1].magnitude, 5).tolist(), data_day1[1][1041:]+data_day2[1][:3901])

        ######## WITH ELAPSED TIME ########
        start = pp.day_fraction("12:20")
        data_day1 = pd.read_csv(path + '/datalog_6-14-2018.xls', delimiter='\t')
        data_day1 = [np.round(pd.to_numeric(data_day1.iloc[:, 0]) - start, 5).tolist(),
                     np.round(pd.to_numeric(data_day1.iloc[:, 4]), 5).tolist()]

        data_day2 = pd.read_csv(path + '/datalog_6-15-2018.xls', delimiter='\t')
        data_day2.iloc[0,0] = 0  # to remove scientific notation "e-"
        data_day2 = [np.round(pd.to_numeric(data_day2.iloc[:, 0]) - start + 1, 5).tolist(),
                     np.round(pd.to_numeric(data_day2.iloc[:, 4]), 5).tolist()]

        #  SINGLE COLUMN, ONE DAY
        output = pp.get_data_by_time(path=path, columns=0, dates="6-14-2018", start_time="12:20",
                                  end_time="13:00", extension=".xls", elapsed=True)
        self.assertSequenceEqual(np.round(output, 5).tolist(), data_day1[0][1041:1282])

         # MULTI COLUMN, TWO DAYS
        output = pp.get_data_by_time(path=path, columns=[0, 4], dates=["6-14-2018", "6-15-2018"],
                                  start_time="12:20", end_time="10:50", extension=".xls",
                                  elapsed=True)
        self.assertSequenceEqual(np.round(output[0], 5).tolist(), data_day1[0][1041:]+data_day2[0][:3901])
        self.assertSequenceEqual(np.round(output[1], 5).tolist(), data_day1[1][1041:]+data_day2[1][:3901])


    def test_day_fraction(self):
        '''
        Converts time into a fraction of the day
        '''
        time = pp.day_fraction(time="12:00")
        self.assertEqual(time, 0.5)


    def test_data_from_dates(self):
        '''
        Return a list of DataFrames representing the ProCoDA data files stored in the given path and recorded on the given dates.
        '''
        path = os.path.join(os.path.dirname(__file__), '.', 'data')
        dataFromPath = pd.read_csv(path + '/datalog_6-15-2018.xls', delimiter='\t')

        getDataFromDates = pp.data_from_dates(path=path, dates='6-15-2018', extension=".xls")[0]

        self.assertTrue(getDataFromDates.equals(dataFromPath))


    def test_column_start_to_end(self):
        '''
        Return entries in column from starting index in first DataFrame to ending index in last DataFrame
        '''
        #One DataFrame
        path = os.path.join(os.path.dirname(__file__), '.', 'data')
        data_manual1 = pd.read_csv(path + '/datalog_6-14-2018.xls', delimiter='\t')

        getColData1 = pp.column_start_to_end(data=[data_manual1], column=1, start_idx=2, end_idx=7)
        compareColData1 = [-4.34825945, -2.3821919, -2.57200098, -2.40549088,
            -1.00214481]
        self.assertSequenceEqual(getColData1, compareColData1)

        #Three DataFrames
        data_manual2 = pd.read_csv(path + '/datalog_6-16-2018.xls', delimiter='\t')
        data_manual3 = pd.read_csv(path + '/datalog_6-15-2018.xls', delimiter='\t')

        getColData2 = pp.column_start_to_end([data_manual1, data_manual2, data_manual3],
            column=2, start_idx=5238, end_idx=2)
        compareColData2 = [24.26625443, 24.2669487, 24.26613235, 24.26708603,
            24.26683617, 24.26708603, 24.26683617]
        self.assertSequenceEqual(getColData2, compareColData2)


    def test_get_data_by_state(self):
        '''
        Extract the time column and a data column for each iteration of a state
        '''
        path = os.path.join(os.path.dirname(__file__), '.', 'data')

        # Local path
        output = pp.get_data_by_state(path, dates="6-19-2013", state=1, column=1, extension=".xls")  # , "6-20-2013"

        datafile = pd.read_csv(path + "/datalog_6-19-2013.xls", delimiter='\t')
        time_and_data1 = np.array([pd.to_numeric(datafile.iloc[:, 0]),
                                   np.round(pd.to_numeric(datafile.iloc[:, 1]), 5)])
        start_time = time_and_data1[0, 0]
        answer = [time_and_data1[:, 98:175], time_and_data1[:, 220:485],
                  time_and_data1[:, 3039:3304], time_and_data1[:, 5858:6123],
                  time_and_data1[:, 8677:8942], time_and_data1[:, 11496:11761],
                  time_and_data1[:, 14315:14580]]

        for i in range(len(output)):
            output_i = np.round(np.array(output[i]).astype(np.double), 5)
            self.assertSequenceEqual([j[0] for j in output_i], [round(j-start_time, 5) for j in answer[i][0]])
            self.assertSequenceEqual([j[1] for j in output_i], [j for j in answer[i][1]])

        # Acceptable URL
        url_acceptable = 'https://raw.githubusercontent.com/monroews/playing/master/ProCoDA_data'
        output = pp.get_data_by_state(url_acceptable, dates="11-5-2019", state=1, column=1, extension='.tsv')
        answer = pp.get_data_by_state(path, dates="11-5-2019", state=1, column=1, extension='.tsv')

        for i in range(len(output)):
            self.assertSequenceEqual([round(o, 5) for o in output[i][:,0]], [round(a, 5) for a in answer[i][:,0]])
            self.assertSequenceEqual([round(o, 5) for o in output[i][:,1]], [round(a, 5) for a in answer[i][:,1]])

        # Github.com URL (blob)
        url_github = 'https://github.com/monroews/playing/blob/master/ProCoDA_data'
        output = pp.get_data_by_state(url_github, dates="11-5-2019", state=1, column=1, extension='.tsv')
        for i in range(len(output)):
            self.assertSequenceEqual([round(o, 5) for o in output[i][:,0]], [round(a, 5) for a in answer[i][:,0]])
            self.assertSequenceEqual([round(o, 5) for o in output[i][:,1]], [round(a, 5) for a in answer[i][:,1]])

         # Github.com URL (tree)
        url_github = 'https://github.com/monroews/playing/tree/master/ProCoDA_data'
        output = pp.get_data_by_state(url_github, dates="11-5-2019", state=1, column=1, extension='.tsv')
        for i in range(len(output)):
            self.assertSequenceEqual([round(o, 5) for o in output[i][:,0]], [round(a, 5) for a in answer[i][:,0]])
            self.assertSequenceEqual([round(o, 5) for o in output[i][:,1]], [round(a, 5) for a in answer[i][:,1]])


    def test_plot_columns(self):
        '''
        Plot the columns of data given the file located by labels
        '''
        path = os.path.join(os.path.dirname(__file__), '.', 'data') + '/statelog_6-14-2018.xls'

        plt.figure()
        pp.plot_columns(path=path, columns=" State ID")
        plt.savefig("Image1.png")
        plt.figure()
        plt.plot([0,1,0,1,2])
        plt.savefig("Image2.png")
        self.assertEqual(None, compare_images("Image2.png", "Image1.png", 0))

        plt.figure()
        pp.plot_columns(path=path, columns=" State ID", x_axis=" State ID")
        plt.savefig("Image3.png")
        plt.figure()
        plt.plot([0,1,0,1,2], [0,1,0,1,2])
        plt.savefig("Image4.png")
        self.assertEqual(None, compare_images("Image4.png", "Image3.png", 0))

        plt.figure()
        pp.plot_columns(path=path, columns=[" State ID"])
        plt.savefig("Image5.png")
        self.assertEqual(None, compare_images("Image1.png", "Image5.png", 0))

        plt.figure()
        pp.plot_columns(path=path, columns=[" State ID"], x_axis=" State ID")
        plt.savefig("Image6.png")
        self.assertEqual(None, compare_images("Image4.png", "Image6.png", 0))

        self.assertRaisesRegex(ValueError, 'columns must be a string or list of strings',
                                                        pp.plot_columns, *(path, 9))

        os.remove("Image1.png")
        os.remove("Image2.png")
        os.remove("Image3.png")
        os.remove("Image4.png")
        os.remove("Image5.png")
        os.remove("Image6.png")


    def test_iplot_columns(self):
        '''
        Plot the columns of data given the file located by indices
        '''
        path = os.path.join(os.path.dirname(__file__), '.', 'data') + '/statelog_6-14-2018.xls'

        plt.figure()
        pp.iplot_columns(path=path, columns=1)
        plt.savefig("Image1.png")
        plt.figure()
        plt.plot([0,1,0,1,2])
        plt.savefig("Image2.png")
        self.assertEqual(None, compare_images("Image2.png", "Image1.png", 0))

        plt.figure()
        pp.iplot_columns(path=path, columns=1, x_axis=1)
        plt.savefig("Image3.png")
        plt.figure()
        plt.plot([0,1,0,1,2], [0,1,0,1,2])
        plt.savefig("Image4.png")
        self.assertEqual(None, compare_images("Image4.png", "Image3.png", 0))

        plt.figure()
        pp.iplot_columns(path=path, columns=[1])
        plt.savefig("Image5.png")
        self.assertEqual(None, compare_images("Image1.png", "Image5.png", 0))

        plt.figure()
        pp.iplot_columns(path=path, columns=[1], x_axis=1)
        plt.savefig("Image6.png")
        self.assertEqual(None, compare_images("Image4.png", "Image6.png", 0))

        self.assertRaisesRegex(ValueError, 'columns must be an int or a list of ints',
                                                    pp.iplot_columns, *(path, ' State ID'))

        os.remove("Image1.png")
        os.remove("Image2.png")
        os.remove("Image3.png")
        os.remove("Image4.png")
        os.remove("Image5.png")
        os.remove("Image6.png")


    def test_read_state(self):
        path = os.path.join(os.path.dirname(__file__), '.', 'data', '')
        output_time, output_data = pp.read_state(["6-19-2013", "6-20-2013"], 1, 28, "mL/s", path, extension=".xls")

        df_day1 = pd.read_csv(path + "/datalog_6-19-2013.xls", delimiter='\t')
        df_day2 = pd.read_csv(path + "/datalog_6-20-2013.xls", delimiter='\t')

        time_day1 = df_day1.iloc[:,0]
        data_day1 = df_day1.iloc[:,28]
        time_day2 = df_day2.iloc[:,0] + 1
        data_day2 = df_day2.iloc[:,28]

        answer_time = pd.concat([
            time_day1[98:175], time_day1[220:485], time_day1[3039:3304],
            time_day1[5858:6123], time_day1[8677:8942], time_day1[11496:11761],
            time_day1[14315:14580],
            time_day2[1442:1707], time_day2[4261:4526], time_day2[7080:7345],
            time_day2[9899:10164], time_day2[12718:12983], time_day2[36572:40549],
            time_day2[41660:41694], time_day2[41696:41698]
            ]) - time_day1.iloc[0]

        answer_data = pd.concat([
            data_day1[98:175], data_day1[220:485], data_day1[3039:3304],
            data_day1[5858:6123], data_day1[8677:8942], data_day1[11496:11761],
            data_day1[14315:14580],
            data_day2[1442:1707], data_day2[4261:4526], data_day2[7080:7345],
            data_day2[9899:10164], data_day2[12718:12983], data_day2[36572:40549],
            data_day2[41660:41694], data_day2[41696:41698]
            ])

        self.assertEqual(output_time.units, u.day)
        self.assertSequenceEqual(list(output_time.magnitude), list(answer_time))
        self.assertEqual(output_data.units, u.mL/u.s)
        self.assertSequenceEqual(list(output_data.magnitude), list(answer_data))


    def test_average_state(self):
        path = os.path.join(os.path.dirname(__file__), '.', 'data', '')
        avgs = pp.average_state(["6-19-2013", "6-20-2013"], 1, 28, "mL/s", path,
                             extension=".xls")
        avgs = np.round(avgs, 5)

        self.assertSequenceEqual(
        avgs.tolist(),
        [5.5, 5.5, 5.5, 5.43125, 5.42094, 5.40908, 5.39544, 5.37976, 5.36172,
        5.34098, 5.31712, 5.28969, 5.5, 5.5, 5.5]*u.mL/u.s
        )

    def test_perform_function_on_state(self):
        path = os.path.join(os.path.dirname(__file__), '.', 'data', '')

        def avg_with_units(lst):
            num = np.size(lst)
            acc = 0
            for i in lst:
                acc = i + acc

            return acc / num

        avgs = pp.perform_function_on_state(avg_with_units,
                                         ["6-19-2013", "6-20-2013"], 1, 28,
                                         "mL/s", path, extension=".xls")
        avgs = np.round(avgs, 5)
        self.assertSequenceEqual(
        avgs.tolist(),
        [5.5, 5.5, 5.5, 5.43125, 5.42094, 5.40908, 5.39544, 5.37976, 5.36172,
        5.34098, 5.31712, 5.28969, 5.5, 5.5, 5.5]*u.mL/u.s
        )

    def test_read_state_with_metafile(self):
        path = os.path.join(os.path.dirname(__file__), '.', 'data', 'Test Meta File.txt')

        def avg_with_units(lst):
            num = np.size(lst)
            acc = 0
            for i in lst:
                acc = i + acc

            return acc / num

        ids, answer = pp.read_state_with_metafile(avg_with_units, 1, 28, path, [], ".xls", "mg/L")

        self.assertSequenceEqual(["1", "2"], ids.tolist())
        self.assertSequenceEqual([5.445427082723495, 5.459751965314751]*u.mg/u.L, answer)

    def test_write_calculations_to_csv(self):
        path = os.path.join(os.path.dirname(__file__), '.', 'data', 'Test Meta File.txt')
        out_path = os.path.join(os.path.dirname(__file__), '.', 'data', 'test_output.txt')

        def avg_with_units(lst):
            num = np.size(lst)
            acc = 0
            for i in lst:
                acc = i + acc

            return acc / num

        output = pp.write_calculations_to_csv(avg_with_units, 1, 28, path,
                                           ["Average Conc (mg/L)"], out_path,
                                           extension=".xls")

        self.assertSequenceEqual(["1", "2"], output['ID'].tolist())
        self.assertSequenceEqual(
        [5.445427082723495, 5.459751965314751],
        output['Average Conc (mg/L)'].tolist())

    def test_intersect(self):
        #tests one crossing
        x = np.array([1,2,3])
        y1 = np.array([2,6,8])
        y2 = np.array([6,2,3])
        output = pp.intersect(x, y1, y2)
        expected = (np.array([1.5]), np.array([4]), np.array([1]))
        for i in range(len(expected)):
            self.assertSequenceEqual(list(expected[i]), list(output[i]))

        #tests two crossings
        x = np.array([1,2,3,4,5,6])
        y1 = np.array([2,6,8,4,1])
        y2 = np.array([6,2,3,7,6])
        output = pp.intersect(x,y1,y2)
        expected = (np.array([1.5, 3.625]), np.array([4, 5.5]), np.array([1, 3]))
        for i in range(len(expected)):
            self.assertSequenceEqual(list(expected[i]), list(output[i]))

        #tests parallel lines
        x = np.array([1,2,3,4])
        y1 = np.array([3,5,7,9])
        y2 = np.array([5,7,9,11])
        output = pp.intersect(x,y1,y2)
        expected = (np.array([]), np.array([]), np.array([]))
        for i in range(len(expected)):
            self.assertSequenceEqual(list(expected[i]), list(output[i]))

        #tests equal and crossing
        x = np.array([-2,-1,0,1,2])
        y1 = np.array([2,1,0,-1,-2])
        y2 = np.array([-2,-1,0,1,2])
        output = pp.intersect(x,y1,y2)
        expected = (np.array([-0, -0]), np.array([0, 0]), np.array([2, 3]))
        for i in range(len(expected)):
            self.assertSequenceEqual(list(expected[i]), list(output[i]))

        #tests equal and not crossing
        x = np.array([0,1,2,3,4])
        y1 = np.array([4,4,4,4,4])
        y2 = np.array([3,4,3,0,-5])
        output = pp.intersect(x,y1,y2)
        expected = (np.array([1, 1]), np.array([4, 4]), np.array([1, 2]))
        for i in range(len(expected)):
            self.assertSequenceEqual(list(expected[i]), list(output[i]))
