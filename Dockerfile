FROM nogil/python

# Install dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# Create a working directory and copy application into container
WORKDIR /app
COPY . .

