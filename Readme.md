## Step 1: 
Start the containers
```
docker-compose up
```

## Step 2: Load data into neo4j
```
docker-compose run app /usr/local/bin/python build_neo4j.py
```

## Step 3
### Top 100 pages by connectivity
```
docker-compose run app /usr/local/bin/python graph/top_100_pages.py
```

### Top 100 catogories by page connectivity
```
docker-compose run app /usr/local/bin/python graph/top_100_categories.py
```

## Is connected
```
docker-compose run app /usr/local/bin/python graph/connected.py
```

## Docker commands
Start the containers
```
docker-compose up
```

Connect a shell in the the python container:
```
docker-compose run app /bin/sh
```

Connect to an ipython shell
```
docker-compose run app /usr/local/bin/ipython
```

Run tests:
```
docker-compose run app /usr/local/bin/pytest /app/graph/test_setup.py /app/graph/test_connected.py
```


