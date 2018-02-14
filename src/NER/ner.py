import sys
import re
from natasha import NamesExtractor, DatesExtractor, MoneyExtractor, AddressExtractor, OrganisationExtractor
from natasha.extractors import Extractor
from pymystem3 import Mystem
from datetime import datetime, timedelta

from yargy_ner import extract_full_date

m = Mystem()


def lemmatize(s):
    global m
    try:
        return ''.join(m.lemmatize(s)).strip()
    except BrokenPipeError as ex:
        m = Mystem()
        return lemmatize(s)

#for line in sys.stdin:
#    matches = dates_extractor(line)
#    facts = []
#    for match in matches:
#        facts.append(match.fact)
#    print(facts)


def extract_users(text):
    return re.findall('(@\w+)', text)


count_names = 'один|два|три|четыре|пять|шесть|семь|восемь|девять|десять'.split('|')

def extract_date(orig_text):
    text = lemmatize(orig_text)
    digit_matches = re.search('(\\d+) (день|неделя|месяц|год)', text)
    word_matches = re.search('(один|два|три|четыре|пять|шесть|семь|восемь|девять|десять) (день|неделя|месяц|год)', text)

    if 'завтра' in text:
        return datetime.now() + timedelta(days=1)
    elif 'послезавтра' in text:
        return datetime.now() + timedelta(days=2)

    elif word_matches or digit_matches:
        # даю тебе четыре дня на реализацию
        # код должен работать через два месяца начиная с сейчас
        if word_matches:
            count = word_matches.index(word_matches.group(1)) + 1
            datenames = word_matches.group(2)

        # даю тебе 4 дня на реализацию
        # код должен работать через 2 месяца начиная с сейчас
        elif digit_matches:
            count = int(digit_matches.group(1))
            datenames = digit_matches.group(2)
        else:
            raise RuntimeError('Unknown date')

        if datenames == 'день':
            return datetime.now() + timedelta(days=count)
        elif datenames == 'неделя':
            return datetime.now() + timedelta(days=count*7)
        elif datenames == 'месяц':
            return datetime.now() + timedelta(days=count*30)
        elif datenames == 'год':
            return datetime.now() + timedelta(days=count*365)

    # срок тебе неделя
    elif 'день' in text:
        return datetime.now() + timedelta(days=1)
    elif 'неделя' in text:
        return datetime.now() + timedelta(days=7)
    elif 'месяц' in text:
        return datetime.now() + timedelta(days=30)
    else:
        return extract_full_date(orig_text)


if __name__ == '__main__':
    tests = '''сделай к 4 февраля
даю тебе 4 дня на реализацию
код должен работать через 2 месяца начиная с сейчас    
срок тебе неделя
тут нет даты'''
    print('now', datetime.now())
    for line in tests.splitlines():
        print(line)
        print(extract_date(line))
        print()

    print(extract_users('сообщи когда будут проблемы @tsundokum'))
