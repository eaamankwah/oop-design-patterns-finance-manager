import unittest

from balance.balance import Balance
from transaction.transaction import Transaction
from transaction.transaction_category import TransactionCategory
from transaction.transaction_command import ApplyTransactionCommand, TransactionManager


class TestTransactionCommand(unittest.TestCase):

    def setUp(self):
        self.balance = Balance.get_instance()
        self.balance.reset()
        self.manager = TransactionManager()

    def test_execute_applies_transaction(self):
        income = Transaction(100, TransactionCategory.INCOME)
        command = ApplyTransactionCommand(self.balance, income)
        self.manager.execute_command(command)
        self.assertEqual(self.balance.get_balance(), 100)

    def test_undo_reverses_transaction(self):
        income = Transaction(100, TransactionCategory.INCOME)
        command = ApplyTransactionCommand(self.balance, income)
        self.manager.execute_command(command)
        self.manager.undo_last()
        self.assertEqual(self.balance.get_balance(), 0)

    def test_undo_reverses_expense(self):
        expense = Transaction(40, TransactionCategory.EXPENSE)
        command = ApplyTransactionCommand(self.balance, expense)
        self.manager.execute_command(command)
        self.assertEqual(self.balance.get_balance(), -40)
        self.manager.undo_last()
        self.assertEqual(self.balance.get_balance(), 0)

    def test_redo_reapplies_transaction(self):
        income = Transaction(100, TransactionCategory.INCOME)
        command = ApplyTransactionCommand(self.balance, income)
        self.manager.execute_command(command)
        self.manager.undo_last()
        self.manager.redo_last()
        self.assertEqual(self.balance.get_balance(), 100)

    def test_undo_with_no_history_raises(self):
        with self.assertRaises(IndexError):
            self.manager.undo_last()

    def test_redo_with_no_history_raises(self):
        with self.assertRaises(IndexError):
            self.manager.redo_last()

    def test_new_command_clears_redo_stack(self):
        c1 = ApplyTransactionCommand(self.balance, Transaction(100, TransactionCategory.INCOME))
        self.manager.execute_command(c1)
        self.manager.undo_last()

        c2 = ApplyTransactionCommand(self.balance, Transaction(50, TransactionCategory.EXPENSE))
        self.manager.execute_command(c2)

        with self.assertRaises(IndexError):
            self.manager.redo_last()


if __name__ == "__main__":
    unittest.main()
