import os
from flask import Flask, request, jsonify
import pandas as pd
import requests

app = Flask(__name__)

CALL_COUNT = 0
DRAFT_PLAYERS = [
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
  "bartowi01"
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
   app.run(debug = True, port=8080)
