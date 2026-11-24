import unittest

from budget.budget_strategy import BudgetPlanner, FiftyThirtyTwentyStrategy, ZeroBasedBudgetStrategy


class TestBudgetStrategy(unittest.TestCase):

    def test_fifty_thirty_twenty_allocation(self):
        planner = BudgetPlanner(FiftyThirtyTwentyStrategy())
        result = planner.plan(1000)
        self.assertEqual(result, {"needs": 500.0, "wants": 300.0, "savings": 200.0})

    def test_zero_based_allocation(self):
        strategy = ZeroBasedBudgetStrategy({"rent": 50, "food": 30, "savings": 20})
        planner = BudgetPlanner(strategy)
        result = planner.plan(1000)
        self.assertEqual(result, {"rent": 500.0, "food": 300.0, "savings": 200.0})

    def test_switch_strategy_at_runtime(self):
        planner = BudgetPlanner(FiftyThirtyTwentyStrategy())
        first = planner.plan(1000)
        planner.set_strategy(ZeroBasedBudgetStrategy({"a": 1, "b": 1}))
        second = planner.plan(1000)
        self.assertNotEqual(first, second)

    def test_zero_total_weight_raises(self):
        with self.assertRaises(ValueError):
            ZeroBasedBudgetStrategy({"a": 0, "b": 0})


if __name__ == "__main__":
    unittest.main()
