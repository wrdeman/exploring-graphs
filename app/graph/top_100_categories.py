import csv
from operator import itemgetter

from utils import get_graph


if __name__ == "__main__":
    nodes = get_graph()

    categories = []
    with open('/data/wiki-topcats-categories.txt') as f:
        for row in f:
            category, pages = row.split(";")
            pages = pages.split(" ")
            pages[-1] = pages[-1].replace("\n", "")
            pages = [int(page) for page in pages if page != ""]
            all_edges = []
            for page in pages:
                all_edges.extend(nodes[page].get_all_edges())
            count = len(set(all_edges) - set(pages))
            categories.append([category, count])

    # write out results
    categories = sorted(categories, key=itemgetter(1), reverse=True)[:100]
    with open('/data/results_connectivity.csv', 'w') as f:
        writer = csv.writer(f, delimiter=',')
        for line in categories:
            writer.writerow(line)
    f.close()
