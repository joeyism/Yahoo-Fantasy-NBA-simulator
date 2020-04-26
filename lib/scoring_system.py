import json

class ScoringSystem(object):
  H2H_SCORE = json.load(open('config/head2head_points.json'))
  H2H = json.load(open('config/head2head.json'))

  @classmethod
  def score_head_to_head_points(cls, row):
    return sum(row[col]*score for col, score in cls.H2H_SCORE.items())

  @classmethod    
  def compare_head_to_head(cls, series1, series2):
    series1_wins = []
    series2_wins = []

    for col, val in cls.H2H.items():
      if series1[col]*val > series2[col]*val:
        series1_wins.append(col)
      else:
        series2_wins.append(col)

    return series1_wins, series2_wins
