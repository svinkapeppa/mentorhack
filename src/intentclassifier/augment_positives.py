from common import DATASETS, get_imperative_variants

import csv

from nltk.tokenize import wordpunct_tokenize


def merge_punk(s):
    return s.replace(' .', '.').replace(' ,', ',').replace(' !', '!').replace(' :', ':').replace(' ( ', ' (').replace(' по – ', ' по–')

positives = []
with (DATASETS / 'youdo.txt').open() as f:
    csvr = csv.reader(f, delimiter=',')
    for row in csvr:
        t = '\n'.join(' '.join(wordpunct_tokenize(l)) for l in row[1].strip().splitlines() if l)
        summary =  row[0]
        positives.append((summary, t))

n = len(positives)

with (DATASETS / 'youdo2.txt').open('w') as f:
    c = csv.writer(f)
    i = 0
    for summary, t in positives:
        i += 1
        if i % 25000 == 0:
            print('{:.2f}%'.format(i / n * 100))
        for aug in get_imperative_variants(t):
            c.writerow([summary, merge_punk(aug)])

