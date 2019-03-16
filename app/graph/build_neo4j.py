import os
import sys

import neo4j
from neobolt.exceptions import AuthError

from preprocess import txt_to_csv, get_category_names


def get_driver():
    """get_driver
    get an instance of the neo4j neobolt driver

    The neo4j image starts with a username/password neo4j/neo4j. However,
    one is required to change the password before making any requests.

    So we try to connect with our 'test' password - on failure we then try ro
    change the default password
    """
    uri = "bolt://db:7687"
    uname = 'neo4j'
    pword = 'test'
    try:
        driver = neo4j.GraphDatabase.driver(uri, auth=(uname, pword))
    except AuthError:
        tword = 'neo4j'
        driver = neo4j.GraphDatabase.driver(uri, auth=(uname, tword))
        q = "CALL dbms.changePassword('test')"
        with driver.session() as session:
            session.run(q)
            session.close()
        driver = neo4j.GraphDatabase.driver(uri, auth=(uname, pword))
    return driver


# add page names to neo4j from csv load
CREATE_PAGE = """
CREATE CONSTRAINT ON (page:Page) ASSERT page.id IS UNIQUE
"""

CREATE_CATEGORIES = """
CREATE CONSTRAINT ON (category:Category) ASSERT category.id IS UNIQUE
"""


COMMIT_PAGE_NAMES = """
USING PERIODIC COMMIT
LOAD CSV FROM 'file:///data/wiki-topcats-page-names.csv' AS line
CREATE (page:Page { name: line[1], id: toInt(line[0])})
"""

COMMIT_PAGE_LINKS = """
USING PERIODIC COMMIT
LOAD CSV FROM 'file:///data/wiki-topcats.txt' AS line
FIELDTERMINATOR " "
MATCH(page1:Page {id: toInt(line[0])})
MATCH(page2:Page {id: toInt(line[1])})
CREATE (page1)-[:LINKS]->(page2)
"""

COMMIT_CATEGORY_NAMES = """
USING PERIODIC COMMIT
LOAD CSV FROM 'file:///data/wiki-topcats-categories-names.csv' AS line
CREATE (category:Category { name: line[1], id: toInt(line[0])})
"""


def create(driver, query):
    """create_index

    run query on neo4j and exit application if it fails

    :param driver: neo4j driver object
    :param query: cypher query string
    """
    # LOAD PAGE NAMES
    with driver.session() as session:
        try:
            session.run(query)
            session.close()
        except Exception as e:
            print(e)
            sys.exit()


def load_pages(driver):
    """load_pages
    Load the page data - id, name. First step is to create a csv that is
    formatted for the neo4j load csv endpoint. Whatever happens we remove the
    csv file at the end

    :param driver: neo4j driver
    """
    csv_fname = txt_to_csv(
        '/data/wiki-topcats-page-names.txt',
        quote=True,
    )

    with driver.session() as session:
        try:
            session.run(COMMIT_PAGE_NAMES)
            session.close()
        except Exception as e:
            print(e)
        finally:
            if os.path.exists(csv_fname):
                pass
                os.remove(csv_fname)


def load_categories(driver):
    """load_categories
    Load the category data - id, name. First step is to create a csv that is
    formatted for the neo4j load csv endpoint. Whatever happens we remove the
    csv file at the end

    :param driver: neo4j driver
    """
    csv_fname = get_category_names(
        '/data/wiki-topcats-categories.txt',
        csv_fname='/data/wiki-topcats-categories-names.csv'
    )

    with driver.session() as session:
        try:
            session.run(COMMIT_CATEGORY_NAMES)
            session.close()
        except Exception as e:
            print(e)
        finally:
            if os.path.exists(csv_fname):
                pass
                os.remove(csv_fname)


if __name__ == "__main__":
    # get the driver
    driver = get_driver()
    # pages
    create(driver, CREATE_PAGE)
    load_pages(driver)
    # page links
    create(driver, COMMIT_PAGE_LINKS)
    # categories
    create(driver, CREATE_CATEGORIES)
    load_categories(driver)
