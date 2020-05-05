import os
from flask import Flask, render_template, request, jsonify
from lib import Data
import pandas as pd

app = Flask(__name__)

YEAR = int(os.getenv("YEAR"))
PREVIOUS_YEAR = YEAR - 1
DATA = Data(YEAR)

def send_json(status_code, message):
  resp = jsonify(message)
  resp.status_code = status_code
  return resp

@app.route('/')
@app.route('/index')
def index():
  df = pd.read_csv("data/this_season_player_data.csv")
  return render_template(
    'players.html',
    data=df[['slug', 'name', 'age', 'drafted']].values
  )

@app.route('/draft', methods=['POST', 'GET'])
def draft():
  if request.method == 'POST':
    userid = request.json.get('userid') or ""
    playerid = request.json.get('playerid') or ""

    if not userid or not playerid:
      return send_json(400, {"error": "userid or playerid not passed"})

    df = pd.read_csv("data/this_season_player_data.csv")
    player = df.loc[df["slug"] == playerid, :].iloc[0]

    if player["drafted"]:
      return send_json(400, {"error": "player already drafted"})

    player["drafted"] = True
    player["drafted_by"] = playerid
    df.loc[player.name, :] = player
    df.to_csv("data/this_season_player_data.csv", index=False)
    return send_json(200, {"msg": "success"})

  elif request.method == 'GET':
    df = pd.read_csv("data/this_season_player_data.csv")
    return send_json(200, df.loc[~df["drafted"], "slug"].values.tolist())


if __name__ == '__main__':
   app.run(debug = True, port=5000)
