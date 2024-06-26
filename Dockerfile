# Use an official Python runtime as a parent image
FROM python:3.12-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /social_network

COPY /social_network /social_network

# Install dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt


EXPOSE 8000
# Run the application
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]