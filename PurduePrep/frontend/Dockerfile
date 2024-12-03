# Frontend Dockerfile
FROM node:18-slim

# Set the working directory
WORKDIR /frontend

# Copy the package.json and install dependencies
COPY frontend/package.json frontend/package-lock.json ./
RUN npm install

# Copy the source code into the container
COPY frontend/ ./

# Build the frontend (for production)
RUN npm run build

# Expose the port that the frontend will run on
EXPOSE 3000

# Command to start the frontend (e.g., for React)
CMD ["npm", "start"]
