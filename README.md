The program simulates a real-time voting system, where users can submit votes on 5 diffent candidates via API calls, and the total vote statistics can also be accessed through API.
The program runs locally as a Flask application. To run it locally, first run app.py to run the simulator, and then run tests.py to see it working. Make sure to download all the neccessary libraries listed in reqiurements.txt.

Note, I had no previous front-end or back-end experience, so this project was very new to me. 
Initially I tried processing new votes being submitted and processed asynchronously using Python's asyncio library. However, I had issues with that implementation. Instead I decided to run a regular Flask app with a background vote processing method ran inside a thread.
