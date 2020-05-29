# -*- coding: utf-8 -*-
import os
import logging
from cmd import Cmd
import re
import parse
import node as nd
import sys


root = nd.Node.init()


class Cli(Cmd):
    def do_pp(self, arg):
        '''
        print node path
        '''
        for node in nd.resolved_nodes.values():
            if int(arg) == id(node):
                while True:
                    print(node.unit_name)
                    if node.parent is None:
                        break
                    node = node.parent

    def do_ln(self, arg):
        '''
        list possible nodes
        '''
        snippet = arg
        for unit_name, node in nd.resolved_nodes.items():
            if re.search(snippet, unit_name):
                print()
                print(node)
                print()

    def do_info(self, arg):
        '''
        show dts info
        '''
        print("dts: ", sys.argv[1])
        if len(sys.argv) == 3:
            print("prefix: ", sys.argv[2])

    def do_exit(self, arg):
        exit()


def usage():
    print("python %s <dts> [prefix]" % sys.argv[0])
    print("prefix: default is '.'")


if __name__ == '__main__':
    if len(sys.argv) != 2 and len(sys.argv) != 3:
        usage()
        exit()

    if len(sys.argv) == 3:
        parse.prefix = sys.argv[2]

    parse.parse(root, sys.argv[1])
    nd.Node.resolve_node()
    Cli().cmdloop()
