# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file and install dependencies
# This is done first to leverage Docker's layer caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application source code
COPY ./island_counter /app/island_counter

# Define the entrypoint for the container.
# This makes the container executable and runs our main script.
ENTRYPOINT ["python", "-m", "island_counter.main"]