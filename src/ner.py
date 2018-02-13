#!/usr/bin/env python3

import sys
from natasha import NamesExtractor, DatesExtractor, MoneyExtractor, AddressExtractor, OrganisationExtractor 

dates_extractor = DatesExtractor() 
name_extractor = NamesExtractor() 
money_extractor = MoneyExtractor()
organization_extractor = OrganisationExtractor() 
address_extractor = AddressExtractor()

for line in sys.stdin:
    matches = dates_extractor(line)
    facts = []
    for match in matches:
        facts.append(match.fact)
    print(facts)
