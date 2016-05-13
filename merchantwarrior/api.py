import requests
import hashlib
from pprint import pprint
from response import Response


class Api(object):
    """The main interface to make API requests and parse responses
    """
    ENDPOINT = 'https://base.merchantwarrior.com/post/'

    transaction = None

    def __init__(self, credentials):
        self.credentials = credentials

    def request(self, method, url, headers={}, post_data=None):
        kwargs = {}
        result = requests.request(method,
                                  url,
                                  headers=headers,
                                  data=post_data,
                                  timeout=80,
                                  **kwargs)

        return result.content, result.status_code, result.headers


    def construct_process_card_post_data(self, credentials, transaction, customer, payment_card):
        post_data = {
            'method': 'processCard',
            'merchantUUID': credentials.merchant_uuid,
            'apiKey': credentials.api_key,
            'transactionAmount': transaction.amount,
            'transactionCurrency': transaction.currency,
            'transactionProduct': transaction.product,
            'customerName': customer.name,
            'customerCountry': customer.country,
            'customerState': customer.state,
            'customerCity': customer.city,
            'customerAddress': customer.address,
            'customerPostCode': customer.postcode,
            'customerPhone': customer.phone,
            'customerEmail': customer.email,
            'customerIP': customer.ip,
            'paymentCardNumber': payment_card.number,
            'paymentCardName': payment_card.name,
            'paymentCardExpiry': payment_card.expiry,
        }
        post_data['hash'] = self.calculate_hash(post_data)
        return post_data


    def process_card(self, transaction, customer, payment_card):
        self.transaction = transaction
        post_data = self.construct_process_card_post_data(self.credentials, transaction, customer, payment_card)
        return self.send_post_data(post_data)

    def send_post_data(self, post_data):
        xml_result = self.request('POST', self.ENDPOINT, [], post_data)

        if xml_result:
            xml_result = xml_result[0]
            response = Response(xml_result)

            # If we have a successful response, set the transactionId on the transaction object
            # This will get used for refunds and other operations against the transaction
            if response.success and response.transaction_id:
                self.transaction.id = response.transaction_id

            return response
        else:
            raise Exception('No response from MW while trying to process card')


    def construct_process_auth_post_data(self, credentials, transaction, customer, payment_card):
        post_data = {
            'method': 'processAuth',
            'merchantUUID': credentials.merchant_uuid,
            'apiKey': credentials.api_key,
            'transactionAmount': transaction.amount,
            'transactionCurrency': transaction.currency,
            'transactionProduct': transaction.product,
            'customerName': customer.name,
            'customerCountry': customer.country,
            'customerState': customer.state,
            'customerCity': customer.city,
            'customerAddress': customer.address,
            'customerPostCode': customer.postcode,
            'customerPhone': customer.phone,
            'customerEmail': customer.email,
            'customerIP': customer.ip,
            'paymentCardNumber': payment_card.number,
            'paymentCardName': payment_card.name,
            'paymentCardExpiry': payment_card.expiry,
        }
        post_data['hash'] = self.calculate_hash(post_data)
        return post_data


    def process_auth(self, transaction, customer, payment_card):
        post_data = self.construct_process_auth_post_data(self.credentials, transaction, customer, payment_card)
        return self.send_post_data(post_data)


    def construct_query_card_post_data(self, credentials, transaction):
        post_data = {
            'method': 'queryCard',
            'merchantUUID': credentials.merchant_uuid,
            'apiKey': credentials.api_key,
        }

        if not transaction.id and not transaction.reference_id:
            raise InvalidShit()
        else:
            if transaction.id:
                post_data['transactionID'] = transaction.id
            if transaction.reference_id:
                post_data['transactionReferenceID'] = transaction.reference_id
        post_data['hash'] = self.calculate_hash(post_data, type='query')
        return post_data

    def query_card(self, transaction):
        post_data = self.construct_query_card_post_data(self.credentials, transaction)
        return self.send_post_data(post_data)


    def construct_refund_card_post_data(self, credentials, transaction, refund_amount):
        post_data = {
            'method': 'refundCard',
            'merchantUUID': credentials.merchant_uuid,
            'apiKey': credentials.api_key,
            'transactionAmount': transaction.amount,
            'transactionCurrency': transaction.currency,
            'transactionID': transaction.id,
            'transactionReferenceID': transaction.reference_id,
            'refundAmount': refund_amount,
        }
        post_data['hash'] = self.calculate_hash(post_data)
        return post_data


    def refund_card(self, transaction, refund_amount):
        post_data = self.construct_refund_card_post_data(self.credentials, transaction, refund_amount)
        return self.send_post_data(post_data)

    def calculate_hash(self, post_data, type='transaction'):
        if type == 'transaction':
            hash_fields = [self.credentials.api_pass_phrase,
                           post_data['merchantUUID'],
                           post_data['transactionAmount'],
                           post_data['transactionCurrency']
            ]
        elif type == 'query':
            hash_fields = [self.credentials.api_pass_phrase,
                           post_data['merchantUUID'],
                           post_data.get('transactionID') or post_data.get('transactionReferenceID'),
            ]
        else:
            raise InvalidHashType()
        return hashlib.md5(''.join(hash_fields).lower()).hexdigest()

