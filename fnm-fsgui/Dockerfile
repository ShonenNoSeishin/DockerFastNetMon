# Use an official Python runtime as a parent image
FROM python:3.11

# Set the working directory in the container
WORKDIR /app

# Install any needed packages specified in requirements.txt
COPY . .
RUN pip install -r requirements.txt

# Set default values if no ENV VARs found
ENV DEFAULT_API_ENDPOINT="http://127.0.0.1:10007"
ENV DEFAULT_API_USER="fnmadmin"
ENV DEFAULT_API_PASSWORD="fnmpassword"

# Make port 8024 available to the world outside this container
EXPOSE 8024
