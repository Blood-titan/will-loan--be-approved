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

# Streamlit config (disable CORS/XSRF for Docker use)
RUN mkdir -p ~/.streamlit && \
    echo "\
    [server]\n\
    headless = true\n\
    enableCORS = false\n\
    enableXsrfProtection = false\n\
    " > ~/.streamlit/config.toml

# Expose Streamlit port
EXPOSE 8501

# Run Streamlit app
ENTRYPOINT ["streamlit", "run"]
CMD ["main.py", "--server.port=8501", "--server.address=0.0.0.0"]
