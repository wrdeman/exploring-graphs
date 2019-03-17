import sys
import math
from utils import get_graph_list


def path_from_node(graph, node):
    """path_from_node
    calculate the shortest path to each node from an initial node

    from the start node we visit each node from the start point (directional)
    the increment the hop count on each of these nodes. from each of these
    nodes we follow onto the next set if we haven't been here before - this is
    what makes sure we note the shortest path

    :param graph:
    :param node:
    """

    hop_count = 1
    node.visited = True
    node.path = 0
    next_hops = node.linked_to

    while next_hops:
        this_hop = next_hops
        next_hops = []
        for hop in this_hop:
            if hop.visited is False:
                hop.path = hop_count
                hop.visited = True
                next_hops.extend(hop.linked_to)
        hop_count += 1


def get_all_paths(graph):
    paths = [[math.inf for _ in graph] for _ in graph]
    for node in graph:
        path_from_node(graph, node)
        for n in graph:
            if n != node and n.path < paths[n._id][node._id]:
                paths[n._id][node._id] = n.path
            n.visited = False
            n.path = 0
        node.visited = False
        node.path = 0
    return paths


if __name__ == "__main__":
    print("NOT FINISHED")
    sys.exit()
    nodes = get_graph_list()
    # print(get_max_paths(nodes))
