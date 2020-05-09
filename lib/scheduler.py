NUM_NBA_WEEKS = 20

def all_pairs(lst):
  if len(lst) < 2:
    yield []
    return
  if len(lst) % 2 == 1:
    # Handle odd length list
    for i in range(len(lst)):
      for result in all_pairs(lst[:i] + lst[i+1:]):
        yield result
  else:
    a = lst[0]
    for i in range(1,len(lst)):
      pair = (a,lst[i])
      for rest in all_pairs(lst[1:i]+lst[i+1:]):
        yield [pair] + rest

def schedule(player_ids):
  total_schedule = []

  while len(total_schedule) < NUM_NBA_WEEKS:
    total_schedule += all_pairs(player_ids)

  return total_schedule[:NUM_NBA_WEEKS]
