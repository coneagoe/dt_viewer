import sys
import os
import parse as ps
import node as nd

dts_A = ''
dts_B = ''
prefix_A = '.'
prefix_B = '.'
root_A = nd.Node.init()
root_B = nd.Node.init()


def usage():
    print("python %s <dts_A> <dts_B>" % sys.argv[0])
    print("dts must be decompiled by dtc, otherwise it may fail")


def dump_node_name(node: nd.Node, fd, depth):
    if node.is_root():
        fd.write(node.syntax_head)
        fd.write('\n\n')

    indent = '\t' * depth
    fd.write(indent)
    fd.write(node.unit_name)
    fd.write(' {\n')


def dump_properties(node: nd.Node, fd, depth):
    if len(node.properties) > 0:
        indent = '\t' * (depth + 1)
        for i in node.properties:
            fd.write(indent)
            fd.write(i)
            fd.write('\n')


def dump_tail(fd, depth):
    indent = '\t' * depth
    fd.write(indent)
    fd.write('};\n')


def dump_tree(node: nd.Node, fd, depth):
    fd.write('\n')
    dump_node_name(node, fd, depth)
    dump_properties(node, fd, depth)

    if len(node.children) > 0:
        for child in node.children.values():
            dump_tree(child, fd, depth + 1)

    dump_tail(fd, depth)


def do_compare(node_a: nd.Node, node_b: nd.Node, fd_a, fd_b, depth):
    if node_a.unit_name == node_b.unit_name:
        dump_node_name(node_a, fd_a, depth)
        dump_node_name(node_b, fd_b, depth)
        dump_properties(node_a, fd_a, depth)
        dump_properties(node_b, fd_b, depth)

    first_child = True
    for a_child_name, a_child in node_a.children.items():
        if a_child_name in node_b.children.keys():
            # common child
            if first_child is True:
                first_child = False
            else:
                fd_a.write('\n')
                fd_b.write('\n')

            b_child = node_b.children[a_child_name]
            do_compare(a_child, b_child, fd_a, fd_b, depth + 1)
        else:
            # a only
            dump_tree(a_child, fd_a, depth + 1)

    for b_child_name, b_child in node_b.children.items():
        if b_child_name not in node_a.children.keys():
            # b only
            dump_tree(b_child, fd_b, depth + 1)

    dump_tail(fd_a, depth)
    dump_tail(fd_b, depth)


def compare(root_a: nd.Node, root_b: nd.Node):
    with open(dts_A + '_a', 'w') as fd_a:
        with open(dts_B + '_b', 'w') as fd_b:
            do_compare(root_a, root_b, fd_a, fd_b, 0)


if __name__ == '__main__':
    if len(sys.argv) != 3:
        usage()
        exit()

    dts_A = os.path.basename(sys.argv[1])
    prefix_A = os.path.dirname(sys.argv[1])
    dts_B = os.path.basename(sys.argv[2])
    prefix_B = os.path.dirname(sys.argv[2])

    ps.prefix = prefix_A
    ps.parse(root_A, dts_A)

    ps.prefix = prefix_B
    ps.parse(root_B, dts_B)

    compare(root_A, root_B)