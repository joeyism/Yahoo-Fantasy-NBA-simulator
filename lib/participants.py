

class Participants(object):
  PLAYER_IDS_FILENAME = 'data/participant_ids'
  PLAYER_URLS_FILENAME = 'data/participant_urls'

  def __init__(self, id, url):
    self.id = id
    self.url = url

  @classmethod
  def write_participant_ids(cls, participant_ids):
    with open(cls.PLAYER_IDS_FILENAME, 'w') as f:
      for item in participant_ids:
        f.write("%s\n" % item)

  @classmethod
  def get_participant_ids(cls):
    return open(cls.PLAYER_IDS_FILENAME, "r").read().split("\n")[:-1]

  @classmethod
  def write_participant_urls(cls, participant_urls):
    with open(cls.PLAYER_URLS_FILENAME, 'w') as f:
      for item in participant_urls:
        f.write("%s\n" % item)

  @classmethod
  def get_participant_urls(cls):
    return open(cls.PLAYER_URLS_FILENAME, "r").read().split("\n")[:-1]

  @classmethod
  def get_participants(cls):
    participants = []
    for id, url in zip(participant_ids, participant_urls):
      participants.append(Participants(id, url))
    return participants
