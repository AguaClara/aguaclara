"""
Tests for the research package's ProCoDA parsing functions
"""

import unittest
from aguaclara.research.procoda_parser import *

class TestProCoDAParser(unittest.TestCase):

    def test_get_data_by_time(self):
        '''
        Extract column(s) of data between given starting and ending days and times
        '''
        path = os.path.join(os.path.dirname(__file__), '.', 'data')

        data_day1 = pd.read_csv(path + '/datalog 6-14-2018.xls', delimiter='\t')
        data_day1 = np.round([pd.to_numeric(data_day1.iloc[:, 0]), pd.to_numeric(data_day1.iloc[:, 4])], 5)
        data_day1 = [data_day1[0].tolist(), data_day1[1].tolist()]

        data_day2 = pd.read_csv(path + '/datalog 6-15-2018.xls', delimiter='\t')
        data_day2 = np.round([pd.to_numeric(data_day2.iloc[:, 0]), pd.to_numeric(data_day2.iloc[:, 4])], 5)
        data_day2 = [data_day2[0].tolist(), data_day2[1].tolist()]
        data_day2[0][0] = 0  # to remove scientific notation "e-"

        # SINGLE COLUMN, ONE DAY
        output = get_data_by_time(path=path, columns=0, dates="6-14-2018", start_time="12:20", end_time="13:00")
        self.assertSequenceEqual(np.round(output, 5).tolist(), data_day1[0][1041:1282])

        # SINGLE COLUMN, TWO DAYS
        output = get_data_by_time(path=path, columns=0, dates=["6-14-2018", "6-15-2018"],
                                  start_time="12:20", end_time="10:50")
        time_column = data_day1[0][1041:] + np.round(np.array(data_day2[0][:3901])+1, 5).tolist()
        self.assertSequenceEqual(np.round(output, 5).tolist(), time_column)

        # MULTI COLUMN, ONE DAY
        output = get_data_by_time(path=path, columns=[0, 4], dates=["6-14-2018"], start_time="12:20",
                                  end_time="13:00")
        self.assertSequenceEqual(np.round(output[0], 5).tolist(), data_day1[0][1041:1282])
        self.assertSequenceEqual(np.round(output[1], 5).tolist(), data_day1[1][1041:1282])

        # MULTI COLUMN, TWO DAYS
        output = get_data_by_time(path=path, columns=[0, 4], dates=["6-14-2018", "6-15-2018"],
                                  start_time="12:20", end_time="10:50")
        time_column = data_day1[0][1041:] + np.round(np.array(data_day2[0][:3901])+1, 5).tolist()
        self.assertSequenceEqual(np.round(output[0], 5).tolist(), time_column)
        self.assertSequenceEqual(np.round(output[1], 5).tolist(), data_day1[1][1041:]+data_day2[1][:3901])

    def test_remove_notes(self):
        '''
        Return a DataFrame without any lines that originally contained text
        '''
        path = os.path.join(os.path.dirname(__file__), '.', 'data')

        output = remove_notes(pd.read_csv(path + '/example datalog.xls', delimiter='\t'))

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


    def test_get_data_by_state(self):
        '''
        Extract the time column and a data column for each iteration of a state
        '''
        path = os.path.join(os.path.dirname(__file__), '.', 'data')

        output = get_data_by_state(path, dates=["6-19-2013"], state=1, column=1)  # , "6-20-2013"

        datafile = pd.read_csv(path + "/datalog 6-19-2013.xls", delimiter='\t')
        time_and_data1 = np.array([pd.to_numeric(datafile.iloc[:, 0]),
                                   np.round(pd.to_numeric(datafile.iloc[:, 1]), 5)])
        start_time = time_and_data1[0, 0]

        answer = [time_and_data1[:, 98:175], time_and_data1[:, 220:485], time_and_data1[:, 3039:3304],
                  time_and_data1[:, 5858:6123], time_and_data1[:, 8677:8942], time_and_data1[:, 11496:11761],
                  time_and_data1[:, 14315:14580]]

        for i in range(len(output)):
            output_i = np.round(np.array(output[i]).astype(np.double), 5)
            self.assertSequenceEqual([j[0] for j in output_i], [round(j-start_time, 5) for j in answer[i][0]])
            self.assertSequenceEqual([j[1] for j in output_i], [j for j in answer[i][1]])

    def test_column_of_time(self):
        '''''
        Extract the time column from a data file.
        '''''
        path = os.path.join(os.path.dirname(__file__), '.', 'data', 'example datalog.xls')
        answer = column_of_time(path, 50, -1)
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
         6.77069570e-03,   6.82855640e-03])*u.day, 5).tolist()
        )


    def test_column_of_data(self):
        '''''
        Extract other columns of data and append units.
        '''''
        path = os.path.join(os.path.dirname(__file__), '.', 'data', 'example datalog.xls')
        answer = column_of_data(path, 50, 1, -1, 'mg/L')
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
         1.97646523,   1.96455812,   1.95887971])*u('mg/L'), 5).tolist()
        )

    def test_notes(self):
        '''''
        Test function that extracts meta information from data file.
        '''''
        path = os.path.join(os.path.dirname(__file__), '.', 'data', 'example datalog.xls')
        answer = notes(path)['Day fraction since midnight on ']
        x = pd.DataFrame(index=[1, 29, 35],
                         columns=['Day fraction since midnight on ', 'red dye (mg/L)', 'Run Pump ()', 'Pump ()'])
        x.iloc[0][0] = 'Start'
        x.iloc[1][0] = 'Start'
        x.iloc[2][0] = '30 mg/L'
        self.assertSequenceEqual(
        answer.tolist(),
        x['Day fraction since midnight on '].tolist())

    def test_read_state(self):
        path = os.path.join(os.path.dirname(__file__), '.', 'data', '')
        time, data = read_state(["6-19-2013", "6-20-2013"], 1, 28, "mL/s", path)
        time = np.round(time, 5)
        self.assertSequenceEqual(
        time.tolist()[1000:1100],
        np.round(
        [0.10189837999999996, 0.10190995999999997, 0.10192152999999993,
         0.10193310999999994, 0.10194468000000001, 0.10195624999999997,
         0.10196782999999998, 0.10197939999999994, 0.10199097999999995,
         0.10200254999999991, 0.10201412999999993, 0.1020257,
         0.10203726999999996, 0.10204884999999997, 0.10206041999999993,
         0.10207199999999994, 0.10208357000000001, 0.10209513999999997,
         0.10210671999999998, 0.10211828999999994, 0.10212986999999996,
         0.10214143999999992, 0.10215300999999999,
         0.10216459, 0.10217615999999996, 0.10218773999999997,
         0.10219930999999993, 0.10221088, 0.1022224599999999,
         0.10223402999999998, 0.10224560999999999, 0.10225717999999995,
         0.10226874999999991, 0.10228032999999992, 0.10229189999999999,
         0.10230348, 0.10231504999999996, 0.10232662999999997,
         0.10233819999999993, 0.10234977, 0.1023613499999999,
         0.10237291999999998, 0.10238449999999999, 0.10239606999999995,
         0.10240763999999991, 0.10241921999999992, 0.10243079,
         0.10244237, 0.10245393999999997, 0.10246550999999993,
         0.10247708999999994, 0.10248866000000001, 0.10250023999999991,
         0.10251180999999998, 0.10252337999999994, 0.10253495999999995,
         0.10254652999999991, 0.10255810999999992, 0.10256968,
         0.10258124999999996, 0.10259282999999997, 0.10260439999999993,
         0.10261597999999994, 0.10262755000000001, 0.10263912999999991,
         0.10265069999999998, 0.10266226999999994, 0.10267384999999996,
         0.10268541999999992, 0.10269699999999993, 0.10270857,
         0.10272013999999996, 0.10273171999999997, 0.10274328999999993,
         0.10275486999999994, 0.1027664399999999, 0.10277800999999998,
         0.10278958999999999, 0.10280115999999995, 0.10281273999999996,
         0.10282430999999992, 0.10283587999999999, 0.10284746,
         0.10285902999999996, 0.10287060999999997, 0.10288229999999998,
         0.10289375, 0.1029054399999999, 0.10291701999999991,
         0.10292858999999999, 0.10294017, 0.10295162999999996,
         0.10296330999999992, 0.10297488999999993, 0.10298646,
         0.1029980399999999, 0.10300960999999997, 0.10302106999999994,
         0.10303275999999995, 0.10304421999999991]*u.day, 5).tolist()
        )

        self.assertSequenceEqual(
        data.tolist()[1000:1100],
        [5.4209375*u.mL/u.s for number in range(100)]
        )

    def test_average_state(self):
        path = os.path.join(os.path.dirname(__file__), '.', 'data', '')
        avgs = average_state(["6-19-2013", "6-20-2013"], 1, 28, "mL/s", path)
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

        avgs = perform_function_on_state(avg_with_units, ["6-19-2013", "6-20-2013"], 1, 28, "mL/s", path)
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

        ids, answer = read_state_with_metafile(avg_with_units, 1, 28, path, [], ".xls", "mg/L")

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

        output = write_calculations_to_csv(avg_with_units, 1, 28, path,
                                           ["Average Conc (mg/L)"], out_path)

        self.assertSequenceEqual(["1", "2"], output['ID'].tolist())
        self.assertSequenceEqual(
        [5.445427082723495, 5.459751965314751],
        output['Average Conc (mg/L)'].tolist())
