# Base image
FROM tiangolo/uvicorn-gunicorn-fastapi:python3.9-slim

# Set the working directory inside the container
WORKDIR /app

# Receive API Key as a build argument
ARG API_KEY

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV API_KEY=$API_KEY

# Copy the application code
COPY . .

# Update pip and install the Python dependencies
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Expose the port that the FastAPI application will run on
EXPOSE 8000

# Start the FastAPI application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
