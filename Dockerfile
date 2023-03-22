FROM python:3.11-slim-buster



# Install dependencies

RUN apt-get update && apt-get install -y curl && \

    curl -fsSL https://deb.nodesource.com/setup_16.x | bash - && \

    apt-get install -y nodejs



# Set the working directory for the app

WORKDIR /app



# Install Python dependencies

COPY requirements.txt .

RUN pip install -r requirements.txt



# Copy the backend code into the container

COPY main.py .

COPY utils/ ./utils/

COPY db/ ./db/



# Copy the frontend code into the container

COPY client/ ./client/



# Build the frontend

WORKDIR /app/client



# Set the working directory back to the app root

WORKDIR /app



# Start the server

CMD ["sh", "-c", "uvicorn main:app --host 0.0.0.0 --port 8000 & node client/server.js"]