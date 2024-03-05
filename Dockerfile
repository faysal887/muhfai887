# Use an official Python runtime as a parent image
FROM python:3.9-slim-buster

# Set the working directory to /app
WORKDIR /app

# Copy only the requirements file to the container
COPY requirements.txt .

# Install development tools and libraries
RUN apt-get update && \
    apt-get install -y build-essential libssl-dev libffi-dev python3-dev

RUN python -m ensurepip --upgrade

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code to the container
COPY . .

# Make port 80 available to the world outside this container
EXPOSE 80

# Run app.py when the container launches
CMD ["uvicorn", "endpoint:app", "--host", "0.0.0.0", "--port", "80"]
