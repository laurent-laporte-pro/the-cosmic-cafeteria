# Use official Python image
FROM python:3.12-slim

# Set work directory
WORKDIR /app

# Copy workspace
COPY ../../ .
# Install dependencies
RUN pip install -e .
RUN pip list
RUN pip install click


# Set environment variables
ENV FLASK_APP=src/cli/__main__.py

# Expose port
EXPOSE 5000
