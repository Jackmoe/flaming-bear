# New XML URL
# http://www1.toronto.ca/fire/livecad.xml?

import requests
import re
from lxml import etree
import gc
from geopy.geocoders import GoogleV3

gc.enable()

_URL = 'http://www1.toronto.ca/fire/livecad.xml?'
_digits = re.compile('/d')

def contains_digits(d):
    return bool(_digits.search(d))

response = requests.get(_URL)
r_code = 'Status = ' + str(response.status_code)
r_encoding = 'Encoding = ' + str(response.encoding)
print r_code
print r_encoding