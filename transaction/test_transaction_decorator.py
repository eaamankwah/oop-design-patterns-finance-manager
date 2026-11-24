import unittest

from balance.balance import Balance
from transaction.transaction import Transaction
from transaction.transaction_category import TransactionCategory


class TestTransactionDecorator(unittest.TestCase):

    def setUp(self):
        self.balance = Balance.get_instance()
        self.balance.reset()

    def test_negative_amount_rejected(self):
        with self.assertRaises(ValueError):
            self.balance.apply_transaction(Transaction(-10, TransactionCategory.EXPENSE))

    def test_zero_amount_rejected(self):
        with self.assertRaises(ValueError):
            self.balance.apply_transaction(Transaction(0, TransactionCategory.INCOME))

    def test_non_transaction_rejected(self):
        with self.assertRaises(TypeError):
            self.balance.apply_transaction("not a transaction")

    def test_valid_transaction_still_applied(self):
        self.balance.apply_transaction(Transaction(25, TransactionCategory.INCOME))
        self.assertEqual(self.balance.get_balance(), 25)

    def test_invalid_transaction_does_not_change_balance(self):
        with self.assertRaises(ValueError):
            self.balance.apply_transaction(Transaction(-5, TransactionCategory.EXPENSE))
        self.assertEqual(self.balance.get_balance(), 0)


if __name__ == "__main__":
    unittest.main()
