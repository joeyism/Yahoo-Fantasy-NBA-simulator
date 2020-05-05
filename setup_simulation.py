import os
from lib import Data
from tqdm import tqdm
import pandas as pd

YEAR = int(os.getenv("YEAR"))
PREVIOUS_YEAR = YEAR - 1
DATA = Data(YEAR)
PREVIOUS_YEAR_DATA = Data(PREVIOUS_YEAR)

# PREVIOUS SEASON
def start():
  total_game_data = []
  for date, day_data in tqdm(PREVIOUS_YEAR_DATA.per_day_game_data(), desc="Getting previous season data"):
    for player_data in day_data:
      player_data['date'] = date
    total_game_data += day_data

  print("Saving data...")
  df = pd.DataFrame(total_game_data)
  filename = "data/previous_season_data.csv"
  df.to_csv(filename, index=False)
  print(f"Successfully saved to {filename}")

  # THIS SEASON
  total_game_data = []

  print("Saving data...")
  df = pd.DataFrame(DATA.player_total)
  df = df[["slug", "name", "age"]]
  df["drafted"] = False
  df["drafted_by"] = ""
  filename = "data/this_season_player_data.csv"
  df.to_csv(filename, index=False)
  print(f"Successfully saved to {filename}")


if __name__ == '__main__':
  start()
