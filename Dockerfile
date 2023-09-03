# BASE IMAGE
FROM python:3.10

RUN python3 -m venv /opt/venv

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app/

# Install any needed packages specified in requirements.txt
RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN /opt/venv/bin/pip pip install -r requirements.txt

# Make port 8000 available to the world outside this container
EXPOSE 8000

# Uruchomienie migracji i serwera Django
CMD python manage.py migrate
CMD python manage.py runserver 0.0.0.0:8000







