import xmltodict
from pprint import pprint


class Response(object):
    """
    Accept a response from MW and assign it to local properties
    """
    success = False
    response_code = None
    response_message = None
    transaction_id = None
    auth_code = None
    auth_message = None
    receipt_no = None
    auth_response_code = None
    auth_settled_date = None
    custom_hash = None

    def __init__(self, raw_xml):

        if raw_xml:
            xml_dict = xmltodict.parse(raw_xml)
            if xml_dict['mwResponse']:

                response = xml_dict['mwResponse']
                self.response_code = response['responseCode']

                if self.response_code == '0':

                    self.response_message = response['responseMessage']
                    self.transaction_id = response['transactionID']
                    self.auth_code = response['authCode']
                    self.auth_message = response['authMessage']
                    self.receipt_no = response['receiptNo']
                    self.auth_response_code = response['authResponseCode']
                    self.auth_settled_date = response['authSettledDate']
                    self.custom_hash = response['customHash']
                    self.success = True
                else:
                    self.success = False
                    self.response_code = response['responseCode']
                    self.response_message = response['responseMessage']
            else:
                raise Exception('No mwResponse node found in response from API')
        else:
            raise Exception('No response from MW API')

    def __str__(self):

        return "\n".join("%s: %s" % item for item in vars(self).items())
