class Revenue:
    def __init__(self, month: str, revenue: int) -> None:
        self.month = month
        self.revenue = revenue

    def dict(self):
        return {
            'month': self.month,
            'revenue': self.revenue
        }
    