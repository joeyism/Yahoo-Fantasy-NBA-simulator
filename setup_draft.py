import os
import setup_simulation
import argparse
import uuid
import pandas as pd
import requests
from lib import Participants

def draft(all_participants, df_filename="data/this_season_player_data.csv"):
  df = pd.read_csv(df_filename)
  for draft_round, participants in enumerate([all_participants, list(reversed(all_participants))]*7 + [all_participants]):
    print(f"Draft round {draft_round}")
    for participant in participants:
      res = requests.get(participant.url, timeout=30)
      data = res.json()
      try:
        playerid = data.get("playerid")
        player = df.loc[df["slug"] == playerid, :].iloc[0]

        if player["drafted"]:
          raise Exception("User already drafted")

        player["drafted"] = True
        player["drafted_by"] = participant.id
        df.loc[player.name, :] = player
        df.to_csv(df_filename, index=False)
      except Exception as err:
        print(f"Error for participant {participant.id} ", err)


def run(no_players, restart=False, prompt_each=False):
  if restart:
    setup_simulation.start()
    participant_ids = [str(uuid.uuid4()) for _ in range(no_players)]
    Participants.write_participant_ids(participant_ids)
  else:
    participant_ids = Participants.get_participant_ids()

  if os.path.exists(Participants.PLAYER_URLS_FILENAME) and not restart:
    participant_urls = Participants.get_participant_urls()
  elif prompt_each:
    participant_urls = []
    for i, participant_id in enumerate(participant_ids):
      url = input(f"Url for user {participant_id}: ")
      participant_urls.append(url)
    Participants.write_participant_urls(participant_urls)
  else:
    participant_urls = input("Urls: ").split()
    Participants.write_participant_urls(participant_urls)

  participants = []
  for id, url in zip(participant_ids, participant_urls):
    participants.append(Participants(id, url))

  input("Press enter to draft")
  draft(participants)


def main():
  parser = argparse.ArgumentParser()
  parser.add_argument("--restart", action="store_true")
  parser.add_argument("--prompt-each", action="store_true")
  parser.add_argument("--no-players", help="Number of players in draft", type=int)

  args = parser.parse_args()
  run(args.no_players, restart=args.restart, prompt_each=args.prompt_each)

if __name__ == '__main__':
  main()
