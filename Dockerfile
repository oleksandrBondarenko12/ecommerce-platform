#  Filename: Dockerfile

# Use an official Python 3.11 slim image as a base
FROM python:3.11-slim

# Prevent Python from writing .pyc files and keep output unbuffered
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory inside the container
WORKDIR /app

# Install system packages needed by psycopg2
RUN apt-get update && apt-get install -y libpq-dev && rm -rf /var/lib/apt/lists/*

# Copy the requirements file and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire project code into the working directory
COPY . .

# Expose the port 8000 to allow communication to/from the container
EXPOSE 8000
