#!/bin/sh

# Set error handling
set -e

# Build client
echo "Building client..."
cd ./client
mkdir -p build
cd build
cmake ..
cmake --build .
cd ../..

# Build server
echo "Building server..."
cd ./server
mkdir -p build
cd build
cmake ..
cmake --build .
cd ../..

echo "Build completed successfully."
