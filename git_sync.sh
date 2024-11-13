#!/bin/bash

# Git automation script
echo "Running Git automation script..."
python3 git_automation.py

# Check exit status
if [ $? -eq 0 ]; then
    echo "Git synchronization completed successfully"
else
    echo "Git synchronization failed"
    exit 1
fi
