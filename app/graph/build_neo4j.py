import os
import sys

import neo4j
from neobolt.exceptions import AuthError

from preprocess import txt_to_csv, get_category_names


def get_driver():
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


def create_index(driver, query):
    # LOAD PAGE NAMES
    with driver.session() as session:
        # create  page with constraint
        try:
            session.run(query)
            session.close()
        except Exception as e:
            print(e)
            sys.exit()


def load_pages(driver):
    # get pages and convert to csv
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
            # clean up
            if os.path.exists(csv_fname):
                pass
                os.remove(csv_fname)


def load_page_links(self):
    with driver.session() as session:
        try:
            session.run(COMMIT_PAGE_LINKS)
            session.close()
        except Exception as e:
            print(e)


def load_categories(driver):
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
            # clean up
            if os.path.exists(csv_fname):
                pass
                os.remove(csv_fname)


if __name__ == "__main__":
    driver = get_driver()
    # create_index(driver, CREATE_PAGE)
    # load_pages(driver)
    # load_page_links(driver)
    create_index(driver, CREATE_CATEGORIES)
    load_categories(driver)
