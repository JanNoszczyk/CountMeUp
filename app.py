from count_me_up import CountMeUp
import json
import threading
import atexit
from uuid import uuid4
from flask import Flask, request
from random import randint


# Create new CountMeUp object
counter = CountMeUp()

# Time interval between calling counter.process_vote
pool_time = 0.01

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
            print(counter.candidate_votes)
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
    return json.dumps(counter.candidate_votes)


@app.route('/random_votes/')
def add_random_votes():
    for i in range(100):
        user = str(uuid4())
        candidate = randint(1, 5)
        counter.add_vote(user, candidate)
    return "Done adding"


@app.route('/clear_votes/')
def clear_votes():
    counter.candidate_votes = {1:0, 2:0, 3:0, 4:0, 5:0}
    return "Votes cleared"


# @app.route("/submit_vote/")
# def hello():
#     user, candidate = request.args.getlist('param')
#     print(user, candidate)
#     counter.add_vote(user, candidate)
#     return user, candidate

@app.route('/submit', methods=['GET'])
def foo():
   user = request.args.get('user', None)
   candidate = request.args.get('candidate', None)
   return user + '' + candidate


if __name__ == "__main__":
    print('Flask starting to run')
    app.run()