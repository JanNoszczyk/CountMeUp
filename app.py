from count_me_up import CountMeUp
import asyncio
from flask import Flask

# Create a flask app
app = Flask(__name__)
# Create new CountMeUp object
counter = CountMeUp()

async def add_votes_randomly():
    await counter.add_vote()

async def process_all_votes():
    await counter.process_vote()

@app.route('/')
def hello_world():
    return counter.candidate_votes

# Create an asynchronous loop to create random votes and also to process them
loop = asyncio.get_event_loop()
loop.create_task(add_votes_randomly())
loop.create_task(process_all_votes())
loop.run_forever()
loop.close()

