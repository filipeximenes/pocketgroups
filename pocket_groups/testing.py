
from pocket import Pocket

CONSUMER_KEY = '23164-b47989d85aed08155b27063d'


request_token = Pocket.get_request_token(consumer_key=CONSUMER_KEY, redirect_uri='/')
auth_url = Pocket.get_auth_url(code=request_token, redirect_uri='/')

print auth_url
