from utils import get_graph_list


def is_connected(graph, node):
    """is_connected

    for a given graph (list of nodes), create a queue of nodes to visit which
    for a given node is get_all_edges where the node is visible. keep popping
    and adding to this queue. once the queue is depleted - we have visited
    all the nodes in this graph.

    :param graph: Node[]
    :param node: Node a random node to start
    """
    queue = {node}
    hop_count = 0

    while True:
        # when nothing in the queue then exit loop
        try:
            node = queue.pop()
        except KeyError:
            break
        if node.visited is False:
            node.visited = True
            hop_count += 1
            queue.update([
                n for n in node.get_all_edges()
                if n.visited is False
            ])
    print(hop_count, len(graph))
    return hop_count == len(graph), graph


def get_subgraphs(graph):
    def get_visible_node(graph):
        for node in graph:
            if node.visited is False:
                return node
        raise Exception("No visible node")
    count = 0

    while True:
        count += 1

        node = get_visible_node(graph)
        is_completed, graph = is_connected(graph, node)
        if is_completed:
            print("Number of subgraphs = {}".format(count))
            break
        else:
            graph = [node for node in graph if node.visited is False]
    return count


if __name__ == "__main__":
    nodes = get_graph_list()

    print(get_subgraphs(nodes))
