# Backend Dockerfile
FROM python:3.12-slim

# Set the working directory
WORKDIR /backend

# Copy the requirements.txt and install dependencies
COPY backend/requirements.txt ./
RUN pip install torch==2.5.1 --extra-index-url https://download.pytorch.org/whl/cpu
RUN pip install --no-cache-dir -r requirements.txt --extra-index-url https://download.pytorch.org/whl/cpu

# Copy the backend application files into the container
COPY backend/ /backend/

# Expose the port for Flask app
EXPOSE 5328

# Command to run the Flask app
CMD ["python3", "app.py"]
