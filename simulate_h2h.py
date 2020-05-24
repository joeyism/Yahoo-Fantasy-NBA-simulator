f"""
Sample run
  python3 {__file__} --player1_file data/sample_joey_file.txt --player2_file data/sample_leo_file.txt --player1_name Joey --player2_name Leo --verbose
"""
import os
from lib import Data, ScoringSystem
from tqdm import tqdm
import pandas as pd
import argparse
from collections import Counter


def _calculate_pct_(series):
  series["fg%"] = series["made_field_goals"]/series["attempted_field_goals"]
  series["ft%"] = series["made_free_throws"]/series["attempted_free_throws"]
  return series

def _sum_for_list_of_players_(df, players):
  df = df.loc[df["slug"].isin(players), :]
  series = df.sum()
  series = _calculate_pct_(series)
  return series

def print_common_wins(total_wins, name):
  user_counter = Counter(total_wins).most_common()
  print(f"\n{name} wins:\n" + "\n".join([f"\t{count[0]}: {count[1]}" for count in user_counter]))
  print(f"\nTotal wins:\t{len(total_wins)}")

def head_to_head_season(user1_players, user2_players, user1_name="User 1", user2_name="User 2", year=os.getenv("YEAR", 2020), verbose=False):
  if verbose:
    print(f"Begin running simulation for NBA {year-1}-{year} season\n")

  data = Data(year)
  user1_players = data.convert_names(user1_players)
  user2_players = data.convert_names(user2_players)

  player1_total_wins = []
  player2_total_wins = []

  for date, game_data in data.per_week_game_data():
    series1_wins, series2_wins = head_to_head_week(date, game_data, user1_players, user2_players, user1_name, user2_name, verbose)
    player1_total_wins += series1_wins
    player2_total_wins += series2_wins

  print(f"\nTotal Results for {year-1}-{year} season\n\t\t{user1_name}: {len(player1_total_wins)}\t{user2_name}: {len(player2_total_wins)}")
  if verbose:
    print_common_wins(player1_total_wins, user1_name)
    print_common_wins(player2_total_wins, user2_name)
  return

def head_to_head_week(date, game_data, user1_players, user2_players, user1_name="User 1", user2_name="User 2", verbose=False):
  df_game_data = pd.DataFrame(game_data)
  series1 = _sum_for_list_of_players_(df_game_data, user1_players)
  series2 = _sum_for_list_of_players_(df_game_data, user2_players)
  series1_wins, series2_wins = ScoringSystem.compare_head_to_head(series1, series2)

  if verbose:
    print(f"Week {date}\t\t{user1_name}: {len(series1_wins)}\t{user2_name}: {len(series2_wins)}")

  return series1_wins, series2_wins


def read_players_file(user_file):
  return open(user_file, "r").read().split("\n")[:-1]


def main():
  parser = argparse.ArgumentParser()
  parser.add_argument("--player1_name", help="Player1 name", default="Player 1")
  parser.add_argument("--player2_name", help="Player2 name", default="Player 2")
  parser.add_argument("--player1_file", help="Player1 file", default="Player 1")
  parser.add_argument("--player2_file", help="Player2 file", default="Player 2")
  parser.add_argument("--year", help="Which year this player plays in", default=os.getenv("YEAR", 2020), type=int)
  parser.add_argument("-v", "--verbose", action="store_true")
  args = parser.parse_args()

  user1_players = read_players_file(args.player1_file)
  user2_players = read_players_file(args.player2_file)

  head_to_head_season(
    user1_players,
    user2_players,
    user1_name=args.player1_name,
    user2_name=args.player2_name,
    year=args.year,
    verbose=args.verbose)

if __name__ == "__main__":
  main()
