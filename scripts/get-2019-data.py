from lib import Data
from tqdm import tqdm
import pandas as pd

data = Data(2019)
total_game_data = []
for date, day_data in tqdm(data.per_day_game_data(), desc="Getting per day data"):
  for player_data in day_data:
    player_data['date'] = date
  total_game_data += day_data

print("Saving data...")
df = pd.DataFrame(total_game_data)
filename = "data/nba_2018_2019_season_data.csv"
df.to_csv(filename, index=False)
print(f"Successfully saved to {filename}")
