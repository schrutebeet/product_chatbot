#!/bin/bash

# Set environment variables
export LOGS_PATH=/home/schrutebeet/Desktop/logs/supermarkets
export DATABASE_HOST=localhost

# Change working directory
cd /home/schrutebeet/Desktop/supermarket_data

# Set up python environment
source super_venv/bin/activate

# Run main file
python -m src.main
