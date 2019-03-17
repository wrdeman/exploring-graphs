import gzip
import math


class Node(object):
    visited = False
    path = math.inf  # work in progress ...
    """Node
    Object for a basic node. Contains an id, and a list of edges into and a
    list of edges out
    """
    def __init__(self, _id):
        self._id = _id
        self.linked_to = []
        self.linked_from = []

    def add_to(self, node):
        """add_to
        add an edge/vertec directed into this node

        :param node: node to be added
        """
        self.linked_to.append(node)

    def add_from(self, node):
        """add_from
        add an edge/vertex directed away from this node

        :param node: node to be added
        """
        self.linked_from.append(node)

    def get_all_edges(self):
        """get_all_edges
        the degree of the node
        return the edges in/out this node

        """
        return self.linked_to + self.linked_from


def add_to_node(nodes, node1_id, node2_id):
    """add_to_node
    add a node to a node

    creates the nodes if they don't exist

    :param node1_id: id to be added
    :param node2_id:
    """
    if node1_id in nodes.keys():
        node1 = nodes[node1_id]
    else:
        node1 = Node(node1_id)
        nodes[node1_id] = node1

    if node2_id in nodes.keys():
        node2 = nodes[node2_id]
    else:
        node2 = Node(node2_id)
        nodes[node2_id] = node2

    node1.add_to(node2)
    node2.add_from(node1)
    return nodes


def add_to_graph(iterable):
    """add_to_graph
    build a graph from an iterable 'list' of strings '1 2'

    :param iterable: can file object of list
    """
    nodes = {}
    for row in iterable:
        node1, node2 = row.split(" ")
        nodes = add_to_node(
            nodes, int(node1), int(node2.replace("\n", ""))
        )
    return nodes


def get_graph():
    with gzip.open('/data/wiki-topcats.txt.gz', 'rt') as f:
        nodes = add_to_graph(f)
    return nodes


def get_graph_list():
    nodes = get_graph()
    nodes = nodes.values()
    return nodes
