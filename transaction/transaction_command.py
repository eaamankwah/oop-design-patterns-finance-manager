# transaction_command.py
"""
Command Pattern (4th Required Pattern / Standout Enhancement #1)
-------------------------------------------------------------------
Encapsulates "apply a transaction" as an object (`ApplyTransactionCommand`)
rather than a direct method call. This decouples the invoker
(`TransactionManager`) from the receiver (`Balance`), and — because each
command knows how to reverse itself — makes Undo/Redo possible without
Balance ever needing to know about command history.

Roles:
    Command interface -> Command
    Concrete Command   -> ApplyTransactionCommand
    Receiver           -> Balance (injected into the command)
    Invoker            -> TransactionManager
"""
from abc import ABC, abstractmethod

from transaction.transaction import Transaction
from transaction.transaction_category import TransactionCategory


class Command(ABC):
    """Command interface declaring execute and undo operations."""

    @abstractmethod
    def execute(self):
        raise NotImplementedError

    @abstractmethod
    def undo(self):
        raise NotImplementedError


class ApplyTransactionCommand(Command):
    """Encapsulates applying (and reversing) a single transaction on a Balance."""

    def __init__(self, balance, transaction: Transaction):
        self.balance = balance
        self.transaction = transaction

    def execute(self):
        """Apply the transaction to the balance."""
        self.balance.apply_transaction(self.transaction)

    def undo(self):
        """Reverse the transaction by applying its inverse."""
        inverse_category = (
            TransactionCategory.EXPENSE
            if self.transaction.category == TransactionCategory.INCOME
            else TransactionCategory.INCOME
        )
        inverse_transaction = Transaction(self.transaction.amount, inverse_category)
        self.balance.apply_transaction(inverse_transaction)


class TransactionManager:
    """Invoker: executes commands and maintains history for undo/redo."""

    def __init__(self):
        self._history = []
        self._redo_stack = []

    def execute_command(self, command: Command):
        """Execute a command and record it in history, clearing any redo state."""
        command.execute()
        self._history.append(command)
        self._redo_stack.clear()

    def undo_last(self):
        """Undo the most recently executed command."""
        if not self._history:
            raise IndexError("No transactions to undo.")
        command = self._history.pop()
        command.undo()
        self._redo_stack.append(command)
        return command

    def redo_last(self):
        """Re-apply the most recently undone command."""
        if not self._redo_stack:
            raise IndexError("No transactions to redo.")
        command = self._redo_stack.pop()
        command.execute()
        self._history.append(command)
        return command

    def has_history(self):
        """Whether there is at least one applied command."""
        return bool(self._history)
