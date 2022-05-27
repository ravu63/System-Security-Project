class Currency:
    def __init__(self, amount, initial, to, *args):
        super().__init__(*args)
        self.amount = amount
        self.initial = initial
        self.to = to

    def getInitial(self):
        return self.initial

    def getTo(self):
        return self.to

    def getAmount(self):
        return self.amount



