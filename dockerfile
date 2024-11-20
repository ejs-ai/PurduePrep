# Use the official Python 3.12 image
FROM python:3.12

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements.txt file and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the PurduePrep folder into the container
COPY PurduePrep /app/PurduePrep

# Expose the port Flask will run on
EXPOSE 5328

# Set the Python path to include the /app directory
ENV PYTHONPATH=/app

# Set the default command to run the Flask app
CMD ["python", "PurduePrep/app.py"]
