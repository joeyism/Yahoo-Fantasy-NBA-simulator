import os
import setup_simulation
import argparse
import uuid
import pandas as pd
import requests
from lib import User

PLAYER_IDS_FILENAME = 'data/player_ids'
PLAYER_URLS_FILENAME = 'data/player_urls'

def _write_player_ids(player_ids):
  with open(PLAYER_IDS_FILENAME, 'w') as f:
    for item in player_ids:
      f.write("%s\n" % item)

def _get_player_ids():
  return open(PLAYER_IDS_FILENAME, "r").read().split("\n")[:-1]

def _write_player_urls(player_urls):
  with open(PLAYER_URLS_FILENAME, 'w') as f:
    for item in player_urls:
      f.write("%s\n" % item)

def _get_player_urls():
  return open(PLAYER_URLS_FILENAME, "r").read().split("\n")[:-1]

def draft(all_users, df_filename="data/this_season_player_data.csv"):
  df = pd.read_csv(df_filename)
  for draft_round, users in enumerate([all_users, list(reversed(all_users))]*7 + [all_users]):
    print(f"Draft round {draft_round}")
    for user in users:
      res = requests.get(user.url, timeout=30)
      data = res.json()
      try:
        playerid = data.get("playerid")
        player = df.loc[df["slug"] == playerid, :].iloc[0]

        if player["drafted"]:
          raise Exception("User already drafted")

        player["drafted"] = True
        player["drafted_by"] = user.id
        df.loc[player.name, :] = player
        df.to_csv(df_filename, index=False)
      except Exception as err:
        print(f"Error for user {user.id} ", err)


def run(no_players, restart=False):
  if restart:
    setup_simulation.start()
    player_ids = [str(uuid.uuid4()) for _ in range(no_players)]
    _write_player_ids(player_ids)
  else:
    player_ids = _get_player_ids()

  if os.path.exists(PLAYER_URLS_FILENAME) and not restart:
    player_urls = _get_player_urls()
  else:
    player_urls = input("Urls: ").split()
    _write_player_urls(player_urls)

  users = []
  for id, url in zip(player_ids, player_urls):
    users.append(User(id, url))
  draft(users)


def main():
  parser = argparse.ArgumentParser()
  parser.add_argument("--restart", action="store_true")
  parser.add_argument("--no-players", help="Number of players in draft", type=int)

  args = parser.parse_args()
  run(args.no_players, restart=args.restart)

if __name__ == '__main__':
  main()
