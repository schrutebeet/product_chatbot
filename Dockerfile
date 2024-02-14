# Use an official Python runtime as a parent image
FROM python:3.11.8


# Create logs directory 
RUN mkdir /logs

# Define environment variable
ENV LOGS_PATH /logs

# Install poetry to be able to install requirements
RUN pip install poetry

# Create app directory 
RUN mkdir /app

# Copy toml file to download specific requirements
COPY ./pyproject.toml /app

# Set the working directory to /app
WORKDIR /app

# Install any needed packages specified in the toml file
RUN poetry install

# Copy the current directory contents into the container at /stocksapp
COPY . .

# Run app.py when the container launches
CMD ["poetry","run","python", "-m", "src.main"]