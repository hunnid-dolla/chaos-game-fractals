#!/bin/sh

echo "Testing image properties..."

# Аргументы для запуска программы
SCRIPT_PATH="$1"
# ИЗМЕНЕНИЕ: Добавлены -s 1000 -i 1000 для скорости
ARGS="-w 800 -h 600 -s 1000 -i 1000 -o test_output.png"

# Генерация тестового изображения, если оно не существует
if [ ! -f "test_output.png" ]; then
    echo "Generating test image..."
    PYTHONPATH=. poetry run python "$SCRIPT_PATH" $ARGS
    # Проверка, была ли генерация успешной
    if [ $? -ne 0 ]; then
        echo "✗ Failed to generate test image"
        exit 1
    fi
fi

# Проверка, существует ли файл
if [ ! -f "test_output.png" ]; then
    echo "✗ Image file 'test_output.png' does not exist"
    exit 1
fi

# Проверка расширения файла
case "test_output.png" in
    *.png)
        echo "✓ Image file has .png extension"
        ;;
    *)
        echo "✗ Image file does not have .png extension"
        exit 1
        ;;
esac

# Проверка, имеет ли файл содержимое (ненулевой размер)
FILE_SIZE=$(stat -c%s "test_output.png" 2>/dev/null || stat -f%z "test_output.png" 2>/dev/null)
if [ "$FILE_SIZE" -gt 0 ]; then
    echo "✓ Image file has content (size: $FILE_SIZE bytes)"
else
    echo "✗ Image file is empty"
    exit 1
fi

# ИЗМЕНЕНИЕ: Проверка сигнатуры PNG через Python (вместо xxd)
# Первые 8 байт PNG: \x89PNG\r\n\x1a\n
IS_PNG=$(python3 -c "with open('test_output.png', 'rb') as f: print(f.read(8) == b'\x89PNG\r\n\x1a\n')")

if [ "$IS_PNG" = "True" ]; then
    echo "✓ Image file has valid PNG signature"
else
    echo "✗ Image file does not have valid PNG signature"
    exit 1
fi

echo "Image properties test passed!"