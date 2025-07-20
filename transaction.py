# Represents a single transaction.
# Validates date format, size, and carrier.
# Provides month key for monthly discount tracking.

from datetime import datetime
from constants import CARRIERS, SIZES, PRICES

class Transaction:
    def __init__(self, date_str, size, carrier, raw_line):
        self.date_str = date_str
        self.size = size
        self.carrier = carrier
        self.raw_line = raw_line
        self.valid = self._validate()
        self.price = PRICES.get(carrier, {}).get(size, None)

    def _validate(self):
        try:
            self.date = datetime.strptime(self.date_str, "%Y-%m-%d")
        except ValueError:
            return False
        return self.size in SIZES and self.carrier in CARRIERS

    def get_month_key(self):
        return self.date.strftime("%Y-%m")
