FROM python:3.12-slim

# Set working directory
WORKDIR /backend

# Install dependencies
COPY backend/requirements.txt ./
RUN pip install --no-cache-dir torch==2.5.1 --extra-index-url https://download.pytorch.org/whl/cpu \
    && pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY backend ./

EXPOSE 8080

# Run the application
CMD ["python", "app.py"]