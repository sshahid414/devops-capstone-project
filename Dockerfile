##################################################
# Create production image
##################################################
FROM python:3.9-slim

# Establish a working folder
WORKDIR /app

# Install dependencies first for better layer caching
COPY requirements.txt .
RUN python -m pip install --upgrade pip wheel && \
    pip install --no-cache-dir -r requirements.txt

# Copy the application contents
COPY service/ ./service/

# Switch to a non-root user for security
RUN useradd --uid 1000 theia && chown -R theia /app
USER theia

# Expose the port and run the service with gunicorn
EXPOSE 8080
CMD ["gunicorn", "--bind=0.0.0.0:8080", "--log-level=info", "service:app"]
