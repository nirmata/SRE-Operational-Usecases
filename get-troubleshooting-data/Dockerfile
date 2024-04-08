# Use an official Python runtime as the base image
FROM python:3.9

# Set the working directory in the container
WORKDIR /app

# Copy the Python script and requirements file into the container
COPY fetch-crashloopback-data.py get-debug-jira-v2.sh /app/

# Update the package list and install jq and curl
RUN apt-get update && apt-get install -y \
    jq \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install the Python dependencies
# Uncomment the following line if you have a requirements.txt file
# RUN pip install --no-cache-dir -r requirements.txt

RUN pip install kubernetes 

# Run the Python script when the container launches
CMD ["./get-debug-jira-v2.sh"]
