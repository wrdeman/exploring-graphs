FROM python:3.7-alpine
ADD app/ /app
WORKDIR /app
RUN export PYTHONPATH="$PYTHONPATH:/app"
# add for scipy
# RUN apk add openblas-dev gfortran make automake gcc g++ subversion python3-dev
RUN pip install -r requirements.txt
