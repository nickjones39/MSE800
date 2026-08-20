"""The Temperature class: a value on a scale, and the conversions between scales."""


class Temperature:
    """A temperature value on either the Celsius or the Fahrenheit scale."""

    CELSIUS = "C"
    FAHRENHEIT = "F"
    SCALE_NAMES = {CELSIUS: "Celsius", FAHRENHEIT: "Fahrenheit"}

    def __init__(self, value, scale):
        if scale not in self.SCALE_NAMES:
            raise ValueError(f"Unknown scale: {scale!r}")
        self.value = float(value)
        self.scale = scale

    @property
    def scale_name(self):
        """The full name of this scale, e.g. 'Celsius'."""
        return self.SCALE_NAMES[self.scale]

    @property
    def label(self):
        """The temperature written the way the user types it, e.g. 'F51'."""
        return f"{self.scale}{self.value:g}"

    def to_celsius(self):
        """This temperature as a number of degrees Celsius."""
        if self.scale == self.CELSIUS:
            return self.value
        return (self.value - 32) * 5 / 9

    def to_fahrenheit(self):
        """This temperature as a number of degrees Fahrenheit."""
        if self.scale == self.FAHRENHEIT:
            return self.value
        return self.value * 9 / 5 + 32

    def converted(self):
        """A new Temperature holding the same reading on the other scale."""
        if self.scale == self.CELSIUS:
            return Temperature(self.to_fahrenheit(), self.FAHRENHEIT)
        return Temperature(self.to_celsius(), self.CELSIUS)

    def describe_conversion(self):
        """The sentence the program prints, rounded to two decimal places."""
        other = self.converted()
        return (f"{self.label} degrees {self.scale_name} is converted to "
                f"{other.value:.2f} degrees {other.scale_name}")

    def __str__(self):
        return f"{self.value:.2f} degrees {self.scale_name}"
