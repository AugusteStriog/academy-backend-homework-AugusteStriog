# Rule 2: The third 'L' shipment via 'LP' is free, once per calendar month.

from rules.base import DiscountRules
from collections import defaultdict

class ThirdLargeLPFreeRules(DiscountRules):
    def __init__(self):
        # Tracks count of 'L' LP shipments per month
        self.lp_large_counts = defaultdict(int)
        # Months where free discount was given

        self.free_given = set()

    def apply(self, transaction, discount_manager):
        if transaction.size != 'L' or transaction.carrier != 'LP':
            return 0.0

        month = transaction.get_month_key()
        key = (month, transaction.carrier)
        self.lp_large_counts[key] += 1

        # Give free discount on 3rd shipment only once per month
        if self.lp_large_counts[key] == 3 and month not in self.free_given:
            self.free_given.add(month)
            return transaction.price
        return 0.0
