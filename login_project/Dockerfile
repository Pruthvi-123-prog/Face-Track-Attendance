# Use a Python image
FROM python:3.11-slim

# Set working directory in container
WORKDIR /app

# Copy everything into the container
COPY . /app

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Collect static files
RUN python manage.py collectstatic --noinput

# Apply migrations
RUN python manage.py migrate

# Expose port 80
EXPOSE 80

# Start the application with Gunicorn
CMD ["gunicorn", "login_project.wsgi:application", "--bind", "0.0.0.0:80"]
