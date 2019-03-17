FROM python:3.7-alpine
ADD app/ /app
WORKDIR /app
RUN export PYTHONPATH="$PYTHONPATH:/app"
RUN pip install -r requirements.txt
