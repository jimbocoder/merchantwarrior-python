
class PaymentCard(object):

    number = None
    name = None
    expiry = None

    def __init__(self, number, name, expiry):
        self.name = name
        self.number = number
        self.expiry = expiry
