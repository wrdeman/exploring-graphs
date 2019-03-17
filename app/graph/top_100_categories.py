import csv
import gzip
from operator import itemgetter

from utils import get_graph


if __name__ == "__main__":
    """ Within a given category we want to know the number of connections
    between pages in that category. So we get the pages within a category
    and sum the connections that occur between the pages in the category
    and exlude inter-category pages.

    First we create a lookup for graph nodes (pages) that contains a list of
    the pages link to/from it. Then we get the category and the pages within
    it and for each page it count the links to/from excluding the pages out
    of that category

    The count is the intersection (&) of all_links_for_all_pages and pages.
    Note by getting the difference (-) we can get the connectivity of the
    category.
    """
    # get a dictionary representation of the graph {id: Node, ..}
    nodes = get_graph()

    categories = []
    f = gzip.open('/data/wiki-topcats-categories.txt.gz', 'rt')
    for row in f:
        # get category and pages
        # format "category; id id id .."
        category, pages = row.split(";")
        pages = pages.split(" ")
        pages[-1] = pages[-1].replace("\n", "")
        pages = [int(page) for page in pages if page != ""]

        # for all the pages in the category count excluding pages outside
        all_edges = []
        for page in pages:
            all_edges.extend(nodes[page].get_all_edges())
        # intersection of all destination pages of the pages in the
        # categories and all the pages in the category
        count = len(set(all_edges) & set(pages))
        categories.append([category, count])
    f.close()

    # write out results
    categories = sorted(categories, key=itemgetter(1), reverse=True)[:100]
    with open('/data/results_connectivity.csv', 'w') as f:
        writer = csv.writer(f, delimiter=',')
        for line in categories:
            writer.writerow(line)
    f.close()
