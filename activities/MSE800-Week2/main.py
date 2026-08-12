"""
Temperature converter

For this project, I want to build a temperature converter that transforms user-entered
temperatures between Fahrenheit and Celsius. The input for Fahrenheit temperatures should start
with an uppercase 'F', and for Celsius, it should start with an uppercase 'C'. Hence, the project
needs to include validation and interpretation of user input.

If the input is in Fahrenheit (e.g., 'F51'), the program should convert it to Celsius, rounding to two
decimal places, and output: "F51 degrees Fahrenheit is converted to XX.XX degrees Celsius",
where 'XX.XX' is the converted temperature value. Conversely, if the input is in Celsius (e.g.,
'C11'), the program should convert it to Fahrenheit, rounding to two decimal places, and output:
"C11 degrees Celsius is converted to YY.YY degrees Fahrenheit", where 'YY.YY' is the converted
temperature value.

Should the user enter an incorrect format or use the wrong prefix, the program should prompt
them with: "Invalid input. Please enter the temperature with the correct 'C' or F' prefix."

"""

from temperature_input import TemperatureInput


def main():
    reader = TemperatureInput()
    temperature = reader.read()
    print(temperature.describe_conversion())


if __name__ == "__main__":
    main()
