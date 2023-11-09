FROM python:latest

# Install dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# Create a working directory and copy application into container
WORKDIR /app
COPY . .

ENV FLASK_APP=flaskr

EXPOSE 80

CMD flask --app flaskr init-db && waitress-serve --port 80 --host 0.0.0.0 --call flaskr:create_app

