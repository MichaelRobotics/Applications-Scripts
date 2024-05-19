# Use the official Python image from the Docker Hub
FROM python:3.10-alpine

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt ./

# Copy the rest of the application code into the container
COPY . .

# Expose port 8080 to be able to access the application
EXPOSE 8080

# Command to run the application
ENTRYPOINT ["python", "app.py"]