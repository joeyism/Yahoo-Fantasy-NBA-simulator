from basketball_reference_web_scraper import client
from datetime import timedelta
from lib.cache import get_cache
from dateutil import tz

EST = tz.gettz('America/Toronto')


class Data(object):
  DEFAULT_SEASON_YEAR = 2019
  THIS_SEASON_PLAYER_FILENAME = "data/this_season_player_data.csv"

  def __init__(self, season_year=None):
    if season_year is None:
      self.season_year = self.DEFAULT_SEASON_YEAR
    else:
      self.season_year = season_year

    self.full_schedule = get_cache(
        path=f'{self.season_year}_full_schedule',
        fn=client.season_schedule,
        season_end_year=self.season_year)

    self.player_total = get_cache(
        path=f'{self.season_year}_player_total',
        fn=client.players_season_totals,
        season_end_year=self.season_year)

    self.SLUG_NAME_CONVERTER = dict((player['slug'], player['name'].lower()) for player in self.player_total)
    self.NAME_SLUG_CONVERTER = dict((player['name'].lower(), player['slug']) for player in self.player_total)
    self.game_dates = sorted(list(set(game['start_time'].astimezone(EST).date() for game in self.full_schedule)))

  def per_day_game_data(self):
    for date in self.game_dates:
      data = get_cache(
        path=f'{self.season_year}_{date}_game_data',
        fn=client.player_box_scores,
        day=date.day,
        month=date.month,
        year=date.year)
      yield (date, data)

  def per_week_game_data(self):
    this_week_game_data = []
    for date, game_data in self.per_day_game_data():
      this_week_game_data += game_data
      if date.isoweekday() == 7:
        week_date = date - timedelta(days=6)
        yield (week_date, this_week_game_data)
        this_week_game_data = []

  def convert_names(self, player_names):
    player_slugs = []
    for player_name in player_names:
      player_slugs.append(self.NAME_SLUG_CONVERTER[player_name.strip().lower()])
    return player_slugs
