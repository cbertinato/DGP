# coding: utf-8

from pyqtgraph.flowchart.NodeLibrary import NodeLibrary, isNodeClass

__all__ = ['derivatives', 'filters', 'gravity', 'operators', 'LIBRARY']

from . import operators, gravity, derivatives, filters, display

LIBRARY = NodeLibrary()
for mod in [operators, gravity, derivatives, filters, display]:
    # nodes = [getattr(mod, name) for name in dir(mod)
    #          if isNodeClass(getattr(mod, name))]
    nodes = [attr for attr in mod.__dict__.values() if isNodeClass(attr)]
    for node in nodes:
        # Control whether the Node is available to user in Context Menu
        if hasattr(mod, '__displayed__') and not mod.__displayed__:
            path = []
        else:
            path = [(mod.__name__.split('.')[-1].capitalize(),)]
        LIBRARY.addNodeType(node, path)
