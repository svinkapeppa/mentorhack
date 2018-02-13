import pickle
from pathlib import Path
from nltk.tokenize import wordpunct_tokenize

MODELS = Path('../models/ir').expanduser()

with (MODELS / 'classifier.pickle').open('rb') as f:
    classifier = pickle.load(f)

def is_task(s):
    lines = [' '.join(wordpunct_tokenize(line.strip())) for line in s.splitlines() if line.strip()]
    text = '\n'.join(lines)
    return classifier.predict([text])[0]
