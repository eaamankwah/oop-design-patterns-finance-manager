# budget_strategy.py
"""
Strategy Pattern (Standout Enhancement #2)
--------------------------------------------
Lets the user swap between interchangeable budgeting algorithms
(e.g. "50/30/20 Rule" vs. "Zero-Based Budgeting") at runtime without the
calling code (`BudgetPlanner`) needing to know which one is in use.

Roles:
    Strategy interface -> BudgetStrategy
    Concrete Strategies -> FiftyThirtyTwentyStrategy, ZeroBasedBudgetStrategy
    Context             -> BudgetPlanner
"""
from abc import ABC, abstractmethod


class BudgetStrategy(ABC):
    """Strategy interface for allocating income across budget categories."""

    @abstractmethod
    def allocate(self, income: float) -> dict:
        """Return a dict mapping category name -> allocated amount."""
        raise NotImplementedError


class FiftyThirtyTwentyStrategy(BudgetStrategy):
    """Classic 50% needs / 30% wants / 20% savings split."""

    def allocate(self, income: float) -> dict:
        return {
            "needs": round(income * 0.50, 2),
            "wants": round(income * 0.30, 2),
            "savings": round(income * 0.20, 2),
        }


class ZeroBasedBudgetStrategy(BudgetStrategy):
    """
    Zero-based budgeting: every dollar of income is assigned to a
    user-defined category (by relative weight) until nothing is left over.
    """

    def __init__(self, category_weights: dict):
        total_weight = sum(category_weights.values())
        if total_weight <= 0:
            raise ValueError("Category weights must sum to more than zero.")
        self.category_weights = category_weights
        self._total_weight = total_weight

    def allocate(self, income: float) -> dict:
        return {
            category: round(income * (weight / self._total_weight), 2)
            for category, weight in self.category_weights.items()
        }


class BudgetPlanner:
    """Context that applies a chosen BudgetStrategy to a given income amount."""

    def __init__(self, strategy: BudgetStrategy):
        self._strategy = strategy

    def set_strategy(self, strategy: BudgetStrategy):
        """Swap the active budgeting strategy at runtime."""
        self._strategy = strategy

    def plan(self, income: float) -> dict:
        """Delegate the allocation to the currently active strategy."""
        return self._strategy.allocate(income)
