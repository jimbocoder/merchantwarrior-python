
class Transaction(object):

    amount = None
    currency = None
    product = None
    id = None
    reference_id = None

    def __init__(self, amount, currency, product, id = None, reference_id = None):
        self.amount = amount
        self.currency = currency
        self.product = product
        self.id = id
        self.reference_id = reference_id


