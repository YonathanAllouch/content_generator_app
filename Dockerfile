# Use an official Python runtime as a parent image, adjust as specific versions become available
FROM python:3.12-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Make port 5000 available to the world outside this container
EXPOSE 5000

# Use Gunicorn to serve the app; adjust the number of workers and threads as needed
CMD ["gunicorn", "--workers", "3", "--threads", "2", "-b", ":5000", "main:app"]
