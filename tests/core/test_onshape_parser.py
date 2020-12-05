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

        self.assertEqual(parse.parse_quantity(d0), '14.14 cm')
        self.assertEqual(parse.parse_quantity(d1), '0.14 mm ** 3')
        self.assertEqual(parse.parse_quantity(d0, False),
                         0.1414213562373095 * u.m)

    def test_is_fs_type(self):
        test_json = json.loads('{"type": 2077, "typeName": "BTFSValueMapEntry", "message": {}}')

        self.assertTrue(parse.is_fs_type(test_json, "BTFSValueMapEntry"))
        self.assertFalse(parse.is_fs_type(test_json, "BTFSValueNumber"))

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
    #
    # def test_get_parsed_measurements(self):
    #     link = 'https://cad.onshape.com/documents/c3a8ce032e33ebe875b9aab4/v/dc76b3f674d3d5d4f6237f35/e/d75b2f7a41dde39791b154e8'
    #     measurements, templates = parse.get_parsed_measurements(link)
    #
    #     self.assertEqual(templates, ['./Entrance_Tank/LFOM.rst'])
    #     self.assertEqual(measurements['N.LfomOrifices'],
    #                      [17.0, 4.0, 6.0, 3.0, 4.0, 3.0, 3.0, 3.0, 3.0, 2.0, 3.0, 1.0])
    #     self.assertEqual(measurements['HL.Lfom'], '20.0 cm')
    #     self.assertEqual(
    #         measurements['H.LfomOrifices'],
    #         ['7.94 mm', '2.47 cm', '4.14 cm', '5.82 cm', '7.49 cm', '9.16 cm',
    #         '10.84 cm', '12.51 cm', '14.18 cm', '15.86 cm', '17.53 cm', '19.21 cm']
    #     )
    #     self.assertEqual(measurements['D.LfomOrifices'], '1.59 cm')
    #     self.assertEqual(measurements['B.LfomRows'], '1.67 cm')

    def test_make_replace_list(self):
        var_dict = {'test': '3.0 cm'}
        file_path = "../rst_files/test_prepend.rst"
        parse.make_replace_list(var_dict, file_path)
        file = open(file_path, "r+")
        lines = file.readlines()
        test_file = open('../rst_files/test_prepend_result.rst')
        test_lines = test_file.readlines()

        self.assertEqual(test_lines, lines)

if __name__ == '__main__':
    unittest.main()
