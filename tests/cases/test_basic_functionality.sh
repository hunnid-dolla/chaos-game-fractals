#!/bin/sh
echo "Testing basic functionality..."
SCRIPT_PATH="$1"
ARGS="-w 800 -h 600 -o test_output.png"

# Используем poetry run python
echo "Running: poetry run python $SCRIPT_PATH $ARGS"
PYTHONPATH=. poetry run python "$SCRIPT_PATH" $ARGS

EXIT_CODE=$?
if [ $EXIT_CODE -eq 0 ]; then
    echo "✓ Application exited successfully"
else
    echo "✗ Application failed with exit code: $EXIT_CODE"
    exit 1
fi

if [ -f "test_output.png" ]; then
    echo "✓ Image file 'test_output.png' was created"
else
    echo "✗ Image file 'test_output.png' was not created"
    exit 1
fi
echo "Basic functionality test passed!"