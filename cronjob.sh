#!/bin/bash

# Set environment variables
export LOGS_PATH=/home/schrutebeet/Desktop/logs
export DATABASE_HOST=localhost

# Change working directory
cd /home/schrutebeet/Desktop/supermarket_data

# Run main file
python -m src.main
