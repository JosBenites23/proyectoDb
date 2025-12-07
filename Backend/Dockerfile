# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file and install dependencies
# This is done in a way that preserves the package structure and leverages Docker caching
RUN mkdir /app/Backend
COPY Backend/requirements.txt /app/Backend/requirements.txt
RUN pip install --no-cache-dir -r /app/Backend/requirements.txt

# Copy the backend application code into the Backend directory
COPY Backend/ /app/Backend/

# Expose port 8000 and run the application as a module
EXPOSE 8000
CMD ["uvicorn", "Backend.main:app", "--reload", "--host", "0.0.0.0", "--port", "8000"]
