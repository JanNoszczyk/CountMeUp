"""Before running, make sure that app.py is running locally first.
Restart app.py before running again"""
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
        ('John', 1), ('John', 1), ('John', 5), ('John', 5),
        ('Ben', 2), ('Ben', 2),
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
    print("Checking that all vote statistics were submitted correctly for (user, candidate): \n", response_2)
    print("User John made 2 votes for both candidates 1 and 5, only one vote for candidate 5 was counted")
    assert response_2['1'] == 2 and response_2['5'] == 1
    assert response_2['2'] == 2
    assert response_2['3'] == 1 and response_2['4'] == 1


def test_2():
    """
    Test to confirm that vote statistics are updated in less than 1s
    """
    def submit_100_random_votes():
        # Adding 50 new votes
        votes = [(str(uuid4()), randint(1, 5)) for i in range(50)]
        for user, candidate in votes:
            url = MAIN_URL + 'submit?user={}&candidate={}'.format(user, candidate)
            requests.get(url)

    start_timer = time.time()
    submit_100_random_votes()
    stats_1 = requests.get(MAIN_URL).text
    submit_100_random_votes()
    stats_2 = requests.get(MAIN_URL).text
    stop_timer = time.time()

    print("Checking that statistics updated in less than a minute")
    print("Checked for 2 vote statistic measurements with 100 new votes added.")
    print("Finishes in: ", stop_timer - start_timer)
    # Check that the two return vote statistics are different (ie they were updated)
    assert stats_1 != stats_2
    # Check that the running time is below 1s
    assert stop_timer-start_timer < 1

test_1()
test_2()
print("All tests were successful")
