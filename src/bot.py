#!/usr/bin/env python3

import csv
import sys
import os
import json
import re
import requests
sys.path.insert(0, "summary/opennmt")
from datetime import datetime
from ir import is_task, is_trello_token
from summary import summorize
from NER.ner import extract_users, extract_date, is_email, is_imperative
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

    url = response['newCard']['shortUrl']
    text = 'Задача: ' + url
    if len(response['memberCardAmounts']) > 0:
        text = text + '\nЗадач:'
    for mc in response['memberCardAmounts']:
        text = text + '\n' + mc['email'] + ': ' + str(mc['cardsAmount'])

    write_to_telegram([chat_id, text, '', '', '', ''])

    if 'error' in response:
      error_text = 'Trello response error: ' + response['error']
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
    text = re.sub(r"@[\w|\d]+", "", text).strip()
    return summorize(text)

def format_body(text):
    return text.replace(KAZEMIR_MENTION, '')

def generate_invite_link(list_id):
    url = "https://api.trello.com/1/lists/" + list_id
    response = requests.request("GET", url)
    return 'https://trello.com/b/' + response.json()['idBoard'] + '/'

def process_message(chat_id, from_, from_mention, question):
    from_mention = '@' + from_mention

    list_id = chat_id2list_id(chat_id)
    token = chat_id2token(chat_id)

    if question.replace(KAZEMIR_MENTION, '').strip() == '/reset':
        TELEGRAM2TRELLO.clear()
        CHAT2TOKENS.clear()
        CHAT2LISTS.clear()
        return

    #print(question, file=sys.stderr)
    if (from_mention not in TELEGRAM2TRELLO) and is_email(question.replace(KAZEMIR_MENTION, '').strip()):
        TELEGRAM2TRELLO[from_mention] = question.replace(KAZEMIR_MENTION, '').strip()
        write_to_telegram([chat_id, snx, '', '','',''])
        return 

    if (list_id is None or token is None) and is_trello_token(question):
        CHAT2TOKENS[chat_id] = question.split(' ')[0]
        CHAT2LISTS[chat_id] = question.split(' ')[1]
        invite_link = generate_invite_link(question.split(' ')[1])
        write_to_telegram([chat_id, trello_list_added_text.format(invite_link), '', '','',''])
        return

    if from_ == chat_id:
        return

    if list_id is None or token is None:
        write_to_telegram([chat_id, trello_list_needed_text, '', 'd913ad0ce1614ffc56e34894b6ba56129b7adac621569d8304ec24b26264a258 5a854bc62886329b30215906','',''])
        return
        
    contains_mention = len(re.findall('@\w+', question)) > 0 
    if not contains_mention:
        return
    strut_rule = contains_mention and is_imperative(question)
    if (not is_task(question) and not strut_rule) and KAZEMIR_MENTION not in question:
        return

    summary = gen_summary(question)
    text = format_body(question)
    assignees = []
    unknown_telegram_users = []
    for user in extract_users(question):
        if user in TELEGRAM2TRELLO:
            assignees.append(TELEGRAM2TRELLO[user])
        else:
            if user != KAZEMIR_MENTION:
                unknown_telegram_users.append(user)

    if len(unknown_telegram_users) > 0:
        write_to_telegram([chat_id, user_email_needed.format(','.join(unknown_telegram_users)), '', '','',''])
        
    due_date = extract_date(question)

    try:
        write_task(token, list_id, summary, text, assignees, due_date, chat_id)
    except Exception as e:
        print(e, file=sys.stderr)

def main():
    for row in csv.reader(iter(sys.stdin.readline, '')):
        chat_id, from_, from_mention, question = row[0], row[1], row[2], row[3]
        process_message(chat_id, from_, from_mention, question)

if __name__ == "__main__":
    main()
