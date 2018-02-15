import re
from pymystem3 import Mystem
from datetime import datetime, timedelta

# from yargy_ner import extract_full_date
from NER.yargy_ner import extract_full_date

m = Mystem()


def lemmatize(s):
    global m
    try:
        return ''.join(m.lemmatize(s)).strip()
    except BrokenPipeError as ex:
        m = Mystem()
        return lemmatize(s)


def mystem_analyze(str):
    global m
    try:
        return m.analyze(str)
    except BrokenPipeError as ex:
        m = Mystem()
        return mystem_analyze(str)


def extract_users(text):
    return re.findall('(@[\w|\d]+)', text.lower())


count_names = 'один|два|три|четыре|пять|шесть|семь|восемь|девять|десять'.split('|')

weekdays = {'понедельник':0,'пн':0,
            'вторник':1,'вт':1,
            'среда':2,'ср':2,
            'четверг':3,'чт':3,
            'пятница':4,'пт':4,
            'суббота':5,'сб':5,
            'воскресенье':6,'вс':6}

weekdays_set = set('понедельник|пн|вторник|вт|среда|ср|четверг|чт|пятница|пт|суббота|сб|воскресенье|вс'.split('|'))


def next_weekday(d, weekday):
    days_ahead = weekday - d.weekday()
    if days_ahead <= 0: # Target day already happened this week
        days_ahead += 7
    return d + timedelta(days_ahead)


def extract_date(orig_text):
    text = lemmatize(orig_text.lower())
    digit_matches = re.search('(\\d+) (день|неделя|месяц|год)', text)
    word_matches = re.search('(один|два|три|четыре|пять|шесть|семь|восемь|девять|десять) (день|неделя|месяц|год)', text)
    next_matches = re.search('следующий (понедельник|пн|вторник|вт|среда|ср|четверг|чт|пятница|пт|суббота|сб|воскресенье|вс)', text)

    if 'послезавтра' in text:
        return datetime.now() + timedelta(days=2)
    elif 'завтра' in text:
        return datetime.now() + timedelta(days=1)
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
    elif next_matches:
        weekday_name = next_matches.group(1)
        return next_weekday(datetime.now(), weekdays[weekday_name])
    elif set(text.split()).intersection(weekdays_set):
        # take longer weekdays -- the longer more reliable =)
        w = max(set(text.split()).intersection(weekdays_set), key=lambda x: len(x))
        return next_weekday(datetime.now(), weekdays[w])

    # срок тебе неделя
    elif 'день' in text:
        return datetime.now() + timedelta(days=1)
    elif 'неделя' in text:
        return datetime.now() + timedelta(days=7)
    elif 'месяц' in text:
        return datetime.now() + timedelta(days=30)
    else:
        full_date = extract_full_date(orig_text.lower())
        if full_date:
            return full_date
        else:
            if is_asap(orig_text):
                return datetime.now() + timedelta(hours=3)

def is_email(text):
    return len(re.findall('^\\w+[.|\\w|\\d]+@\\w+[.|\\w|\\d]+$', text.lower().strip())) > 0


def is_imperative(s):
    for g in mystem_analyze(s):
        if 'analysis' in g:
            if len(g['analysis']) > 0:
                for gr in g['analysis']:
                    if 'пов' in gr['gr']:
                        return True
    return False

_asap_lemmatized_phrases = [lemmatize(phrase) for phrase in '''как можно скорее
сделай быстро
срочная задача
срочная проблема'''.split('\n')]
_asap_words = set('срочно важно асап asap'.split())

def is_asap(text):
    lem_text = lemmatize(text.lower())
    for phrase in _asap_lemmatized_phrases:
        if phrase in lem_text:
            return True
    words = set(lem_text.split())
    return len(words.intersection(_asap_words)) > 0


if __name__ == '__main__':
    tests = '''сделай к 4 февраля
даю тебе 4 дня на реализацию
код должен работать через 2 месяца начиная с сейчас    
срок тебе неделя
сделай к следующему четвергу
к следующему пн
сделай ко вт
завтра будет готово
надо чтобы было послезавтра
тут нет даты
эту задачу нужно сделать срочно'''
    print('now', datetime.now())
    for line in tests.splitlines():
        print(line)
        print(extract_date(line))
        print()

    print(extract_users('сообщи когда будут проблемы @tsundokum'))
    print(is_imperative('сообщи когда будут проблемы @tsundokum'))
    print(is_imperative('сообщишь когда будут проблемы @tsundokum'))

    assert is_email('alexander.vorontsov.msk@gmail.com')

    print()
    print('ASAP  tests:')
    print(is_asap('сделай срочно'))
    print(is_asap('ставлю срочную задачу'))
    print(is_asap('очередной срок'))
