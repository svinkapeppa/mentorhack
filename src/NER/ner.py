import sys
import re
from natasha import NamesExtractor, DatesExtractor, MoneyExtractor, AddressExtractor, OrganisationExtractor
from natasha.extractors import Extractor
from pymystem3 import Mystem
from datetime import datetime, timedelta

# from date_grammar import DATE

dates_extractor = DatesExtractor() 
name_extractor = NamesExtractor() 
money_extractor = MoneyExtractor()
organization_extractor = OrganisationExtractor() 
address_extractor = AddressExtractor()

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
    matches = re.search('@\w+', text)
    res = []
    for m in matches:
        res.append(m)
    return res


def extract_date(text):
    text = lemmatize(text)
    matches = re.search('\d+ день|неделя|месяц|год', text)

    if 'завтра' in text:
        return datetime.now() + timedelta(days=1)
    elif 'послезавтра' in text:
        return datetime.now() + timedelta(days=2)
    elif text == 'один неделя':
        return datetime.now() + timedelta(weeks=1)
    elif text == 'два неделя':
        return datetime.now() + timedelta(weeks=2)
    elif text == 'один день':
        return datetime.now() + timedelta(days=1)
    elif text == 'два день':
        return datetime.now() + timedelta(days=2)
    elif text == 'три день':
        return datetime.now() + timedelta(days=3)
    elif text == 'один месяц':
        return datetime.now() + timedelta(month=1)
    elif len(matches) > 0: #regex check
        return  # TODO
    elif text == 'день':
        return datetime.now() + timedelta(day=1)
    elif text == 'неделя': 
        return datetime.now() + timedelta(week=1)
    elif text == 'месяц':
        return datetime.now() + timedelta(month=1)
    else: #natasha
        pass

    facts = []
    for match in matches:
        return match.fact


# class MyDatesExtractor(Extractor):
#     def __init__(self):
#         super(MyDatesExtractor, self).__init__(DATE)
# de = MyDatesExtractor()
# res = de('к 1 февраля')
# print(len(res))
# print(res[0])

print(extract_date('завтра'))