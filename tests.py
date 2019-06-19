"""Before running, make sure that app.py is running locally first."""
import requests
import urllib.request
from requests.exceptions import HTTPError

MAIN_URL = 'http://127.0.0.1:5000/'

def test_1():
    votes = [
        ('John', '1'),
        ('Ben', '2'),
        ('Julie', '3'),
        ('Sophie', '4')
    ]

    for user, candidate in votes:
        url = MAIN_URL + 'submit?user={}&candidate={}'.format(user, candidate)
        print(url)
        try:
            response = requests.get(url)
            print(response.text)
        except:
            print("Request error")


test_1()

# req = urllib.request.urlopen(MAIN_URL + 'submit_vote/?param=Jan&param=Pan')
# print(req)