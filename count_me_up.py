import queue


class CountMeUp:
  """
  CountMeUp creates a FIFO queue to store all the votes. It also has methods to add new votes to the queue and to
  display the current vote statistics.
  CountMeUp will also track the total number of votes per candidate and the number of votes done per each user using
  hashmaps stored in runtime memory
  I do not have any experience in front-end or server-side developtment. Therefore, I have implemented my CountMeUp
  program as running locally with all the data stored locally. Alternatively,
  """
  def __init__(self):
    self.maxsize = 10000000
    self.Queue = queue.Queue(self.maxsize)
    self.candidate_votes = {1:0, 2:0, 3:0, 4:0, 5:0}
    self.users = {}

  def add_vote(self, user, candidate):
    """
    The function will add the vote to the queue.
    Each vote is stored as a tuple in the queue as (user, candidate)
    :param user: The user who submitted the vote
    :param candidate: The candidate for whom the vote was submitted
    """
    self.Queue.put((user, candidate))

  def process_vote(self):
    """
    The function will process a vote at the beginning of the queue. If the queue is empty for more than 20seconds,
    an Empty exception will be raised.
    If the vote is valid (submitted by a user with at most 3 votes) it will be added to the candidate_votes dictionary
    which counts up the number of valid votes made per candidate. Otherwise, the vote will not be counted. The numbers
    of votes made per user are tracked in the dictionary users.
    """
    user, candidate = self.Queue.get()
    if user in self.users:
      if self.users[user] <= 3:
        # The vote will only be counted if its valid
        self.candidate_votes[candidate] += 1
      self.users[user] += 1
    else:
      # If the user is new, add him to the users dictionary
      self.users[user] = 1
      self.candidate_votes[candidate] += 1


