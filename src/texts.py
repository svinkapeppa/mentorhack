trello_list_needed_text = '''Необходимо вас зарегистрировать! Для этого:
        - следите, чтобы у всех членов команды был установлен логин в профиле telegram
        - перейдите на https://trello.com/1/authorize?expiration=never&name=MentorBot&key=09ee14411f546915a65d690b1a8d36b0&response_type=token&scope=read,write,account
        - нажмите "ALLOW"
        - запомните токен
        - откройте или создайте доску в https://trello.com и в URL браузера замените имя доски на report.json
        - вы получите описание вашей доски в JSON, найдите объект списка с нужным вам именем (поле name)
        - запомните ид списка
        - пришлите в чат сообщение в формате <токен> <имя списка> 
        Или для демонстрации можете воспользоваться нашей тестовой доской просто нажав на кнопку. Все члены команды должны будут добавиться в доску, ссылка на приглашение: https://trello.com/invite/b/7usXnKsV/838e400c012e4023de2e52041cafda5f/mentorhack
    '''

trello_list_added_text = 'Ссылка на доску в Trello: {} . Все члены команды должны быть добавлены в доску админом и написать мне или в чат свою почту'
user_email_needed = '{} напишите мне свою почту и не забудьте добавиться в тасктрекер. А то я не могу добавлять вас в задачу!'
snx = 'Спасибо!'
