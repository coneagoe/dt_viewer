# -*- coding: utf-8 -*-
import os
import logging
import re


prefix = '.'
nodes = []


def parse(node, dts_name):
    if prefix != '.':
        dts_name = os.path.join(prefix, dts_name)

    if not os.path.exists(dts_name):
        logging.error("dts %s does not exist", dts_name)
        exit()

    with open(dts_name) as fd:
        for i, line in enumerate(fd):
            node = do_parse(node, i + 1, line, dts_name)


def do_parse(node, line_number, line, dts_name):
    if re.search("^\s*/include/", line):
        parse_include(node, line)
    elif re.search("^.+{", line):
        node = parse_left_bracket(node, line, dts_name, line_number)
    elif re.search("};", line):
        node = parse_right_bracket(node, line, line_number)
    else:
        node.add_property(line)
    return node


def parse_include(node, line):
    dts_name = line.split('"')[1]
    dts_name_tmp = os.path.join(prefix, dts_name)
    if not os.path.exists(dts_name_tmp):
        dts_name_tmp = os.path.join(prefix, 'fsl', dts_name)
        if not os.path.exists(dts_name_tmp):
            logging.error("dts %s does not exist", dts_name)
            exit()
        else:
            dts_name = dts_name_tmp

    parse(node, dts_name)


def parse_left_bracket(node, line, dts_name, line_number):
    if re.match('^\s*/\s*{', line):
        if node.is_root():
            nodes.append(node)
            return node

    m = re.match('^\s*([0-9a-zA-Z,._+/:\s\-@&]+)\s*{', line)
    if m is None:
        logging.error('Unexpected node name: %s', line)
        exit(-1)

    line = m.group(1)
    nodes.append(node)
    if line == '/':
        node.name = '/'
        node.unit_name = '/'
        node.locations.append("%s:%d" % (dts_name, line_number))
        return node

    node = node.add_child(line, dts_name, line_number)
    return node


def parse_right_bracket(node, line, line_number):
    node = nodes.pop()
    return node

