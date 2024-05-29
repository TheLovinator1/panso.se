# Stage 1: Build the requirements.txt using Poetry
FROM python:3.12-slim

# Create a non-root user
RUN useradd -ms /bin/bash appuser

# Switch to the non-root user
USER appuser

# Copy all of the files to the /app directory
COPY --chown=appuser:appuser . /app

# Set the working directory
WORKDIR /app

# Create a virtual environment and activate it
RUN python -m venv /app/.venv
ENV PATH="/app/.venv/bin:$PATH"

# Install application dependencies
RUN pip install --no-cache-dir -r requirements.txt

# The port the application will listen on
EXPOSE 8000

# Database and STATIC_ROOT are stored in /home/appuser/.local/share/Panso
VOLUME ["/home/appuser/.local/share/Panso"]

# Run startup script
CMD ["./docker-entrypoint.sh"]
