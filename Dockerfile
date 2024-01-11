FROM python:latest

# Install dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# Create a working directory and copy application into container
WORKDIR /app
COPY . .

ENV FLASK_APP=app

EXPOSE 80

CMD waitress-serve --port 80 --host 0.0.0.0 --call app:create_app

