# Rule 3: Enforce €10/month discount cap and partial discounting when exceeded.
# Manages applying discount rules to transactions.

from constants import MAX_MONTHLY_DISCOUNT

class DiscountRules:
    def __init__(self, rules):
        self.rules = rules
        self.monthly_discounts = {}

    def apply_discounts(self, transaction):
        original_price = transaction.price
        month = transaction.get_month_key()

        # Remaining discount available this month
        discount_left = MAX_MONTHLY_DISCOUNT - self.monthly_discounts.get(month, 0.0)
        total_discount = 0.0

        # Apply each rule respecting the discount cap
        for rule in self.rules:
            if discount_left <= 0:
                break 

            rule_discount = rule.apply(transaction, self)

            if rule_discount:
                allowed_discount = min(rule_discount, discount_left)

                total_discount += allowed_discount
                discount_left -= allowed_discount

        self.monthly_discounts[month] = self.monthly_discounts.get(month, 0.0) + total_discount

        final_price = original_price - total_discount

        discount_value = round(total_discount, 2) if total_discount > 0 else None
        return round(final_price, 2), discount_value
