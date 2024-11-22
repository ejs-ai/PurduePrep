# Use the nikolaik/python-nodejs image for both Python and Node.js
FROM nikolaik/python-nodejs:python3.12-nodejs21-slim-canary as base

# Set the working directory for the Python app
WORKDIR /app

# Copy the requirements.txt file and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt --extra-index-url https://download.pytorch.org/whl/cpu

# Copy the PurduePrep folder into the container
COPY PurduePrep /app/PurduePrep

# Set the working directory for the frontend
WORKDIR /frontend

# Copy the frontend code
COPY PurduePrep/frontend/purdueprep-web /frontend

# Install frontend dependencies
RUN npm install
# RUN npm audit fix

# Expose the frontend dev server port (optional)
EXPOSE 3000

# Expose the Flask app's port
EXPOSE 5328

# Set environment variables for Python and Flask
ENV PYTHONPATH=/app

# Default command to start both the backend and the frontend
CMD ["sh", "-c", "python3 /app/PurduePrep/app.py & cd /frontend && npm run dev"]
