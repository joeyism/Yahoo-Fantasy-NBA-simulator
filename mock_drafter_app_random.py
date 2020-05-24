import os
from flask import Flask, request, jsonify
import pandas as pd
import requests
import random

app = Flask(__name__)

DO_NOT_DRAFT_PLAYERS = [
  "curryst01",
  "embiijo01",
  "doncilu01",
  "tatumja01",
  "siakapa01",
  "whiteha01",
  "moranja01",
  "grahade01",
  "anthoca01",
  "leverca01",
  "youngth01", 
  "randlju01", 
  "fultzma01", 
  "huertke01", 
  "bartowi01",
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
  res = requests.get('http://localhost:5000/draft')
  draft_names = res.json()
  random_int = random.randint(0, len(draft_names))
  playerid = draft_names[random_int]
  while playerid in DO_NOT_DRAFT_PLAYERS:
    random_int = random.randint(0, len(draft_names))
    playerid = draft_names[random_int]
  print(f"Draft: {playerid}")
  return send_json(200, {"playerid": playerid})

if __name__ == '__main__':
   app.run(debug = True, port=8082)
