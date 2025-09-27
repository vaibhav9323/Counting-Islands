#!/bin/bash

# This script runs the island-counter application inside a Docker container.
# It takes a single argument: the path to the input file. 

# Check if a file path is provided
if [ -z "$1" ]; then
    echo "Error: No input file specified." >&2
    echo "Usage: ./run.sh <path_to_the_file>" >&2
    # Run the container without args to show the help message from argparse
    docker run --rm island-counter:latest
    exit 1
fi

INPUT_FILE_PATH=$1
INPUT_FILE_NAME=$(basename "$INPUT_FILE_PATH")
INPUT_FILE_DIR=$(dirname "$INPUT_FILE_PATH")
ABS_INPUT_FILE_DIR=$(cd "$INPUT_FILE_DIR" && pwd)

# Check if the file exists
if [ ! -f "$INPUT_FILE_PATH" ]; then
    echo "Error: File not found at '$INPUT_FILE_PATH'" >&2
    exit 1
fi

# Run the Docker container
# -v mounts the directory containing the input file into the container at /data
# --rm automatically removes the container when it exits
docker run --rm \
    -v "$ABS_INPUT_FILE_DIR":/data \
    island-counter:latest "/data/$INPUT_FILE_NAME"