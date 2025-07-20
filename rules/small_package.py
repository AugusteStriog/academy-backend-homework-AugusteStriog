# Rule 1: All 'S' shipments should always match the lowest 'S' package price among providers.

from rules.base import DiscountRules
from constants import PRICES

class SmallPackageDiscountRules(DiscountRules):
    def apply(self, transaction, discount_manager):
        if transaction.size != 'S':
            return 0.0
        # Find lowest price for 'S' size across carriers
        lowest_price = min(PRICES[carrier]['S'] for carrier in PRICES if 'S' in PRICES[carrier])
        # Calculate the difference between transaction price and lowest price
        return max(0.0, transaction.price - lowest_price)
