# --- Stage 1: Build Frontend ---
FROM node:18-slim as build-stage
WORKDIR /app/frontend
COPY frontend/package*.json ./
RUN npm install
COPY frontend/ ./
RUN npm run build

# --- Stage 2: Backend & Final Image ---
FROM python:3.10-slim
WORKDIR /app

# Install system dependencies for Playwright
RUN apt-get update && apt-get install -y \
    curl \
    gnupg \
    libnss3 \
    libnspr4 \
    libatk1.0-0 \
    libatk-bridge2.0-0 \
    libcups2 \
    libdrm2 \
    libxkbcommon0 \
    libxcomposite1 \
    libxdamage1 \
    libxext6 \
    libxfixes3 \
    libxrandr2 \
    libgbm1 \
    libpango-1.0-0 \
    libcairo2 \
    libasound2 \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Install Playwright browsers (Chromium only for efficiency)
RUN playwright install chromium

# Copy Backend code
COPY backend/ ./

# Copy Frontend build from Stage 1
COPY --from=build-stage /app/frontend/dist ./static

# Set Environment Variables
ENV PORT=8000
EXPOSE 8000

# Start Application with Gunicorn and Uvicorn workers
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
