# -*- coding: utf-8 -*-
import re
import logging


resolved_nodes = dict()
unresolved_nodes = dict()


def has_label(string):
    if re.search(':', string):
        return True
    return False


def has_address(string):
    if re.search('@', string):
        return True
    return False


def is_overlay_node(string):
    if re.search('^\s*&', string):
        return True
    return False


def get_original_node(label):
    for unit_name, node in resolved_nodes.items():
        if re.search(label, unit_name):
            return node
    return None


def get_overlay_node(label):
    for node in unresolved_nodes.values():
        if label == node.label:
            return node
    return None


class Node(object):
    def __init__(self, string, file_name, line_number, parent):
        self.parent = parent
        self.children = dict()
        self.unit_name = string.strip()
        self.label = ''
        self.name = ''
        self.unit_address = ''
        self._extract(string)
        self.locations = []
        self.locations.append("%s:%d" % (file_name, line_number))
        self.properties = []
        if self.is_root():
            self.syntax_head = '/dts-v1/;'

    def is_root(self):
        return self.unit_name == '/'

    def __repr__(self):
        return "id: %s\nunit name: %s\nlabel: %s\nname: %s\nunit address: %s\nlocations: %s" \
               % (id(self), self.unit_name, self.label,
                  self.name, self.unit_address, self.locations)

    @classmethod
    def init(cls):
        root = Node('/', '', 0, None)
        resolved_nodes['/'] = root
        return root

    @classmethod
    def uninit(cls):
        resolved_nodes.clear()

    def add_child(self, string, file_name, line_number):
        child = Node(string, file_name, line_number, self)
        if is_overlay_node(string):
            child.parent = None
            node = get_original_node(child.label)
            if node is None:
                node = get_overlay_node(child.label)

            if node is None:
                unresolved_nodes[child.unit_name] = child
                return child
            else:
                node._merge_node(child)
                return node
        else:
            self.children[child.unit_name] = child
            resolved_nodes[child.unit_name] = child
            return child

    def add_property(self, line):
        if re.search("dts-v", line):
            if self.is_root():
                self.syntax_head = line.strip()
                return

        if re.search("^\s+$", line):
            return
        self.properties.append(line.strip())

    def _merge_node(self, node):
        self.locations += node.locations
        return

        # TODO merge subtree
        if self.label == node.label or self.name == node.name:
            pass
        else:
            logging.error("Not same node (%s, %s), cannot merge", self, node)
            exit(-1)

        self.locations += node.locations
        for child0 in self.children.values():
            for child1 in node.children.values():
                if child0.label == child1.label:
                    child0._merge_node(child1)

    def _extract(self, string):
        if has_label(string) and has_address(string):
            label, name, address = re.split(':|@', string)
            self.label = label.strip()
            self.name = name.strip()
            self.unit_address = address.strip()
        elif has_label(string) and not has_address(string):
            label, name = string.split(':')
            self.label = label.strip()
            self.name = name.strip()
        elif not has_label(string) and has_address(string):
            name, address = string.split('@')
            self.name = name.strip()
            self.unit_address = name.strip()
        else:
            if is_overlay_node(string):
                label = string.strip()
                self.label = label.strip('&')
            else:
                self.name = string.strip()

    @classmethod
    def resolve_node(cls):
        for unit_name, unresolved_node in unresolved_nodes.items():
            node = resolved_nodes[unit_name]
            if node is Node:
                logging.error("Cannot find node: %s", unit_name)
                exit(-1)

            node._merge_node(unresolved_node)
        unresolved_nodes.clear()
