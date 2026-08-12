"""The TemperatureInput class: validates and interprets what the user types."""

from temperature import Temperature


class TemperatureInput:
    """Turns raw text such as 'F51' or 'C11' into a Temperature object."""

    PROMPT = "Enter a temperature (e.g. F51 or C11): "
    ERROR = ("Invalid input. Please enter the temperature with the "
             "correct 'C' or 'F' prefix.")

    @staticmethod
    def parse(text):
        """Return a Temperature for valid text, or None if the text is invalid."""
        text = text.strip()
        if len(text) < 2:
            return None

        prefix = text[0]
        number = text[1:]
        if prefix not in Temperature.SCALE_NAMES:
            return None

        try:
            value = float(number)
        except ValueError:
            return None

        return Temperature(value, prefix)

    def read(self):
        """Keep prompting until the user types a valid temperature."""
        while True:
            temperature = self.parse(input(self.PROMPT))
            if temperature is not None:
                return temperature
            print(self.ERROR)
