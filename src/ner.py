import sys
import re
from natasha import NamesExtractor, DatesExtractor, MoneyExtractor, AddressExtractor, OrganisationExtractor 
from pymystem3 import Mystem
from datetime import datetime

dates_extractor = DatesExtractor() 
name_extractor = NamesExtractor() 
money_extractor = MoneyExtractor()
organization_extractor = OrganisationExtractor() 
address_extractor = AddressExtractor()
m = Mystem()

m = Mystem()

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
    text = m.lemmatize(text)
    matches = re.search('@\d+ день|неделя|месяц|год', text)

    if 'завтра' in text:
        return datetime.now() + datetime.timedelta(days=1)
    elif 'послезавтра' in text:
        return datetime.now() + datetime.timedelta(days=2) 
    elif text == 'один неделя':
        return datetime.now() + datetime.timedelta(weeks=1) 
    elif text == 'два неделя':
        return datetime.now() + datetime.timedelta(weeks=2)       
    elif text == 'один день':
        return datetime.now() + datetime.timedelta(days=1)     
    elif text == 'два день':
        return datetime.now() + datetime.timedelta(days=2)     
    elif text == 'три день':
        return datetime.now() + datetime.timedelta(days=3)                     
    elif text == 'один месяц':
        return datetime.now() + datetime.timedelta(month=1)                         
    elif len(matches) > 0: #regex check
        return ???
    elif text == 'день':
        return datetime.now() + datetime.timedelta(day=1)                         
    elif text == 'неделя': 
        return datetime.now() + datetime.timedelta(week=1)                         
    elif text == 'месяц':
        return datetime.now() + datetime.timedelta(month=1)                         
    else: #natasha
        pass

    facts = []
    for match in matches:
        return match.fact
