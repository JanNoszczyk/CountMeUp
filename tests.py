"""Before running, make sure that app.py is running locally first."""
import time
import json
import requests
from uuid import uuid4
from random import randint

MAIN_URL = 'http://127.0.0.1:5000/'

def test_1():
    """
    Test to confirm that votes are allocated correctly.
    """
    votes = [
        ('John', 1),
        ('Ben', 2),
        ('Julie', 3),
        ('Sophie', 4)
    ]

    # Clear the vote results to ensure test still runs correctly if rerun on the same app instance
    time.sleep(0.2)
    print("Clearing vote statistics")
    requests.get(MAIN_URL + 'clear_votes')
    time.sleep(0.2)

    for user, candidate in votes:
        url = MAIN_URL + 'submit?user={}&candidate={}'.format(user, candidate)
        response_1 = requests.get(url).text
        # Assert that the votes were submitted correctly
        print("Checking vote response for user {} {}".format(user, candidate))
        assert response_1 == user + ' ' + str(candidate)

    # Wait a little before asking for statistics again
    time.sleep(0.2)
    # Attempt to get user statistics
    response_2 = requests.get(MAIN_URL).text
    response_2 = json.loads(response_2)
    print("Checking that all vote statistics were submitted correctly: ", response_2)
    assert response_2['1'] == 1 and response_2['2'] == 1
    assert response_2['3'] == 1 and response_2['4'] == 1


def test_2():
    """
    Test to confirm that vote statistics are updated in less than 1s
    """
    def submit_100_random_votes():
        votes = [(str(uuid4()), randint(1, 5)) for i in range(50)]
        for user, candidate in votes:
            url = MAIN_URL + 'submit?user={}&candidate={}'.format(user, candidate)
            try:
                requests.get(url)
            except:
                print("Request error 4")

    start_timer = time.time()
    submit_100_random_votes()
    stats_1 = requests.get(MAIN_URL).text
    submit_100_random_votes()
    stats_2 = requests.get(MAIN_URL).text
    stop_timer = time.time()

    print("Checking that statistics updated in less than a minute")
    # Check that the two return vote statistics are different (ie they were updated)
    assert stats_1 != stats_2
    # Check that the running time is below 1s
    assert stop_timer-start_timer < 1

test_1()
test_2()
print("All tests were successful")
