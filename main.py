"""This module serves as the entry point for the program."""
from balance.balance import Balance
from balance.balance_observer import LowBalanceAlertObserver, PrintObserver
from budget.budget_strategy import (
    BudgetPlanner,
    FiftyThirtyTwentyStrategy,
    ZeroBasedBudgetStrategy,
)
from transaction.external_income_transaction import ExternalFreelanceIncome
from transaction.transaction import Transaction
from transaction.transaction_adapter import TransactionAdapter
from transaction.transaction_category import TransactionCategory
from transaction.transaction_command import ApplyTransactionCommand, TransactionManager


def main():
    print("=" * 60)
    print("Freelancer Personal Finance Manager")
    print("=" * 60)

    # --- Singleton: one Balance instance shared across the whole app ---
    balance = Balance.get_instance()
    balance.reset()

    # --- Observer: register observers via dependency injection ---
    print_observer = PrintObserver()
    low_balance_observer = LowBalanceAlertObserver(threshold=100)
    balance.register_observer(print_observer)
    balance.register_observer(low_balance_observer)

    # --- Command: invoker that lets us execute/undo/redo transactions ---
    manager = TransactionManager()

    print("\nAdding transactions...")

    # Create standard transactions
    transactions = [
        Transaction(100, TransactionCategory.INCOME),
        Transaction(50, TransactionCategory.EXPENSE),
        Transaction(200, TransactionCategory.INCOME),
        Transaction(75, TransactionCategory.EXPENSE),
    ]

    # Create an external income transaction (via Adapter pattern)
    freelance_income = ExternalFreelanceIncome(1200, "INV-98765", "Mobile App Project")
    adapter = TransactionAdapter(freelance_income)
    adapted_transaction = adapter.to_transaction()

    all_transactions = transactions + [adapted_transaction]

    # Apply all transactions to balance through Command objects
    for txn in all_transactions:
        manager.execute_command(ApplyTransactionCommand(balance, txn))

    print(f"\n{balance.summary()}")

    # --- Demonstrate Command pattern: undo / redo ---
    print("\n--- Undo/Redo demo (Command pattern) ---")
    print("Undoing last transaction...")
    manager.undo_last()
    print(balance.summary())

    print("Redoing last transaction...")
    manager.redo_last()
    print(balance.summary())

    # --- Trigger the low balance alert on purpose ---
    print("\n--- Low balance alert demo (Observer pattern) ---")
    manager.execute_command(
        ApplyTransactionCommand(balance, Transaction(1400, TransactionCategory.EXPENSE))
    )
    print(balance.summary())

    # --- Demonstrate Strategy pattern: budget planning ---
    print("\n--- Budget planning demo (Strategy pattern) ---")
    income_total = 3000
    planner = BudgetPlanner(FiftyThirtyTwentyStrategy())
    print(f"50/30/20 plan for ${income_total}: {planner.plan(income_total)}")

    planner.set_strategy(
        ZeroBasedBudgetStrategy({"rent": 40, "food": 20, "savings": 20, "fun": 20})
    )
    print(f"Zero-based plan for ${income_total}: {planner.plan(income_total)}")

    print(f"\nFinal {balance.summary()}")


if __name__ == "__main__":
    main()
