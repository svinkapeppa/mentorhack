trello_list_needed_text = '''необходимо вас зарегистрировать! Для этого:
        - перейдите на https://trello.com/1/authorize?expiration=never&name=MentorBot&key=09ee14411f546915a65d690b1a8d36b0&response_type=token&scope=read,write,account
        - нажмите "ALLOW"
        - запомните токен
        - откройте или создайте доску в https://trello.com и в URL браузера замените имя доски на report.json
        - вы получите описание вашей доски, найдите объект списка с нужным вам именем (поле name)
        - запомните ид списка
        - пришлите в чат сообщение в формате <токен> <имя списка> 
        - следите, чтобы у всех членов команды был установлен логин в профиле telegram
    '''

trello_list_added_text = 'Ссылка-приглашение в Trello: {} . Все члены команды должны перейти по ней и написать мне или в чат свою почту, указанную в Trello.'
user_email_needed = '{} напишите мне свою почту и не забудьте добавится в тасктрекер. А то я не могу добавлять вас в задачу!'
snx = 'спасибо!'
