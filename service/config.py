"""
Global Configuration for Application
"""
import os
import logging

# Get configuration from environment.
# Defaults to a local SQLite database so the service runs with zero infra.
# In CI / Kubernetes this is overridden with a PostgreSQL connection string.
DATABASE_URI = os.getenv("DATABASE_URI", "sqlite:///accounts.db")

# Configure SQLAlchemy
SQLALCHEMY_DATABASE_URI = DATABASE_URI
SQLALCHEMY_TRACK_MODIFICATIONS = False

# Secret for session management
SECRET_KEY = os.getenv("SECRET_KEY", "sup3r-s3cr3t")

# Logging level
LOGGING_LEVEL = logging.INFO
