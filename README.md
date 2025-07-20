# Vinted Shipping Discount Calculator

Calculates shipping discounts for Vinted transactions based on defined rules.

**Python version:** 3.13.5

---

## Files

- **main.py** - Runs the program: reads input file, processes transactions, applies discounts, prints results.  
- **transaction.py** - Represents and validates each shipment transaction.  
- **discount_manager.py** - Manages discount application and enforces monthly discount caps.  
- **rules/base.py** - Abstract base class for discount rules.  
- **rules/small_package.py** - Rule: All small shipments get the lowest small package price discount.  
- **rules/third_large_lp.py** - Rule: The third large LP shipment each month is free once per month.  
- **constants.py** - Defines carriers, package sizes, prices, and max monthly discount.  
- **constants.py** - Unit tests.

---

## Usage

Run the program:

```bash
python3 main.py

Run the test:

```bash
python3 -m unittest discover -s tests