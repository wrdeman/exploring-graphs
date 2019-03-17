import gzip
from operator import itemgetter


if __name__ == "__main__":
    """ I have assumed that the page connectivity is given by the number of
    links to and from the page. Following this we can scan the list of links
    and count the occurences of each page. The link data is two columns of
    page indexes, the left is the source and the right is the destination.

    To do this, iterate through the list incrementing a count on each occurence
    either source or destination

    """

    def add_to_node(node):
        """add_to_node
        either add a node to the dictionary of nodes or increment the exisiting
        count

        :param node: node id
        """
        if node in nodes.keys():
            nodes[node] += 1
        else:
            nodes[node] = 1

    # dictionary for nodes
    nodes = {}
    f = gzip.open('/data/wiki-topcats.txt.gz', 'rt')
    for row in f:
        # split into source/destination
        node1, node2 = row.split(" ")
        # add source
        add_to_node(int(node1))
        # add destination
        add_to_node(int(node2.replace("\n", "")))
    f.close()

    # convert dict of key: counts into a list of [id, count] for sorting
    nodes = [[k, v] for k, v in nodes.items()]

    # sort list of (key, count) highest first and limit to 100
    nodes = sorted(nodes, key=itemgetter(1), reverse=True)[:100]

    # convert list of 100 into a dict so it's easier to append the real name
    nodes = {node[0]: {'name': '', 'count': node[1]} for node in nodes}

    # scan through the table of names and match name with id
    f_names = gzip.open('/data/wiki-topcats-page-names.txt.gz', 'rt')
    for row in f_names:
        _id, name = row.split(" ", 1)
        if int(_id) in nodes.keys():
            name = name.replace("\n", "")
            nodes[int(_id)]['name'] = name
    f_names.close()

    # write out results
    nodes = [[k, v['name'], v['count']] for k, v in nodes.items()]
    with open('/data/results_pages.txt', 'w') as f_results:
        for line in nodes:
            line = [str(l) for l in line]
            line = ",".join(line)
            line += "\n"
            f_results.write(line)
    f_results.close()
