__author__ = 'wan'

from xml.etree import ElementTree as ET


def parser(name):
    p = ET.parse('test.xml')
    data = []
    root = p.getroot()
    prefix = '{%s}' % (root.tag.split('}')[0].split('{')[1])
    _rec(root, data, name, prefix)
    return data


def _rec(children, data, name, prefix):
    if children is None or len(children) <= 0:
        return
    for child in children:
        if child is None:
            return
        if child.tag.__eq__(prefix + name):
            data.append(child.text)
            _rec(child.getchildren(), data, name, prefix)
            continue
        _rec(child.getchildren(), data, name, prefix)


print(parser('instanceId'))