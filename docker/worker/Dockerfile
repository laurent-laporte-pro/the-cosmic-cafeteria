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
