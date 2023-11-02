FROM python:latest

# Install dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# Create a working directory and copy application into container
WORKDIR /app
COPY ./app/ .

CMD [ "python", "main.py"]

