from lib import Data
import argparse

def convert_name(player_names, year):
  data = Data(year)
  player_slugs = []
  for player_name in player_names:
    player_slugs.append(data.NAME_SLUG_CONVERTER[player_name.strip().lower()])
  return player_slugs

def main():
  parser = argparse.ArgumentParser()
  parser.add_argument("player_name", help="Player name to transform")
  parser.add_argument("--year", help="Which year this player plays in", default=2020)
  parser.add_argument("--multiple", help="Whether list of name or single name", action="store_true")
  args = parser.parse_args()

  if args.multiple:
    player_names = args.player_name.split(",")
  else:
    player_names = [args.player_name]

  player_slugs = convert_name(player_names, args.year)
  print(", ".join(player_slugs))


if __name__ == "__main__":
  main()
