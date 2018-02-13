#!/usr/bin/env python3
import csv
import sys
from datetime import datetime
from ir import is_task

BOARDS = {}
writer = csv.writer(sys.stdout, quoting=csv.QUOTE_NONNUMERIC)

def write_task(listd_id, summary, text, assignee, due_date):
    writer.writerow([list_id, summary, text, assignee, due_date.timestamp()])

def chat_id2list_id(chat_id):
    return 'STUB'

def user2assignee(userId):
    return 'bavadim@gmail.com'

def extract_user(text):
    return 'vad'

def extract_date(text):
    return datetime.now()

def gen_summary(text):
    return 'STUB'

def format_body(text):
    return text

for row in csv.reader(iter(sys.stdin.readline, '')):
    chat_id, form, question = row[0], row[1], row[2]
    if not is_task(question):
        continue

    list_id = chat_id2list_id(chat_id)
    summary = gen_summary(question)
    text = format_body(question)
    assignee = user2assignee(extract_user(question))
    due_date = extract_date(question)

    write_task(list_id, summary, text, assignee, due_date)
    sys.stdout.flush() 
