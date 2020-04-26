import os
import pickle

CACHE_FOLDER = './.cache'
if not os.path.exists(CACHE_FOLDER):
  os.makedirs(CACHE_FOLDER)

def get_cache(path, fn, verbose=False, *args, **kwargs):
  filepath = os.path.join(CACHE_FOLDER, path)
  if os.path.exists(filepath):
    if verbose:
      print(f"Cache found in {filepath}. Loading...")
    return pickle.load(open(filepath, "rb"))
  else:
    if verbose:
      print(f"Cache not found in {filepath}. Downloading...")
    data = fn(*args, **kwargs)
    pickle.dump(data, open(filepath, "wb"))
    return data
