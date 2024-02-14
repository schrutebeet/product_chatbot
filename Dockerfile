# Use an official Python runtime as a parent image
FROM python:3.11.8

# Set the working directory to /app
WORKDIR /app

# Copy toml file to download specific requirements
COPY ./pyproject.toml app/

# Install poetry to be able to install requirements
RUN pip install poetry

# Install any needed packages specified in the toml file
RUN poetry install --no-root

# Create logs directory 
RUN mkdir /logs

# Define environment variable
ENV LOGS_PATH /logs

# Copy the current directory contents into the container at /stocksapp
COPY . /app


# Run app.py when the container launches
CMD ["python", "-m", "src.main"]
