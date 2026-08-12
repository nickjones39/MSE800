"""
BMI (Body Mass Index) Calculator - Command-Line Interface application.

The user enters their weight (kg) and height (cm); the program calculates
their BMI and reports the corresponding weight category.
"""


def get_positive_float(prompt):
    """Prompt the user until they enter a positive number, then return it."""
    while True:
        entry = input(prompt).strip()
        try:
            value = float(entry)
        except ValueError:
            print("  Please enter a valid number (e.g. 70.5).")
            continue
        if value <= 0:
            print("  Value must be greater than zero.")
            continue
        return value


def calculate_bmi(weight_kg, height_m):
    """Return the BMI for a given weight (kg) and height (m)."""
    return weight_kg / (height_m ** 2)


def classify_bmi(bmi):
    """Return the World Health Organisation weight category for a BMI value."""
    if bmi < 18.5:
        return "Underweight"
    elif bmi < 25:
        return "Normal weight"
    elif bmi < 30:
        return "Overweight"
    else:
        return "Obese"


def main():
    """Run the BMI calculator CLI."""
    print("=== BMI Calculator ===")

    # Gather validated input from the user.
    weight = get_positive_float("Enter your weight in kilograms (kg): ")
    height_cm = get_positive_float("Enter your height in centimetres (cm): ")

    # Convert height to metres, then calculate and classify.
    height_m = height_cm / 100
    bmi = calculate_bmi(weight, height_m)
    category = classify_bmi(bmi)

    # Display the result, rounded to one decimal place.
    print(f"\nYour BMI is {bmi:.1f} ({category}).")


if __name__ == "__main__":
    main()