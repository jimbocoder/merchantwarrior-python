import logging
import merchantwarrior as mw
from pprint import pprint

# logging.basicConfig()
# logging.getLogger().setLevel(logging.DEBUG)
# requests_log = logging.getLogger("requests.packages.urllib3")
# requests_log.setLevel(logging.DEBUG)
# requests_log.propagate = True

credentials = mw.ApiCredentials(
    merchant_uuid='57314b72e0624',
    api_key='yxh5l1if',
    api_pass_phrase='ejzzrepf',
)

api = mw.Api(
    credentials=credentials
)

customer = mw.Customer()
customer.name = 'Samir patel'
customer.country = 'au'
customer.state = 'QLD'
customer.city = 'Brisbane'
customer.address = '123 Fake St'
customer.postcode = '4000'
customer.phone = '07 3123 4567'
customer.email = 'john@smith.com'
customer.ip = '127.0.0.1'

transaction = mw.Transaction(
    amount='10.00',
    currency='aud',
    product='Test Product'
)

card = mw.PaymentCard(
    number='5123456789012346',
    name='Samir Patel Card Name',
    expiry='0517'
)

auth_transaction = mw.Transaction(
    amount='6.66',
    currency='aud',
    product='Test Product 420'
)

print "Attempting to process a transaction\n"
response = api.process_card(transaction, customer, card)

if response.success:
    print "\nSuccessfully processed transaction"
    print "Response code: " + response.response_code
    print "Response message: " + response.response_message
    print "Transaction Id: " + str(response.transaction_id)

    print "\nAttempting to query card"
    query_response = api.query_card(transaction)
    print "\nSuccessfully queried card"
    print "Response code: " + query_response.response_code
    print "Response message: " + str(query_response.response_message)

    print "\nAttempting to refund the same transaction by transactionId"
    refund_response = api.refund_card(transaction, transaction.amount)
    print "Successfully refunded transactionId: " + transaction.id
    print "Response code: " + response.response_code
    print "Response message: " + str(refund_response.response_message)
else:
    print "\nAn error occurred while trying to process your transaction"


