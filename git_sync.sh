#!/bin/bash

# Git automation script
echo "Running Git automation script..."

# Make the script exit on any error
set -e

# Run the Python script for git automation
python3 git_automation.py

# Store the exit status
exit_status=$?

# Check exit status and provide appropriate message
if [ $exit_status -eq 0 ]; then
    echo "Git synchronization completed successfully"
    exit 0
else
    echo "Git synchronization failed"
    exit 1
fi
