import unittest
import json
import os
from aguaclara.core.units import u
from aguaclara.core import onshape_parser as parse

os.chdir(os.path.dirname(__file__))


class OnshapeParserTest(unittest.TestCase):
    def test_parse_quanity(self):
        d0 = {'value': 0.1414213562373095,
              'unitToPower': [{'value': 1, 'key': 'METER'}], 'typeTag': ''}
        d1 = {'value': 0.1414213562373095,
              'unitToPower': [{'value': 3, 'key': 'MILLIMETER'}], 'typeTag': ''}
        d2 = {'value': 0.001414213562373095,
              'unitToPower': [{'value': 1, 'key': 'METER'}], 'typeTag': ''}
        d3 = {'value': 1414.213562373095,
              'unitToPower': [{'value': 1, 'key': 'METER'}], 'typeTag': ''}
        d4 = {'value': 1414213.562373095,
              'unitToPower': [{'value': 2, 'key': 'METER'}], 'typeTag': ''}
        d5 = {'value': 0.00043,
              'unitToPower': [{'value': 2, 'key': 'METER'}], 'typeTag': ''}
        d6 = {'value': 0.00000043,
              'unitToPower': [{'value': 2, 'key': 'METER'}], 'typeTag': ''}
        d7 = {'value': 1414213562.373095,
              'unitToPower': [{'value': 3, 'key': 'METER'}], 'typeTag': ''}
        d8 = {'value': 0.00000043,
              'unitToPower': [{'value': 3, 'key': 'METER'}], 'typeTag': ''}
        d9 = {'value': 0.0043,
              'unitToPower': [{'value': 3, 'key': 'METER'}], 'typeTag': ''}
        d10 = {'value': 0.1414213562373095,
              'unitToPower': [{'value': -1, 'key': 'METER'}], 'typeTag': ''}
        d11 = {'value': -0.0043,
              'unitToPower': [{'value': 1, 'key': 'METER'}], 'typeTag': ''}

        self.assertEqual(parse.parse_quantity(d0), '14.14 cm')
        self.assertEqual(parse.parse_quantity(d0, False),
                         0.1414213562373095 * u.m)
        self.assertEqual(parse.parse_quantity(d1), '0.14 mm ** 3')
        self.assertEqual(parse.parse_quantity(d2), '1.41 mm')
        self.assertEqual(parse.parse_quantity(d3), '1.41 km')
        self.assertEqual(parse.parse_quantity(d4), '1.41 km ** 2')
        self.assertEqual(parse.parse_quantity(d5), '4.3 cm ** 2')
        self.assertEqual(parse.parse_quantity(d6), '0.43 mm ** 2')
        self.assertEqual(parse.parse_quantity(d7), '1414213562.37 kl')
        self.assertEqual(parse.parse_quantity(d8), '0.43 ml')
        self.assertEqual(parse.parse_quantity(d9), '4.3 l')
        self.assertEqual(parse.parse_quantity(d10), '0.14 / m')
        self.assertEqual(parse.parse_quantity(d11), '-0.0 m')

    def test_is_fs_type(self):
        test_json = json.loads('{"type": 2077, "typeName": "BTFSValueMapEntry", "message": {}}')

        self.assertTrue(parse.is_fs_type(test_json, "BTFSValueMapEntry"))
        self.assertFalse(parse.is_fs_type(test_json, "BTFSValueNumber"))
        self.assertFalse(parse.is_fs_type(None, "BTFSValueNumber"))

    def test_merge_index_sections(self):
        new_section = ['test_line', 'test_line2']
        old_section = ['test_line', 'test_line3']
        result = parse.merge_index_sections(new_section, old_section)

        self.assertEqual(result, ['test_line', 'test_line2', 'test_line3'])

    def test_find_index_section_limits(self):
        index0 = '../rst_files/index_lfom.rst'
        _, limits0 = parse.find_index_section_limits(index0)
        index1 = '../rst_files/index_lfom_ET.rst'
        _, limits1 = parse.find_index_section_limits(index1)

        self.assertEqual(limits0, [[18, 26], [27, 32]])
        self.assertEqual(limits1, [[18, 26], [27, 33]])

    def test_merge_indexes(self):
        old_index = '../rst_files/index_lfom.rst'
        new_index = '../rst_files/new_index_ET.rst'
        parse.merge_indexes(new_index, old_index)
        index_file = open(old_index, "r+")
        lines = index_file.readlines()
        test_file = open('../rst_files/index_lfom_ET.rst')
        test_lines = test_file.readlines()

        self.assertEqual(test_lines, lines)

        old_index = '../rst_files/index_ET.rst'
        new_index = '../rst_files/index_floc.rst'
        parse.merge_indexes(new_index, old_index)
        index_file = open(old_index, "r+")
        lines = index_file.readlines()
        test_file = open('../rst_files/index_ET_floc.rst')
        test_lines = test_file.readlines()

    def test_find_treatment_section_limits(self):
        process0 = '../rst_files/Treatment_Process_ET.rst'
        _, limits0 = parse.find_treatment_section_limits(process0)
        process1 = '../rst_files/Treatment_Process_ET_Floc.rst'
        lines, limits1 = parse.find_treatment_section_limits(process1)

        self.assertEqual(limits0, [[0, 14], [15, 20]])
        self.assertEqual(limits1, [[0, 14], [15, 20], [21, 26]])

    def test_merge_treatment_processes(self):
        old_processes = '../rst_files/Treatment_Process_ET.rst'
        new_processes = '../rst_files/Treatment_Process_Floc.rst'
        parse.merge_treatment_processes(new_processes, old_processes)
        file = open(old_processes, "r+")
        lines = file.readlines()
        test_file = open('../rst_files/Treatment_Process_ET_Floc.rst')
        test_lines = test_file.readlines()

        self.assertEqual(test_lines, lines)

    def test_get_parsed_measurements(self):
        link = 'https://cad.onshape.com/documents/c3a8ce032e33ebe875b9aab4/v/dc76b3f674d3d5d4f6237f35/e/d75b2f7a41dde39791b154e8'
        measurements, templates = parse.get_parsed_measurements(
            link,
            fields=['variables', 'template'],
            for_docs=False
        )

        self.assertEqual(templates, ['./Entrance_Tank/LFOM.rst'])
        self.assertEqual(measurements['N.LfomOrifices'],
                         [17.0, 4.0, 6.0, 3.0, 4.0, 3.0, 3.0, 3.0, 3.0, 2.0, 3.0, 1.0])
        self.assertEqual(measurements['HL.Lfom'], 0.2 * u.m)
        self.assertEqual(
            measurements['H.LfomOrifices'],
            [0.0079375 * u.m, 0.02467613636363637 * u.m,
             0.04141477272727274 * u.m, 0.0581534090909091 * u.m,
             0.07489204545454548 * u.m, 0.09163068181818185 * u.m,
             0.1083693181818182 * u.m, 0.1251079545454546 * u.m,
             0.14184659090909096 * u.m, 0.15858522727272734 * u.m,
             0.1753238636363637 * u.m, 0.19206250000000008 * u.m]
        )
        self.assertEqual(measurements['D.LfomOrifices'], 0.015875 * u.m)
        self.assertEqual(measurements['B.LfomRows'], 0.016666666666666666 * u.m)

    def test_make_replace_list(self):
        var_dict = {'test': '3.0 cm'}
        file_path = "../rst_files/test_prepend.rst"
        parse.make_replace_list(var_dict, file_path)
        file = open(file_path, "r+")
        lines = file.readlines()
        test_file = open('../rst_files/test_prepend_result.rst')
        test_lines = test_file.readlines()

        self.assertEqual(test_lines, lines)

    def test_copy_to_docs(self):
        file_path = "Mix/Mix_Design_Data.rst"
        parse.copy_to_docs(file_path, base="rst_files")

        assert os.path.exists(file_path)

if __name__ == '__main__':
    unittest.main()
