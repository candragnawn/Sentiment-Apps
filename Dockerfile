# Use official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the backend requirements file into the container at /app
COPY backend/requirements.txt /app/requirements.txt

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install gunicorn uvicorn

# Copy the rest of the backend code
COPY backend /app/backend

# Make port 8000 available to the world outside this container
EXPOSE 8000

# Define environment variable
ENV PYTHONPATH=/app/backend/src

# Run app.py when the container launches
CMD ["uvicorn", "backend.src.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "4"]
