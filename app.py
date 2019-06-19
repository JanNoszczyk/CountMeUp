from count_me_up import CountMeUp
import json
import atexit
import threading
from flask import Flask, request


# Create new CountMeUp object
counter = CountMeUp()

# Time interval between calling counter.process_vote
pool_time = 0.0001

# lock to control access to variable
lock = threading.Lock()
# thread handler
thread = threading.Thread()

def create_app():
    """
    Each process_votes method in turn calls the counter.process_vote to process a single vote from the queue.
    It then runs itself concurrently within a thread.
    The Flask web app exposes API to add new votes and to display the candidate vote statistics.
    However, the processing of new user votes operates on the same CountMeUp object as Flask, therefore it needs to be
    ran as a background thread executed at every pool_time interval.
    :return: Flask web application instance
    """
    # Create a flask app
    app = Flask(__name__)

    def interrupt_thread():
        global thread
        thread.cancel()

    def process_votes():
        global counter
        global thread
        with lock:
            # Process a single vote from the queue
            counter.process_vote()
        # Start next thread to process a vote again in the next time interval
        thread = threading.Timer(pool_time, process_votes, ())
        thread.start()

    def initialise_process():
        # Create the thread for the first time and run it
        global thread
        thread = threading.Timer(pool_time, process_votes, ())
        thread.start()

    initialise_process()
    # After the Flask web app is closed, clear the old thread
    atexit.register(interrupt_thread)
    return app


app = create_app()


@app.route('/')
def check_candidate_votes():
    """
    :return: API call will return the current candidate statistics
    """
    return json.dumps(counter.candidate_votes)


@app.route('/clear_votes/')
def clear_votes():
    """
    Will reset the candidate vote statistics
    """
    counter.candidate_votes = {1:0, 2:0, 3:0, 4:0, 5:0}
    return "Votes cleared"


@app.route('/submit', methods=['GET'])
def submit_vote():
    """
    API call will add the user and his vote to the current vote queue
    """
    user = request.args.get('user', None)
    candidate = request.args.get('candidate', None)
    counter.add_vote(str(user), int(candidate))
    return user + ' ' + candidate


if __name__ == "__main__":
    print('Flask starting to run')
    app.run()
