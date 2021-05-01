"""Parser to obtain a dictionary of key-value pairs from an Onshape model's URL
and add those variables to an RST file.

Relies on the Onshape Documenter feature:
https://cad.onshape.com/documents/6b5c9b74e331c4d03a7c6b01/w/6f98333f14625dd1bdcac2f7/e/35b3d3018f18ec53eeecded7
"""

import json
import math
import os
from shutil import copyfile
from onshape_client.oas import BTFeatureScriptEvalCall2377
from onshape_client.onshape_url import OnshapeElement
from onshape_client import Client
from aguaclara.core.units import u

ureg =  u

msg_str = "message"
val_str = "value"
key_str = "key"

# create global roles using this: https://stackoverflow.com/questions/9698702/how-do-i-create-a-global-role-roles-in-sphinx
# If this grows too much, we'll need to add a global rst as described in the post above.
def parse_quantity(q, for_docs=True):
    """Parse an Onshape units definition

    Args:
        q: an Onshape units definition... for instance:
            {
              'typeTag': '',
              'unitToPower': [
                {
                  'key': 'METER',
                  'value': 1
                }
              ],
              'value': 0.0868175271040671
            }
        for_docs: True if parsing variables for AIDE documentation,
            False otherwise (e.g. validation)

    Returns:
        a string that can be converted to any other unit engine.
    """
    units_s = q[val_str]
    for unit in q["unitToPower"]:
        units_s = units_s * ureg(unit[key_str].lower()) ** unit[val_str]
        try:
            log = math.floor(math.log10(units_s.magnitude))
        except:
            log = 0
        if for_docs:
            if unit[key_str] == 'METER' and unit[val_str] == 1:
                if log >= 3:
                    units_s = units_s.to(ureg.kilometer)
                elif log >= -2 and log <= -1:
                    units_s = units_s.to(ureg.centimeter)
                elif log <= -3:
                    units_s = units_s.to(ureg.millimeter)
            elif unit[key_str] == 'METER' and unit[val_str] == 2:
                if log >= 6:
                    units_s = units_s.to(ureg.kilometer**2)
                elif log >= -4 and log <= -1:
                    units_s = units_s.to(ureg.centimeter**2)
                elif log <= -5:
                    units_s = units_s.to(ureg.millimeter**2)
            elif unit[key_str] == 'METER' and unit[val_str] == 3:
                log += 3
                if log >= 3:
                    units_s = units_s.to(ureg.kiloliter)
                elif log <= -1:
                    units_s = units_s.to(ureg.milliliter)
                else:
                    units_s = units_s.to(ureg.liter)
            return f'{round(units_s, 2):~}'
        else:
            return units_s

def is_fs_type(candidate, type_name):
    """Checks if the a JSON entry is of a specific FeatureScript type.

    Args:
        candidate: decoded JSON object to check the type of
        type_name: string of the FeatureScript Type to check for

    Returns:
        result: True if candidate is of type_name, False otherwise
    """
    result = False
    try:
        if isinstance(type_name, str):
            result = type_name == candidate["typeName"]
        elif isinstance(type_name, list):
            result = any(
                [type_name_one == candidate["typeName"] for type_name_one in type_name]
            )
    except Exception:
        result = False
    return result

def copy_to_docs(file_path, new_name=None, base="doc_files"):
    """First, searches recursively searches for the base path in parent folders.
    Then copies a file to the current working directory. The new file's path
    will be identical to the old file's path relative to the base path.

    Args:
        file_path: path to the file to be copied
        base: base path to use in creating relative file path of the copy
        new_name: new name for the file to avoid duplication.
            Default: None, use existing name

    Returns:
        none
    """
    dir = os.getcwd()
    while not os.path.exists(os.path.join(dir, base)):
        dir = os.path.dirname(dir)

    basepath = os.path.join(dir, base)
    new_path = new_name if new_name is not None else file_path
    try:
        copyfile(os.path.join(basepath, file_path), new_path)
    except IOError as io_err:
        os.makedirs(os.path.dirname(new_path))
        copyfile(os.path.join(basepath, file_path), new_path)

def parse_variables_from_list(unparsed, for_docs=True):
    """Helper function for parse_variables_from_map parses values from a list
    instead of a map.

    Args:
        unparsed: portion of deserialized JSON which has yet to be parsed
        for_docs: True if parsing variables for AIDE documentation,
            False otherwise (e.g. validation)

    Returns:
        measurement_list: list of parsed values
    """
    measurement_list = []

    for to_parse in unparsed:
        if is_fs_type(to_parse, "BTFSValueWithUnits"):
            measurement_list.append(parse_quantity(to_parse[msg_str], for_docs))
        elif is_fs_type(to_parse, ["BTFSValueNumber", "BTFSValueString"]):
            measurement_list.append(to_parse[msg_str][val_str])

    return measurement_list

def merge_index_sections(new_section, old_section):
    """Helper function for merge_indexes which loops through each section and
    combines them.

    Args:
        new_section: section which is being added to if line from old_section is absent
        old_section: section which is pulled from

    Returns:
        none
    """
    for line in old_section:
        if line in new_section:
            continue
        else:
            new_section.append(line)

    return new_section

def find_index_section_limits(filename, section_start=".. toctree::\n",
                              section_end="\n"):
    """Helper function for merge_indexes which loops through the
    file and marks the beginning and end of each section.

    Args:
        filename: path to file to be modified
        section_start: string which marks the start of each section
            Default: '.. toctree::\n'
        section_end: string which marks the end of each section
            Default: '\n'

    Returns:
        lines: list of strings of each line in the file
        section_limits: list of the form [[start1, end1], [start2, end2]]
            which marks the separation between sections
    """
    section_limits = []
    start = 0
    first_newline = True
    index_file = open(filename, "r+")
    lines = index_file.readlines()
    index_file.close()

    for i, line in enumerate(lines):
        if line == section_start:
            start = i
        if line == section_end and start != 0:
            if first_newline:
                first_newline = False
            else:
                end = i
                section_limits.append([start, end])
                start = end = 0
                first_newline = True

    return lines, section_limits

def merge_indexes(new_index, old_index):
    """Merges two indexes by comparing the two files, index.rst and new_index.rst
    section by section and adding pieces which exist in index.rst but are missing
    from new_index.rst . At the end, the one which was added to is maintained as
    index.rst and new_index.rst is deleted.

    Args:
        new_index: path to index file which is being merged from
        old_index: path to existing index file which is being merged into

    Returns:
        none
    True
    """
    old_lines, old_section_limits = find_index_section_limits(old_index)
    new_lines, new_section_limits = find_index_section_limits(new_index)

    for start, end in old_section_limits:
        included = False
        caption = old_lines[start+1]
        for new_start, new_end in new_section_limits:
            if new_lines[new_start+1] == caption:
                new_section = merge_index_sections(new_lines[new_start:new_end], old_lines[start:end])
                del new_lines[new_start:new_end]
                i = new_start
                for line in new_section:
                    new_lines.insert(i, line)
                    i += 1
                included = True
        if not included:
            i = new_end
            new_lines.insert(i, "\n")
            for line in old_lines[start:end]:
                i += 1
                new_lines.insert(i, line)

    old_index_file = open(old_index, "w+")
    old_index_file.write("".join(new_lines))
    old_index_file.close()

    os.remove(new_index)

def find_treatment_section_limits(filename, section_delimiter=".. _heading"):
    """Helper function for merge_treatment_processes which loops through the
    file and marks the beginning and end of each section.

    Args:
        filename: path to file to be modified
        section_delimiter: string which marks the separation between sections
            Default: '.. _heading'

    Returns:
        lines: list of strings of each line in the file
        section_limits: list of the form [[start1, end1], [start2, end2]]
            which marks the separation between sections
    """
    section_limits = []
    start = 0
    file = open(filename, "r+")
    lines = file.readlines()
    file.close()

    for i, line in enumerate(lines):
        if section_delimiter in line:
            end = i - 1
            section_limits.append([start, end])
            start = i

    section_limits.append([start,len(lines)])

    return lines, section_limits

def merge_treatment_processes(new_processes, old_processes):
    """Merges two treatment process descriptions by comparing the two files
    section by section and adding pieces which exist in new_processes but are missing
    from old_processes.

    Args:
        new_processes: path to treatment process file which is being merged from
        old_processes: path to existing treatment process file which is being merged into

    Returns:
        none
    """
    old_lines, old_section_limits = find_treatment_section_limits(old_processes)
    new_lines, new_section_limits = find_treatment_section_limits(new_processes)

    for start, end in new_section_limits:
        included = False
        heading = new_lines[start]
        for old_start, old_end in old_section_limits:
            if old_lines[old_start] == heading:
                included = True
        if not included:
            i = old_end
            old_lines.insert(i, "\n")
            for line in new_lines[start:end]:
                i += 1
                old_lines.insert(i, line)

    old_file = open(old_processes, "w+")
    old_file.write("".join(old_lines))
    old_file.close()

def parse_variables_from_map(unparsed, default_key="", for_docs=True):
    """Helper function for parse_attributes which loops through an unparsed map
    that matched one of the desired fields

    Args:
        unparsed: portion of deserialized JSON which has yet to be parsed
        default_key: key for the field. Used to detect special entries like index
        for_docs: True if parsing variables for AIDE documentation,
            False otherwise (e.g. validation)

    Returns:
        parsed_variables: dictionary of parsed variables
        templates: list of templates to move from doc_files and render in the
            design specs.
        processes: list of unit processes in the given Onshape model
    """
    parsed_variables = {}
    value = None
    templates = []
    processes = []

    if default_key == "template":
        if for_docs:
            copy_to_docs(unparsed)
        templates.append(unparsed)
        return parsed_variables, templates, processes
    elif default_key == "index":
        if unparsed != "" and unparsed is not None and for_docs:
                if os.path.exists('index.rst'):
                    copy_to_docs(unparsed, 'new_index.rst')
                    merge_indexes('new_index.rst', 'index.rst')
                else:
                    copy_to_docs(unparsed, 'index.rst')
        return parsed_variables, templates, processes
    elif default_key == "process":
        processes.append(unparsed)
        if unparsed != "" and unparsed is not None and for_docs:
            file = "Introduction/Treatment_Process.rst"
            file_path = "../../../doc_files/Introduction/Treatment_Process_" + unparsed + ".rst"
            if os.path.exists(file):
                merge_treatment_processes(file_path, file)
            else:
                try:
                    copyfile(file_path, file)
                except IOError as io_err:
                    os.makedirs(os.path.dirname(file))
                    copyfile(file_path, file)
        return parsed_variables, templates, processes

    if isinstance(unparsed, list):
        for to_parse in unparsed:
            if is_fs_type(to_parse, "BTFSValueMapEntry"):
                key = to_parse[msg_str][key_str][msg_str][val_str]
                candidate_message = to_parse[msg_str][val_str]
                if is_fs_type(candidate_message, "BTFSValueMap"):
                    value, template = parse_variables_from_map(candidate_message[msg_str][val_str])
                    templates.extend(template)
                elif is_fs_type(candidate_message,  "BTFSValueArray"):
                    value = parse_variables_from_list(candidate_message[msg_str][val_str],
                                                      for_docs)
                elif is_fs_type(candidate_message, "BTFSValueWithUnits"):
                    value = parse_quantity(candidate_message[msg_str], for_docs)
                elif is_fs_type(candidate_message, ["BTFSValueNumber", "BTFSValueString"]):
                    value = candidate_message[msg_str][val_str]
                parsed_variables[key] = value
    else:
        parsed_variables[default_key] = unparsed

    return parsed_variables, templates, processes

def parse_attributes(attributes, fields, for_docs=True, type_tag="Documenter"):
    """Helper function for get_parsed_measurements which loops through the
    atributes, parsing only the specified fields.

    Args:
        attributes: deserialized JSON object returned by Onshape link
        fields: fields which we are interested in parsing, e.g. 'variables' or 'index'
        for_docs: True if parsing variables for AIDE documentation,
            False otherwise (e.g. validation)
        type_tag: type from Onshape of the configuration we are parsing for
            Default: 'Documenter'

    Returns:
        measurements: dictionary of parsed variables
        templates: list of templates to move from doc_files and render in the
            design specs.
        processes: list of unit processes in the given Onshape model
    """
    measurements = {}
    templates = []
    processes = []

    for attr in attributes:
        if is_fs_type(attr, "BTFSValueMap"):
            if attr[msg_str]["typeTag"] == type_tag:
                for attr2 in attr[msg_str][val_str]:
                    docs = attr2[msg_str][val_str][msg_str][val_str]
                    for doc in docs:
                        for unparsed in doc[msg_str][val_str]:
                            if is_fs_type(unparsed, "BTFSValueMapEntry"):
                                key = unparsed[msg_str][key_str][msg_str][val_str]
                                for field in fields:
                                    if key == field:
                                        new_measure, new_templates, new_processes = parse_variables_from_map(
                                            unparsed[msg_str][val_str][msg_str][val_str],
                                            key,
                                            for_docs
                                        )
                                        measurements.update(new_measure)
                                        templates.extend(new_templates)
                                        processes.extend(new_processes)

    for i in range(len(templates)):
        new_template = './' + os.path.basename(os.path.dirname(templates[i])) + \
                       '/' + os.path.basename(templates[i])
        templates[i] = new_template

    return measurements, templates, processes

def get_parsed_measurements(link,
                            fields=["variables", "template", "index", "process"],
                            for_docs=True):
    """Parses the output of the Onshape Documenter feature found in the Onshape
    document at the given url.

    Args:
        link: URL of Onshape document
        fields: names of fields to search for in the Onshape JSON object
        for_docs: True if parsing variables for AIDE documentation,
            False otherwise (e.g. validation)

    Returns:
        measurements: dictionary of parsed variables
        templates: list of templates to move from doc_files and render in the
            design specs.
        processes: list of unit processes in the given Onshape model
    """
    script = r"""
        function (context is Context, queries is map)
        {
            return getAttributes(context, {
                "entities" : qEverything(),
            });
        }
        """

    client = Client(
        configuration = {
            "base_url": "https://cad.onshape.com",
            "access_key": "ekAHCj04TtODlvlI9yWj2bjB",
            "secret_key": "sS11vEOD5CavkLVcZshLBgfBlB5aBvnpz6v3oEvC0bN0zxhW"
        }
    )

    element = OnshapeElement(link)

    script_call = BTFeatureScriptEvalCall2377(script=script)
    response = client.part_studios_api.eval_feature_script(
        element.did,
        element.wvm,
        element.wvmid,
        element.eid,
        bt_feature_script_eval_call_2377=script_call,
        _preload_content=False,
    )

    attributes = json.loads(response.data.decode("utf-8"))["result"][msg_str][val_str]

    measurements, templates, processes = parse_attributes(attributes, fields, for_docs)

    return measurements, templates, processes

# from https://stackoverflow.com/questions/5914627/prepend-line-to-beginning-of-a-file
def line_prepender(filename, line):
    """Prepends a file with the given line.

    Args:
        filename: path to file to be modified
        line: string of text to prepend to the file

    Returns:
        none
    """
    with open(filename, 'r+') as f:
        content = f.read()
        f.seek(0, 0)
        f.write(line.rstrip('\r\n') + '\n' + content)

def make_replace_list(parsed_dict, filename, var_attachment=''):
    """Adds the dictionary of variables which have been parsed to the top of the
    given file.

    Args:
        parsed_dict: dictionary of variables parsed from Onshape document
        filename: path to file to be modified
        var_attachment: string to prepend to all variables, e.g. "LFOM"
            Default: ''

    Returns:
        none
    """
    prefix = '.. |'
    suffix = '| replace:: '

    for var in parsed_dict:
        if type(parsed_dict[var]) == dict:
            make_replace_list(parsed_dict[var], filename, var_attachment + var + "_")
        else:
            line = prefix + var_attachment + str(var) + suffix + str(parsed_dict[var])
            line_prepender(filename, line)
