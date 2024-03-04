# Pull the base image
FROM python:3.8-slim-buster

# Set environment variables
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    netcat \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory
WORKDIR /app/project

# Copy the requirement files and install the dependencies
COPY ./requirements.txt /tmp/requirements.txt
COPY ./requirements-dev.txt /tmp/requirements-dev.txt

# Copy scripts code
COPY ./scripts /app/scripts

# Run the script
RUN /app/scripts/setup.sh

# Copy project code
COPY ./project .

# Exposing the port
EXPOSE 8000

# Run run.sh
CMD ["/app/scripts/run.sh"]
