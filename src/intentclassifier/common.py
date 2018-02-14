import re
import json
import os
import csv
import sys

from nltk.tokenize import wordpunct_tokenize

import pickle
from pathlib import Path

from pymystem3 import Mystem
import pymorphy2

morph = pymorphy2.MorphAnalyzer()
m = Mystem()


def mystem_analyze(str):
    global m
    try:
        return m.analyze(str)
    except BrokenPipeError as ex:
        m = Mystem()
        return mystem_analyze(str)

DATASETS = Path('~/data/taskdialog').expanduser()
MODELS = Path('~/data/taskdialog/models').expanduser()

def to_imperative(word):
    try:
        p = [pm for pm in morph.parse(word) if 'INFN' in pm.tag][0]
    except IndexError as ex:
        return
    try:
        sing = p.inflect({'VERB', 'perf', 'impr', 'excl', 'plur'}).word
        plur = p.inflect({'VERB', 'perf', 'impr', 'excl'}).word
        return (sing, plur)
    except AttributeError as ex:
        return
    
assert to_imperative('Совершить') == ('совершите', 'соверши')
    
words_of_need = {'необходимо', 'нужно'}

def get_imperative_variants(text):
    try:
        words = []
        isinf = []
        for tok in mystem_analyze(text.lower()):
            if 'analysis' in tok:
                if len(tok['analysis']) >= 1:
                    gram = tok['analysis'][0]['gr']
                    infinitive = 'инф' in gram and 'V' in gram
                    w = tok['text']
                    words.append(w)
                    isinf.append(infinitive)
        if max(isinf) == False:
            return text,
        if isinf[0]:
            variants = []
            for w, v in zip(words, isinf):
                if v:
                    imp = to_imperative(w)
                    variants.append(imp or (w, w))
                else:
                    variants.append((w, w))
            sing, plur = zip(*variants)
            return text, ' '.join(sing), ' '.join(plur)
        elif words_of_need.intersection(words):
            prev_word = ''
            variants = []
            used_imperative = False
            for w, v in zip(words, isinf):
                if v and prev_word in words_of_need:
                    imp = to_imperative(w)
                    if imp:
                        variants.pop()
                        variants.append(imp)
                        used_imperative = True
                    else:
                        variants.append((w, w))

                else:
                    variants.append((w, w))
                prev_word = w

            if used_imperative:
                sing, plur = zip(*variants)
                return text, ' '.join(sing), ' '.join(plur)
    except ValueError as ex:
        pass
    return text,
        
assert get_imperative_variants('нужно сделать хорошо')[1] == 'сделайте хорошо'
assert get_imperative_variants('повертеть попой')[2] == 'поверти попой'
assert len(get_imperative_variants('хорошо сделать')) == 1
