FROM nikolaik/python-nodejs:python3.12-nodejs21-slim-canary AS base

# Set environment to production for Next.js
ENV NODE_ENV=production

# Install backend dependencies
# Install PyTorch
RUN pip install torch==2.5.1 --extra-index-url https://download.pytorch.org/whl/cpu
COPY PurduePrep/backend/requirements.txt ./ 
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire PurduePrep folder
COPY PurduePrep /PurduePrep

# Install frontend dependencies
WORKDIR /PurduePrep/frontend
RUN npm install

# Build frontend (Only do this during the build process)
RUN npm run build

# Expose the necessary ports
EXPOSE 3000
EXPOSE 5000


# Set Python path for backend
ENV PYTHONPATH=/PurduePrep

# Run backend and frontend in production mode
CMD ["sh", "-c", "python3 /PurduePrep/backend/app.py & cd /PurduePrep/frontend && npm run start"]
