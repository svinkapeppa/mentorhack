#!/usr/bin/env python3

import csv
import sys
import os
import json
sys.path.insert(0, "summary/opennmt")
from datetime import datetime
from ir import is_task, is_trello_token
from summary import summorize
from NER.ner import extract_users, extract_date, is_email
from texts import trello_list_needed_text, trello_list_added_text, user_email_needed, snx

KAZEMIR_MENTION = "@mentor_assist_bot"
CHAT2LISTS = {}
CHAT2TOKENS = {}
TELEGRAM2TRELLO = {}

telegram_gate = csv.writer(sys.stdout, quoting=csv.QUOTE_NONNUMERIC)
def write_to_telegram(arr):
    telegram_gate.writerow(arr)
    sys.stdout.flush()

def write_task(token, list_id, summary, text, assignees, due_date, chat_id):
    if due_date is None:
        due_date = ""
    else:
        due_date = due_date.date().isoformat()

    payload = [token, list_id, summary, text, ','.join(assignees), due_date]

    to_exec = "echo '" + json.dumps(payload) + "' | " + os.getcwd() + "/totrello/index.js"
    response = json.loads(os.popen(to_exec).read())

    #print(response, file=sys.stderr)
    url = response['newCard']['shortUrl']
    write_to_telegram([chat_id, url, '', '', '', ''])

    error = response['error']

    if error:
      error_text = 'Trello response error: ' + error
      write_to_telegram([chat_id, error_text, '', '', '', ''])

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

def process_message(chat_id, from_, from_mention, question):
    from_mention = '@' + from_mention

    list_id = chat_id2list_id(chat_id)
    token = chat_id2token(chat_id)
    
    if chat_id == from_ and from_mention not in TELEGRAM2TRELLO and is_email(question):
        TELEGRAM2TRELLO[from_mention] = question
        write_to_telegram([chat_id, snx, '', '','',''])

    if (list_id is None or token is None) and is_trello_token(question):
        CHAT2TOKENS[chat_id] = question.split(' ')[0]
        CHAT2LISTS[chat_id] = question.split(' ')[1]
        write_to_telegram([chat_id, trello_list_added_text, '', '','',''])
        continue

    if list_id is None or token is None:
        write_to_telegram([chat_id, trello_list_needed_text, '', '','',''])
        continue
        
    if not is_task(question) and KAZEMIR_MENTION not in question:
        continue

    summary = gen_summary(question)
    text = format_body(question)
    assignees = []
    unknown_telegram_users = []
    for user in extract_users(question):
        if user in TELEGRAM2TRELLO:
            if user != KAZEMIR_MENTION:
                assignees.append(TELEGRAM2TRELLO[user])
        else:
            unknown_telegram_users.append(user)

    if len(unknown_telegram_users) > 0:
        write_to_telegram([chat_id, user_email_needed.format(','.join(unknown_telegram_users)), '', '','',''])
        
    due_date = extract_date(question)

    write_task(token, list_id, summary, text, assignees, due_date, chat_id)

def main():
    for row in csv.reader(iter(sys.stdin.readline, '')):
        chat_id, from_, from_mention, question = row[0], row[1], row[2], row[3]
        process_message(chat_id, from_, from_mention, question)

if __name__ == "__main__":
    main()
