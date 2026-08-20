# MSE800 - Week 2: Temperature Converter

Yoobee MSE800, Week 2 coursework.

## Requirements

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

## Files

- `main.py` — entry point: reads a temperature and prints the conversion
- `temperature.py` — `Temperature`, a value on a scale and the conversions between scales
- `temperature_input.py` — `TemperatureInput`, validates and interprets what the user types

## Running

```bash
python main.py
```

## Example

```
Enter a temperature (e.g. F51 or C11): F51
F51 degrees Fahrenheit is converted to 10.56 degrees Celsius
```

```
Enter a temperature (e.g. F51 or C11): X20
Invalid input. Please enter the temperature with the correct 'C' or 'F' prefix.
Enter a temperature (e.g. F51 or C11): C11
C11 degrees Celsius is converted to 51.80 degrees Fahrenheit
```
