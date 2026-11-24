# transaction_decorator.py
"""
Decorator Pattern (Standout Enhancement)
-----------------------------------------
Python function decorators are the idiomatic way to implement the classic
Decorator pattern in Python: they wrap a callable, transparently adding
behavior (validation, logging) around it without changing its interface
or the code that calls it.

Here we decorate `Balance.apply_transaction` with two independent,
stackable decorators:

- `validate_transaction`: guards against invalid input before it ever
  reaches the balance.
- `log_transaction`: records what happened, without the core balance
  logic needing to know anything about logging.

Because each decorator only depends on the `Transaction` abstraction
(not on `Balance` internals), they can be reused on any future method
that accepts a `Transaction` as its first argument.
"""
import functools
import logging

from transaction.transaction import Transaction

logger = logging.getLogger("finance_manager")
if not logger.handlers:
    logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")


def validate_transaction(func):
    """Decorator that validates a transaction before it is applied."""

    @functools.wraps(func)
    def wrapper(self, transaction, *args, **kwargs):
        if not isinstance(transaction, Transaction):
            raise TypeError("Expected a Transaction instance.")
        if transaction.amount is None or transaction.amount <= 0:
            raise ValueError("Transaction amount must be a positive number.")
        return func(self, transaction, *args, **kwargs)

    return wrapper


def log_transaction(func):
    """Decorator that logs a transaction before and the resulting balance after."""

    @functools.wraps(func)
    def wrapper(self, transaction, *args, **kwargs):
        logger.info("Applying transaction: %s", transaction)
        result = func(self, transaction, *args, **kwargs)
        logger.info("Balance after transaction: %.2f", self.get_balance())
        return result

    return wrapper
