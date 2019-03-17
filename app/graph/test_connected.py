import pytest

from connected import is_connected, get_subgraphs
from paths import path_from_node, get_all_paths
from utils import add_to_node, Node, add_to_graph


def build_graph(adjacency_list):
    """build_graph

    :param adjacency_list:
    """
    graph = {}
    for node1, nodes in adjacency_list.items():
        # allow hanging node - if it has not connections then add it
        if nodes == []:
            if node1 not in graph:
                graph[node1] = Node(node1)
        for node2 in nodes:
            graph = add_to_node(graph, node1, node2)
    return graph


def test_build_graph():
    """test_build_graph
    test that building a graph from adjacency list
    """
    adjacency_list = {
        0: [1, 2],
        1: [],
        2: [],
    }
    graph = build_graph(adjacency_list)
    assert sorted(graph.keys()) == [0, 1, 2]
    assert sorted([i._id for i in graph[0].get_all_edges()]) == [1, 2]
    assert sorted([i._id for i in graph[1].get_all_edges()]) == [0]
    assert sorted([i._id for i in graph[2].get_all_edges()]) == [0]


@pytest.mark.parametrize("test_input,expected", [
    (0, True),
    (1, True),
    (2, True)
])
def test_connections_complete(test_input, expected):
    adjacency_list = {
        0: [1, 2],
        1: [],
        2: [],
    }
    graph = build_graph(adjacency_list)
    node = graph[test_input]
    graph = graph.values()
    assert is_connected(graph, node)[0] is expected


@pytest.mark.parametrize("test_input,expected", [
    (0, False),
    (1, False),
    (2, False),
    (3, False)
])
def test_connections_incomplete(test_input, expected):
    adjacency_list = {
        0: [1, 2],
        1: [],
        2: [],
        3: []
    }
    graph = build_graph(adjacency_list)
    node = graph[test_input]
    graph = graph.values()
    assert is_connected(graph, node)[0] is expected


def test_connections_subgraphs():
    adjacency_list = {
        0: [1, 2],
        1: [],
        2: [],
        3: []
    }
    graph = build_graph(adjacency_list)
    graph = graph.values()
    assert get_subgraphs(graph) == 2


def test_connections_subgraphs_complete():
    adjacency_list = {
        0: [1, 2, 3],
        1: [],
        2: [3, 4],
        3: [4],
        4: []
    }
    graph = build_graph(adjacency_list)
    graph = graph.values()
    assert get_subgraphs(graph) == 1


def test_add_to_graph():
    test = [
        "0 1",
        "0 2",
    ]
    nodes = add_to_graph(test)
    assert sorted([n._id for n in nodes[0].linked_to]) == [1, 2]
    assert sorted([n._id for n in nodes[0].linked_from]) == []
    assert sorted([n._id for n in nodes[1].linked_to]) == []
    assert sorted([n._id for n in nodes[1].linked_from]) == [0]
    assert sorted([n._id for n in nodes[2].linked_to]) == []
    assert sorted([n._id for n in nodes[2].linked_from]) == [0]


def test_path():
    adjacency_list = {
        0: [1, 4],
        1: [2, 4],
        2: [3, 1],
        3: [2, 4, 5],
        4: [0, 1],
        5: [3],
    }
    test = [
        [5, 0],
        [3, 1],
        [2, 2],
        [1, 3],
        [4, 2],
        [0, 3]
    ]
    graph = build_graph(adjacency_list)
    node_start = graph[5]
    graph = graph.values()
    path_from_node(graph, node_start)

    assert sorted([[g._id, g.path] for g in graph]) == sorted(test)


def test_all_paths():
    adjacency_list = {
        0: [1, 4],
        1: [2, 4],
        2: [3, 1],
        3: [2, 4, 5],
        4: [0, 1],
        5: [3],
    }
    test = [
        [5, 0],
        [3, 1],
        [2, 2],
        [1, 3],
        [4, 2],
        [0, 3]
    ]
    graph = build_graph(adjacency_list)
    graph = graph.values()
    paths = get_all_paths(graph)
    assert sorted([[g._id, g.path] for g in graph]) == sorted(test)
