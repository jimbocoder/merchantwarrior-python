
class ApiCredentials(object):

    merchant_uuid = None
    api_key = None
    api_pass_phrase = None

    def __init__(self, merchant_uuid, api_key, api_pass_phrase):
        self.merchant_uuid = merchant_uuid
        self.api_key = api_key
        self.api_pass_phrase = api_pass_phrase

