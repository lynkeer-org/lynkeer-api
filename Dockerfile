FROM python:3.10

# Set working dir inside the app folder
WORKDIR /app

# Copy only necessary files
COPY requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir -r /app/requirements.txt

# This makes "app" a top-level module
ENV PYTHONPATH=/app

# Copy just the contents of the app folder
#COPY ./app /app
COPY . /app


CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]

