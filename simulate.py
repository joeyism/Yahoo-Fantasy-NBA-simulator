import pandas as pd
import simulate_h2h
from tqdm import tqdm
from lib import Participants, scheduler, Data
from collections import defaultdict

YEAR = os.getenv("YEAR", 2020)

def main():
  PARTICIPANT_PLAYERS = {}
  PLAYER_WINS = defaultdict(list)
  participant_ids = Participants.get_participants()
  schedule = scheduler.scheduler(participant_ids)
  df = pd.read_csv(DATA.THIS_SEASON_PLAYER_FILENAME)

  for participant_id in participant_ids:
    PARTICIPANT_PLAYERS[participant_id] = df.loc[df["drafted_by"] == participant_id, "slug"].values

  data = Data(YEAR)
  for i, data in enumerate(data.per_week_game_data()):
    date, game_data = data
    for participant1_id, participant2_id in schedule[i]:
      series1_wins, series2_wins = head_to_head_week(
          date,
          game_data,
          PARTICIPANT_PLAYERS[participant1_id],
          PARTICIPANT_PLAYERS[participant2_id],
          participant1_id,
          participant2_id,
          verbose)
      PLAYER_WINS[participant1_id] += series1_wins
      PLAYER_WINS[participant2_id] += series2_wins

  for participant_id in PLAYER_WINS:
    simulate_h2h.print_common_wins(PLAYER_WINS[participant_id])
  return


if __name__ == "__main__":
  main()
