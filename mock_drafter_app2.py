import os
from flask import Flask, request, jsonify
import pandas as pd
import requests

app = Flask(__name__)

CALL_COUNT = 0
DRAFT_PLAYERS = [
  'westbru01',
  'rosste01',
  'lillada01',
  'robindu01',
  'allenja01',
  'johnsja01',
  'bertada01',
  'harremo01',
  'paytoel01',
  'sextoco01',
  'mitchdo01',
  'dragigo01',
  'beaslma01',
  'capelca01',
  'lavinza01'
]

def send_json(status_code, message):
  resp = jsonify(message)
  resp.status_code = status_code
  return resp

@app.route('/')
@app.route('/index')
def index():
  global CALL_COUNT
  res = requests.get('http://localhost:5000/draft')
  draft_names = res.json()
  playerid = DRAFT_PLAYERS[CALL_COUNT]
  print(f"Draft Round {CALL_COUNT}: {playerid}")
  CALL_COUNT += 1
  return send_json(200, {"playerid": playerid})

if __name__ == '__main__':
   app.run(debug = True, port=8081)
