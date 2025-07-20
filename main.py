# Reads transactions from input file, validates, applies discounts,
# and prints results in required format.

from transaction import Transaction
from discount_rules import DiscountRules
from rules.small_package import SmallPackageDiscountRules
from rules.third_large_lp import ThirdLargeLPFreeRules
import sys

def process_line(line: str, discount_rules: DiscountRules):
    line = line.strip()
    if not line:
        return
    parts = line.split()
    if len(parts) != 3:
        print(f"{line} Ignored")
        return
    date_str, size, carrier = parts
    transaction = Transaction(date_str, size, carrier, line)
    if not transaction.valid:
        print(f"{line} Ignored")
        return

    final_price, discount = discount_rules.apply_discounts(transaction)
    if final_price is None:
        print(f"{line} Ignored")
        return

    discount_str = f"{discount:.2f}" if discount is not None else '-' 
    print(f"{date_str} {size} {carrier} {final_price:.2f} {discount_str}")

def main(input_file='input.txt'):
    rules = [SmallPackageDiscountRules(), ThirdLargeLPFreeRules()]
    discount_rules = DiscountRules(rules)
    try:
        with open(input_file, 'r') as f:
            for line in f:
                process_line(line, discount_rules)
    except FileNotFoundError:
        print(f"Input file '{input_file}' not found.", file=sys.stderr)

if __name__ == "__main__":
    main()
