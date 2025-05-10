FROM python:3.11-slim

# Set environment variables
ENV FLASK_APP=src.api.app:create_app
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_ENV=development
ENV PYTHONPATH=/app/src

# Set working directory inside the container
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy source code into the container
COPY src/ ./src/

# Expose the port your app runs on
EXPOSE 5000

# Run the Flask app
CMD ["flask", "run"]
