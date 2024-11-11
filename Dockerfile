# Use the official Python image from Docker Hub
FROM python:3.11.9-slim-bullseye

ENV PYTHONBUFFERED=1

ENV PORT 8080

# Set the working directory in the container
WORKDIR /app

# Copy the dependency file and install dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy the project files into the container
COPY . /app/

# CMD gunicorn server.wsgi:application --bind 0.0.0.0:8080
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "credit_approval.wsgi:application"]


# Expose the port Django will run on
EXPOSE 8080

# Run the Django application

