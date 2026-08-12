# MSE800 - Week 1

Coursework activities for MSE800, Week 1. Additional activities will be added to this repository over time.

## Activities

### Activity 3.1: Develop a Python Project Using Functions

A Python program that takes a number **N** from the user and:

- Prints all Fibonacci values up to N
- Calculates and prints the factorial of N

**File:** `main.py`

**Run:**

```bash
python main.py
```

You'll be prompted to enter a number. Input is validated — non-numeric and negative entries are rejected and re-prompted.

**Example:**

```
Enter a number (N): 10
Fibonacci series up to 10: [0, 1, 1, 2, 3, 5, 8]
Factorial of 10: 3628800
```

**Structure:**

| Function | Purpose |
|----------|---------|
| `fibonacci_series(limit)` | Returns Fibonacci values up to `limit` |
| `factorial(n)` | Returns `n!` |
| `get_valid_number()` | Prompts until valid input is entered |
| `main()` | Runs the program |

### Activity 4: BMI Calculator CLI

A command-line application that takes a user's weight and height and reports their Body Mass Index (BMI) with the corresponding WHO weight category.

**File:** `bmi_calculator.py`

**Run:**

```bash
python bmi_calculator.py
```

You'll be prompted for weight (kg) and height (cm). Input is validated — non-numeric and non-positive entries are re-prompted.

**Example:**

```
=== BMI Calculator ===
Enter your weight in kilograms (kg): 108
Enter your height in centimetres (cm): 178
Your BMI is 34.1 (Obese).
```

**Structure:**

| Function | Purpose |
|----------|---------|
| `get_positive_float(prompt)` | Prompts until a positive number is entered |
| `calculate_bmi(weight_kg, height_m)` | Returns BMI |
| `classify_bmi(bmi)` | Returns the WHO weight category |
| `main()` | Runs the program |

## Requirements

- Python 3.x (standard library only — no external packages)

See `requirements.txt` for dependency details.

## Setup

Using conda:

```bash
conda create --name MSE800 python=3.12
conda activate MSE800
```

## Author

Nick Jones
