#!/bin/bash

set -x

# Check if a filename was provided
if [ -z "$1" ]; then
    echo "Usage: $0 <filename_without_extension>"
    echo "Example: $0 vector_algos"
    exit 1
fi

# Configuration
TARGET=$1
SOURCE="${TARGET}.cpp"
UTILS_DIR="../utils"

# Verify source file exists
if [ ! -f "$SOURCE" ]; then
    echo "Error: Source file '$SOURCE' not found."
    exit 1
fi

echo "--- Compiling $SOURCE ---"

# The generalized compile command
clang++ -std=c++23 -O2 -g0 \
    -I"$UTILS_DIR" \
    "$UTILS_DIR/loguru.cpp" \
    "$UTILS_DIR/logging.cpp" \
    "$UTILS_DIR/stl_utils.cpp" \
    "$SOURCE" \
    -o "$TARGET" \
    -lpthread -lstdc++ -lm

# Only run the binary if compilation was successful
if [ $? -eq 0 ]; then
    echo "--- Running $TARGET ---"
    ./"$TARGET"
else
    echo "--- Compilation Failed ---"
    exit 1
fi
