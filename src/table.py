from seat import Seat


class Table:
    """
    Class representing a blackjack table.

    Attributes:
    - seats (list): A list of Seat objects representing the seats at the table.
    """

    def __init__(self):
        """
        Initializes a blackjack table with no seats.
        """
        self.seats: list[Seat] = []

    def add_seat(self, seat):
        """
        Adds a seat to the table.

        Args:
        - seat (Seat): The Seat object to add to the table.
        """
        if len(self.seats) < 7:
            self.seats.append(seat)
        else:
            print("The table is full. Cannot add more seats.")

    def __str__(self):
        """
        Returns a string representation of the table (list of seat strings).
        """
        table_info = f"Table Object: Contains {len(self.seats)} seats\n"
        seat_info = ""
        for idx, seat in enumerate(self.seats, start=1):
            seat_info += f" - Seat {idx}: {str(seat)}\n"
        return table_info + seat_info

    def __repr__(self):
        """
        Returns a string representation of the table for debugging purposes.
        """
        return f"Table(seats={self.seats})"
