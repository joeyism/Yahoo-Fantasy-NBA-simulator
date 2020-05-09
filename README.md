# Yahoo Fantasy NBA Simulator
This is a library that simulates past Yahoo Fantasy NBA, to help you check how well you could have done historically. In order for this to run, you must supply a list of NBA player names

Supported Format:
* Head to Head

## How to Run Draft

### Host
Run
```bash
python3 app.py
```

Wait for users to start their own servers. Then run
```bash
honcho run python3 setup_draft.py --no-players $NUM_PLAYERS --restart
```

### Users
Start `ngrok` via
```bash
ngrok http 8080
```
and give your host the ngrok URL.

Create an API similar to the one in `mock_drafter_app.py`, then execute it via
```bash
python3 mock_drafter_app.py
```

## How to Run Simulation
You must supply files, each with a list of NBA players for each user/player. Then, run the simulation to see which user/player wins


## Sample Run

### Normal Run
```bash
python3 simulate.py --player1_file data/sample_joey_file.txt --player2_file data/sample_leo_file.txt --player1_name Joey --player2_name Leo
```

returns

```
Total Results for 2019-2020 season
		Joey: 83	Leo: 88
```

### Verbose Run
```bash
python3 simulate.py --player1_file data/sample_joey_file.txt --player2_file data/sample_leo_file.txt --player1_name Joey --player2_name Leo --verbose
```
returns
```
Begin running simulation for NBA 2019-2020 season

Week 2019-10-21		Joey: 4	Leo: 5
Week 2019-10-28		Joey: 3	Leo: 6
Week 2019-11-04		Joey: 5	Leo: 4
Week 2019-11-11		Joey: 4	Leo: 5
Week 2019-11-18		Joey: 4	Leo: 5
Week 2019-11-25		Joey: 6	Leo: 3
Week 2019-12-02		Joey: 3	Leo: 6
Week 2019-12-09		Joey: 6	Leo: 3
Week 2019-12-16		Joey: 4	Leo: 5
Week 2019-12-23		Joey: 6	Leo: 3
Week 2019-12-30		Joey: 5	Leo: 4
Week 2020-01-06		Joey: 5	Leo: 4
Week 2020-01-13		Joey: 3	Leo: 6
Week 2020-01-20		Joey: 1	Leo: 8
Week 2020-01-27		Joey: 3	Leo: 6
Week 2020-02-03		Joey: 5	Leo: 4
Week 2020-02-17		Joey: 6	Leo: 3
Week 2020-02-24		Joey: 5	Leo: 4
Week 2020-03-02		Joey: 5	Leo: 4

Total Results for 2019-2020 season
		Joey: 83	Leo: 88

Joey wins:
	total_rebounds: 17
	assists: 14
	blocks: 11
	steals: 10
	ft%: 8
	points: 7
	turnovers: 7
	made_three_point_field_goals: 5
	fg%: 4

Leo wins:
	fg%: 15
	made_three_point_field_goals: 14
	points: 12
	turnovers: 12
	ft%: 11
	steals: 9
	blocks: 8
	assists: 5
	total_rebounds: 2
```
