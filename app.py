from count_me_up import CountMeUp
import json
import threading
import atexit
from uuid import uuid4
from flask import Flask
from random import randint


# Create new CountMeUp object
counter = CountMeUp()

# Time interval between calling counter.process_vote
pool_time = 0.1

lock = threading.Lock()
thread = threading.Thread()

def create_app():
    # Create a flask app
    app = Flask(__name__)

    def process_votes():
        # Should counter be global?
        global counter
        global thread
        # Process a single vote from the queue
        with lock:
            counter.process_vote()
        # Start next thread to process a vote again in the next time interval
        thread = threading.Timer(pool_time, process_votes(), ())
        thread.start()

    def initialise_process():
        # Create the thread for the first time and run it
        global thread
        thread = threading.Timer(pool_time, process_votes(), ())
        thread.start()

    def interrupt_thread():
        global thread
        thread.cancel()

    initialise_process()
    atexit.register(interrupt_thread)
    return app

# Create new Flask app with vote processing threads running in the background
app = create_app()

@app.route('/')
def hello_world():
    return json.dumps(counter.candidate_votes)

@app.route('/vote/')
def add_random_votes():
    for i in range(100):
        user = str(uuid4())
        candidate = randint(1, 5)
        counter.add_vote(user, candidate)
    return "Done adding"


# if __name__ == "__main__":
#     app.run()
#     # Thread(target=counter.process_vote()).start()
#     # Thread(target=app.run()).start()
