#!/bin/bash

curl -XGET https://snap.stanford.edu/data/wiki-topcats.txt.gz --output data/wiki-topcats.txt.gz 
curl -XGET https://snap.stanford.edu/data/wiki-topcats-categories.txt.gz --output data/wiki-topcats-categories.txt.gz
curl -XGET https://snap.stanford.edu/data/wiki-topcats-page-names.txt.gz --output data/wiki-topcats-page-names.txt.gz
