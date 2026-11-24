# balance_observer.py
"""
Observer Pattern
-----------------
`Balance` is the Subject; anything implementing `IBalanceObserver` can be
registered (dependency injection via `register_observer`) to be notified
whenever a transaction is applied — decoupling "what happens when the
balance changes" from the balance-tracking logic itself.
"""


class IBalanceObserver:
    """Observer interface. Any concrete observer must implement `update`."""

    def update(self, balance, transaction):
        """Handle balance updates."""
        raise NotImplementedError("Subclasses must implement update method.")


class PrintObserver(IBalanceObserver):
    """Prints a message whenever a transaction changes the balance."""

    def update(self, balance, transaction):
        """Print balance update message."""
        print(f"[Balance Update] Applied {transaction} -> New balance: ${balance:.2f}")


class LowBalanceAlertObserver(IBalanceObserver):
    """Triggers an alert whenever the balance falls below a defined threshold."""

    def __init__(self, threshold):
        self.threshold = threshold
        self.alert_triggered = False

    def update(self, balance, transaction):
        """Alert if balance drops below threshold."""
        if balance < self.threshold:
            self.alert_triggered = True
            print(
                f"[ALERT] Balance ${balance:.2f} has fallen below "
                f"threshold ${self.threshold:.2f}!"
            )
        else:
            self.alert_triggered = False
