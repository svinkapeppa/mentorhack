#!/usr/bin/env python3

import csv
import sys
sys.path.insert(0, "summary/opennmt")
from datetime import datetime
from ir import is_task, is_trello_token
from summary import summorize
from ner import extract_users, extract_date
from texts import trello_list_needed_text, trello_list_added_text

CHAT2LISTS = {}
CHAT2TOKENS = {}
TELEGRAM2TRELLO = {}

def write_task(token, list_id, summary, text, assignees, due_date):
    #TODO subprocess
    print([token, list_id, summary, text, ','.join(assignees), due_date.date().isoformat()], file=sys.stderr)

def chat_id2list_id(chat_id):
    if chat_id in CHAT2LISTS:
        return CHAT2LISTS[chat_id]
    else:
        return None

def chat_id2token(chat_id):
    if chat_id in CHAT2TOKENS:
        return CHAT2TOKENS[chat_id]
    else:
        return None

def users2assignees(users):
    res = []
    for telegram in users:
        if telegram in TELEGRAM2TRELLO:
            res.append(TELEGRAM2TRELLO[telegram])
    return res

def gen_summary(text):
    return summorize(text)

def format_body(text):
    return text

def main():
    telegram_gate = csv.writer(sys.stdout, quoting=csv.QUOTE_NONNUMERIC)
    for row in csv.reader(iter(sys.stdin.readline, '')):
        chat_id, form, question = row[0], row[1], row[2]

        list_id = chat_id2list_id(chat_id)
        token = chat_id2token(chat_id)
        
        if (list_id is None or token is None) and is_trello_token(question):
            CHAT2TOKENS[chat_id] = question.split(' ')[0]
            CHAT2LISTS[chat_id] = question.split(' ')[1]
            telegram_gate.writerow([chat_id, trello_list_added_text, '', '','',''])
            continue

        if list_id is None or token is None:
            telegram_gate.writerow([chat_id, trello_list_needed_text.strip(), '', '','',''])
            continue
            
        if not is_task(question):
            continue

        summary = gen_summary(question)
        text = format_body(question)
        assignees = users2assignees(extract_users(question))
        due_date = extract_date(question)

        write_task(token, list_id, summary, text, assignees, due_date)

if __name__ == "__main__":
    main()
