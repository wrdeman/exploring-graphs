from operator import itemgetter


if __name__ == "__main__":
    def add_to_node(node):
        if node in nodes.keys():
            nodes[node] += 1
        else:
            nodes[node] = 1

    nodes = {}
    with open('/data/wiki-topcats.txt') as f:
        for row in f:
            node1, node2 = row.split(" ")
            add_to_node(int(node1))
            add_to_node(int(node2.replace("\n", "")))

    # convert dict of key: counts into a list for sorting
    nodes = [[k, v] for k, v in nodes.items()]
    # sort list of (key, count) highest first and limit to 100
    nodes = sorted(nodes, key=itemgetter(1), reverse=True)[:100]
    # convert list of 100 into a dict so it's easier to append the real name
    nodes = {node[0]: {'name': '', 'count': node[1]} for node in nodes}

    # scan through the table of names and match name with id
    with open('/data/wiki-topcats-page-names.txt') as f:
        for row in f:
            _id, name = row.split(" ", 1)
            if int(_id) in nodes.keys():
                name = name.replace("\n", "")
                nodes[int(_id)]['name'] = name

    # write out results

    nodes = [[k, v['name'], v['count']] for k, v in nodes.items()]
    with open('/data/results_pages.txt', 'w') as f:
        for line in nodes:
            line = [str(l) for l in line]
            line = ",".join(line)
            line += "\n"
            f.write(line)
    f.close()
    #
    # categories = []
    # with open('data/wiki-topcats-categories.txt') as f:
    #     for row in f:
    #         category, pages = row.split(";")
    #         pages = pages.split(" ")
    #         pages[-1] = pages[-1].replace("\n", "")
    #         connectivity = sum(c[page] for page in pages)
    #         categories.append([category, connectivity])
    #
    # c = sorted(categories, key=itemgetter(1), reverse=True)
    # with open('results/categories.txt', 'w') as f:
    #     for line in c:
    #         f.write("{},{}\n".format(line[0], line[1]))
    # f.close()


