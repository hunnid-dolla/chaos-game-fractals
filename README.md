# Описание

Реализован генератор изображений фрактального пламени (Fractal Flame) на основе алгоритма Chaos Game. Программа визуализирует математическую красоту систем итерируемых функций (IFS), используя современные методы рендеринга и оптимизации производительности.

# Функциональность

+ **Генерация и математика**:
  * Реализован алгоритм Chaos Game с поддержкой цветной генерации.
  * Поддержка 5 математических трансформаций: `linear`, `sinusoidal`, `spherical`, `swirl`, `horseshoe`.
  * Применение аффинных преобразований (сжатие, вращение, сдвиг).
+ **Настройка и конфигурация**:
  * Гибкая настройка через CLI аргументы или JSON-файл.
  * Валидация входных данных с помощью `pydantic`.
  * Возможность задавать собственные аффинные коэффициенты или генерировать их случайно.
+ **Рендеринг и постобработка**:
  * Логарифмическая гамма-коррекция для достижения эффекта "свечения" на черном фоне.
  * Поддержка симметрии (вращательная симметрия) для создания мандал и снежинок.
  * Сохранение результата в формате PNG (RGB, 8 бит на канал).

# Техническая реализация

+ **Производительность**:
  * **Векторизация**: Логика рендеринга полностью переписана на `numpy`, что обеспечило ускорение вычислений в десятки раз.
  * **Многопоточность**: Использование `ProcessPoolExecutor` для параллельной генерации фрактала на всех ядрах процессора.
  * Эффективная работа с памятью через прямую запись в массивы данных.
+ **Архитектура**:
  * Разделение ответственности: `core`, `renderer`, `transformations`, `image_processor`.
  * Использование `dataclasses` и строгая типизация.
+ **Качество кода**: Соблюдение style-guide (ruff, black, isort), прохождение CI/CD пайплайна.
+ **Тестирование**:
  * Unit-тесты для математики трансформаций и логики конфигурации.
  * Интеграционные (Black Box) тесты производительности и корректности вывода.

# Запуск

* Быстрый запуск с параметрами: `poetry run python -m src.main -s 100000 -i 5000 -t 4 -f swirl:1.0,horseshoe:0.5 -o flame.png`
* Запуск через конфиг файл: `poetry run python -m src.main --config config.json --output-path result.png`

Пример JSON конфигурации:
```json
{
  "size": {"width": 1920, "height": 1080},
  "iteration_count": 25000,
  "samples": 1000000,
  "threads": 4,
  "gamma": 2.2,
  "symmetry_level": 3,
  "functions": [{"name": "swirl", "weight": 1.0}]
}
```

#### Какие дополнительные задания выполнены?

- [x] реализовано 5 и более трансформаций (linear, sinusoidal, spherical, swirl, horseshoe)
- [x] реализована поддержка логарифмической гамма-коррекции (параметры `--gamma`, `--gamma-correction`)
- [x] добавлена поддержка симметрии в генерации пламени (параметр `--symmetry`)

#### Скриншоты с примерами работы программы

+ Пример генерации "Галактики"

Команда:
`poetry run python -m src.main -s 200000 -i 5000 -t 4 --symmetry 3 -f swirl:1.0,horseshoe:0.5 -o galaxy_final.png`

<img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/36919389-7726-4bb3-92c5-cdcef6e8678d" />

+ Пример генерации "Неонового цветка" 

Команда:
`poetry run python -m src.main --config neon.json --output-path neon.png`

neon.json:
```json
  {
  "size": {
    "width": 1920,
    "height": 1080
  },
  "iteration_count": 5000,
  "samples": 300000,
  "threads": 4,
  "gamma": 3.0,
  "symmetry_level": 6,
  "seed": 333,
  "functions": [
    { "name": "sinusoidal", "weight": 2.0 },
    { "name": "swirl", "weight": 0.5 }
  ]
}
```
<img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/d1e7b2c5-0bcf-4334-b665-21f42a37bcdd" />

+ Пример генерации "Космоса" 

Команда:
`poetry run python -m src.main --config nebula.json --seed 777 -o space_2.png`

<img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/0fca2dfc-c9ec-4090-a4fa-cba746d76c2c" />
