# Base image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy app files
COPY . .

# Expose port for FastAPI
EXPOSE 8501

# Run FastAPI app using uvicorn
CMD ["uvicorn", "api_app:app", "--host", "0.0.0.0", "--port", "8501", "--reload"]
