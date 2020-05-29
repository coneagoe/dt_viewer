# dt_viewer

It's difficult to locate a node in a bunch of _dts_, especially it includes a lot of _dtsi_ and _dtsi_
includes other _dtsi_.

The script view.py is designed to help you to list possible nodes.

Another user case is to compare two _dts_, you may be interfered with the order of nodes even
they're same.

You can use compare.py to make it easier.

## notice

These scripts are just re search, they don't care syntax validation. And they are not aware of some
directives (e.g. /delete-property/ and /delete-node/).

