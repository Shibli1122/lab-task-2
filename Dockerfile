# Use Node.js on a Debian base to allow installing Python & Postgres tools
FROM node:18-bullseye-slim

# Install Python 3, pip, and PostgreSQL dependencies
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Install psycopg2-binary for your Python script
RUN pip3 install psycopg2-binary

WORKDIR /app

# Create the folder structure expected by your Node app
RUN mkdir backend database

# Copy your files into their respective folders
COPY backend_package.json ./backend/package.json
COPY backend_server.js ./backend/server.js
COPY database_service.py ./database/db_service.py

# Install Node dependencies
RUN cd backend && npm install

# Initialize DB and start the server
CMD python3 database/db_service.py && node backend/server.js