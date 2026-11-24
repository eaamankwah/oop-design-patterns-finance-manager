# balance.py
"""
Singleton Pattern
------------------
`Balance` ensures there is exactly one shared source of truth for the
user's net balance across the whole application. Direct instantiation
(`Balance()`) is blocked after the first instance is created; callers
must go through `Balance.get_instance()`.

Observer Pattern (integration point)
-------------------------------------
`Balance` also acts as the Subject in the Observer pattern: observers are
registered via dependency injection (`register_observer`) rather than
being hard-coded, and are notified whenever a transaction is applied.

Decorator Pattern (integration point)
--------------------------------------
`apply_transaction` is wrapped with `validate_transaction` and
`log_transaction` decorators (see transaction/transaction_decorator.py),
layering validation and logging behavior on top of the core balance
update logic without cluttering it.
"""
from transaction.transaction_category import TransactionCategory
from transaction.transaction_decorator import log_transaction, validate_transaction


class Balance:
    """Singleton to track the balance."""

    _instance = None

    def __init__(self):
        """Initialize the balance. Prevent direct instantiation."""
        if Balance._instance is not None:
            raise RuntimeError(
                "Balance is a singleton. Use Balance.get_instance() instead of Balance()."
            )
        self._balance = 0.0
        self._observers = []
        Balance._instance = self

    @classmethod
    def get_instance(cls):
        """Return the single shared Balance instance, creating it if necessary."""
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def reset(self):
        """Reset the net balance to zero and clear registered observers."""
        self._balance = 0.0
        self._observers = []

    # --- Observer registration (constructor/setter-based dependency injection) ---

    def register_observer(self, observer):
        """Register an observer to be notified of balance changes."""
        if observer not in self._observers:
            self._observers.append(observer)

    def unregister_observer(self, observer):
        """Remove a previously registered observer."""
        if observer in self._observers:
            self._observers.remove(observer)

    def _notify_observers(self, transaction):
        """Notify all registered observers of the latest transaction/balance."""
        for observer in self._observers:
            observer.update(self.get_balance(), transaction)

    # --- Core balance operations ---

    def add_income(self, amount):
        """Add income to the balance."""
        self._balance += amount
        return self._balance

    def add_expense(self, amount):
        """Subtract expense from the balance."""
        self._balance -= amount
        return self._balance

    @validate_transaction
    @log_transaction
    def apply_transaction(self, transaction):
        """
        Apply a Transaction object to update the balance.

        Args:
            transaction (Transaction): The transaction to apply.
        """
        if transaction.category == TransactionCategory.INCOME:
            self.add_income(transaction.amount)
        elif transaction.category == TransactionCategory.EXPENSE:
            self.add_expense(transaction.amount)
        else:
            raise ValueError(f"Unknown transaction category: {transaction.category}")

        self._notify_observers(transaction)

    def get_balance(self):
        """Get the current net balance."""
        return self._balance

    def summary(self):
        """Return a summary string of the net balance."""
        return f"Current balance: ${self._balance:.2f}"
