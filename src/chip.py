class Chip:
    """
    Class representing a chip used in a casino.

    Attributes:
    - value (int): The value of the chip.
    """

    def __init__(self, value):
        """
        Initializes a chip with a given value.

        Args:
        - value (int): The value of the chip.
        """
        self.value = value

    def get_value(self):
        """
        Returns the value of the chip.
        """
        return self.value

    def __str__(self):
        """
        Returns a string representation of the chip.
        """
        return f"Chip(value={self.value})"
