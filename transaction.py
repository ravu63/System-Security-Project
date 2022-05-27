import currency

class Transaction:

    def __init__(self, name, email, address, city, state, postalCode):
        self.name = name
        self.email = email
        self.address = address
        self.city = city
        self.state = state
        self.zip = postalCode

    def getName(self):
        return self.name

    def getEmail(self):
        return self.email

    def getAddress(self):
        return self.address

    def getCity(self):
        return self.city

    def getState(self):
        return self.state

    def getZip(self):
        return self.zip

    def getDetails(self):
        message = 'Name: {}\n Email: {} \n Address: {} \n City: {} \n State: {} \n Postal Code: {} \n'\
            .format(self.name, self.email, self.address, self.city, self.state, self.zip)
        return message

    def setName(self, n):
        self.name = n

    def setEmail(self, n):
        self.email = n

    def setAddress(self, n):
        self.address = n

# makes use of superclass transaction
class CustomerPurchase(Transaction):
    def __init__(self, *args, **kwargs):
        Transaction.__init__(self, *args)
        self.amount = kwargs.get('amount')
        self.initial = kwargs.get('initial')
        self.to = kwargs.get('to')
        self.price = kwargs.get('price')
        self.transactionID = kwargs.get('transactionID')

    def __str__(self):
        message = super().getDetails()
        message += str(self.initial) + " to " + str(self.to)
        message += " Price:" + str(self.price) + str(self.initial) + "\n Transaction ID: " + str(self.transactionID)
        return message

    def getPrice(self):
        return self.price

    def getTransactionID(self):
        return self.transactionID

