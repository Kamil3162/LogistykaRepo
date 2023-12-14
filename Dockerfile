# Use the official Python image as the base image
FROM python:3.10

# Install system dependencies for mysqlclient
RUN apt-get update \
    && apt-get install -y default-libmysqlclient-dev gcc

# Create a virtual environment
RUN python -m venv /opt/venv

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app/

# Upgrade pip and install packages from requirements.txt
RUN apt-get update && apt-get install -y \
    gcc \
    libffi-dev \
    libssl-dev \
    python3-dev
RUN /opt/venv/bin/pip install --upgrade pip
COPY requirements.txt .
RUN /opt/venv/bin/pip install -r requirements.txt

# Make port 8000 available to the world outside this container
EXPOSE 8000

# Activate virtual environment and run Django server
#CMD /opt/venv/bin/activate && /opt/venv/bin/python manage.py migrate && /opt/venv/bin/python manage.py runserver 0.0.0.0:8000
CMD /opt/venv/bin/python manage.py migrate && /opt/venv/bin/python manage.py runserver 0.0.0.0:8000
