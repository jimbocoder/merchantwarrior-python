import logging
import merchantwarrior as mw
from pprint import pprint

logging.basicConfig()
logging.getLogger().setLevel(logging.DEBUG)
requests_log = logging.getLogger("requests.packages.urllib3")
requests_log.setLevel(logging.DEBUG)
requests_log.propagate = True

credentials = mw.ApiCredentials(
    merchant_uuid = '57314b72e0624',
    api_key = 'yxh5l1if',
    api_pass_phrase = 'ejzzrepf',
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

transaction.id = '3551-a2b87efc-1955-11e6-960c-0022197fbe29'
# response = api.process_card(transaction, customer, card)
response = api.query_card(transaction)

print "Response message: " + response.response_message + "\n"
print "Response code: " + response.response_code + "\n"


# or api.process_auth()
# or api.query_card()
# or api.refund_card()
