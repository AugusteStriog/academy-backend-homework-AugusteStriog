import unittest
from transaction import Transaction
from discount_rules import DiscountRules
from rules.small_package import SmallPackageDiscountRules
from rules.third_large_lp import ThirdLargeLPFreeRules

class TestDiscountRules(unittest.TestCase):
    # Test that small MR package gets correct discount to match lowest S price
    def test_small_package_discount(self):
        t = Transaction("2025-07-01", "S", "MR", "")
        mgr = DiscountRules([SmallPackageDiscountRules()])
        price, discount = mgr.apply_discounts(t)
        self.assertEqual(price, 1.50)
        self.assertEqual(discount, 0.50)

    # Test that every third large LP shipment per month is free
    def test_third_large_lp_free(self):
        mgr = DiscountRules([ThirdLargeLPFreeRules()])
        ts = [Transaction(f"2025-07-0{i}", "L", "LP", "") for i in range(1, 5)]
        _, d1 = mgr.apply_discounts(ts[0])
        _, d2 = mgr.apply_discounts(ts[1])
        price3, d3 = mgr.apply_discounts(ts[2])
        _, d4 = mgr.apply_discounts(ts[3])

        self.assertIsNone(d1)
        self.assertIsNone(d2)
        self.assertEqual(price3, 0.00)
        self.assertEqual(d3, 6.90)
        self.assertIsNone(d4)

    # Test that monthly discount cap of 10.0 is not exceeded
    def test_discount_cap_enforced(self):
        mgr = DiscountRules([SmallPackageDiscountRules(), ThirdLargeLPFreeRules()])
        shipments = []
        for i in range(1, 21):
            shipments.append(Transaction(f"2025-07-{i:02d}", "S", "MR", ""))
        shipments.append(Transaction("2025-07-21", "L", "LP", ""))
        shipments.append(Transaction("2025-07-22", "L", "LP", ""))
        shipments.append(Transaction("2025-07-23", "L", "LP", ""))

        discounts = []
        for t in shipments:
            _, discount = mgr.apply_discounts(t)
            discounts.append(discount if discount is not None else 0.0)

        self.assertAlmostEqual(sum(discounts[:20]), 10.0)
        self.assertEqual(discounts[22], 0.0)

    # Test that discount is partially applied when cap is nearly reached
    def test_full_discount_and_partial_cap(self):
        mgr = DiscountRules([SmallPackageDiscountRules(), ThirdLargeLPFreeRules()])
        for i in range(1, 20):
            t = Transaction(f"2025-07-{i:02d}", "S", "MR", "")
            price, discount = mgr.apply_discounts(t)
            self.assertAlmostEqual(discount, 0.50)

        t1 = Transaction("2025-07-20", "L", "LP", "")
        _, d1 = mgr.apply_discounts(t1)
        self.assertIsNone(d1)

        t2 = Transaction("2025-07-21", "L", "LP", "")
        _, d2 = mgr.apply_discounts(t2)
        self.assertIsNone(d2)

        t3 = Transaction("2025-07-22", "L", "LP", "")
        price3, d3 = mgr.apply_discounts(t3)
        self.assertLess(d3, 6.90)
        self.assertAlmostEqual(d3, 0.5)
        self.assertAlmostEqual(price3, 6.90 - 0.5)

    # Test that transactions with invalid date formats are rejected
    def test_invalid_transaction_package_size(self):
        tx = Transaction("2025-07-01", "X", "LP", "2025-07-01 X LP")
        self.assertFalse(tx.valid)



if __name__ == '__main__':
    unittest.main()
