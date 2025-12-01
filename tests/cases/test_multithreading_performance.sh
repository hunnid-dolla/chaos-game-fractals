#!/bin/sh
echo "Testing multithreading performance..."

measure_time() {
    threads=$1
    output_file="test_output_${threads}_threads.png"
    echo "Running with $threads threads..."

    START_TIME=$(date +%s)
    # Используем poetry run python
    PYTHONPATH=. poetry run python "$PYTHON_PATH" -w 1920 -h 1080 -t "$threads" -o "$output_file"
    EXIT_CODE=$?
    END_TIME=$(date +%s)

    DURATION=$((END_TIME - START_TIME))
    if [ $EXIT_CODE -eq 0 ]; then
        echo "✓ Completed with $threads threads in ${DURATION} seconds"
        echo "$threads,$DURATION" >> performance_results.csv
        return 0
    else
        echo "✗ Failed with $threads threads (exit code: $EXIT_CODE)"
        return 1
    fi
}

if [ -z "$1" ]; then
    echo "✗ python file path not provided."
    exit 1
fi
PYTHON_PATH="$1"

if [ ! -f "$PYTHON_PATH" ]; then
    echo "✗ python file '$PYTHON_PATH' does not exist."
    exit 1
fi

echo "threads,duration_seconds" > performance_results.csv

for threads in 1 2 4; do
    if ! measure_time "$threads"; then
        echo "Performance test failed for $threads threads"
        exit 1
    fi
done

echo ""
echo "Performance test results:"
cat performance_results.csv
echo ""
echo "Multithreading performance test completed!"