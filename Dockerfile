# Use an official Python runtime as a parent image
FROM python:3.9-slim-buster

# Set the working directory to /app
WORKDIR /app

# Update and upgrade packages
RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y build-essential libssl-dev libffi-dev python3-dev

# Install pip
RUN python -m ensurepip --default-pip

# Install pybind11 from wheels
# RUN python -m pip install pybind11
RUN pip install wheel setuptools pip --upgrade

# Install any needed packages specified in requirements.txt
COPY requirements.txt .
RUN python -m pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code to the container
COPY . .

# Make port 80 available to the world outside this container
EXPOSE 80

# Run app.py when the container launches
CMD ["uvicorn", "endpoint:app", "--host", "0.0.0.0", "--port", "80"]
