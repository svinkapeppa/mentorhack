import pickle
from pathlib import Path
from nltk.tokenize import wordpunct_tokenize
import re

MODELS = Path('../models/ir').expanduser()

with (MODELS / 'classifier3.pickle').open('rb') as f:
    classifier = pickle.load(f)

def is_task(s):
    lines = [' '.join(wordpunct_tokenize(line.strip())) for line in s.splitlines() if line.strip()]
    text = '\n'.join(lines)
    return classifier.predict([text])[0]

def is_trello_token(s):
    if re.match('^[\w\d]{64} [\w\d]{24}$', s) is not None:
        return True
    else:
        return False
    
