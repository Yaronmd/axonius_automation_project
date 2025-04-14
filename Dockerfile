FROM python:3.9-slim


WORKDIR /app

# Install system dependencies for Playwright and pip tools
RUN apt-get update && \
    apt-get install -y curl wget gnupg libnss3 libatk-bridge2.0-0 libcups2 libxkbcommon0 libasound2 libxcomposite1 libxrandr2 libgtk-3-0 libxdamage1 libgbm1 && \
    rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install -r requirements.txt && \
    pip install playwright && \
    playwright install --with-deps

# Copy project
COPY . .

# Default command to run tests
CMD ["pytest", "-s"]
