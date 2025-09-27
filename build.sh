#!/bin/bash
echo "Building the island-counter docker image..."
docker build -t island-counter:latest .
echo "Build complete."