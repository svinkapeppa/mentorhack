from natasha.grammars.date import DAY, MONTH_NAME, YEAR, MONTH
from yargy import or_, rule, Parser
from datetime import datetime


from yargy import fact


Date = fact(
    'Date',
    ['year', 'month', 'day']
)


DATE = or_(
    rule(
        DAY.interpretation(
            Date.day
        ),
        MONTH_NAME.interpretation(
            Date.month
        ),
        YEAR.interpretation(
            Date.year
        )
    ),
    rule(
        DAY.interpretation(
            Date.day
        ),
        MONTH_NAME.interpretation(
            Date.month
        )
    ),
    rule(
        YEAR.interpretation(
            Date.year
        ),
        '-',
        MONTH.interpretation(
            Date.month
        ),
        '-',
        DAY.interpretation(
            Date.day
        )
    ),
).interpretation(
    Date
).named('DATE')

text = '''Мне нужно, чтобы это было сделано через 2 дня
ожидаю, что сегодня будет сделано
нужно распарсить вс е форумы к завтрашнему дню
назначим встречу на завтра
послезавтра хочется, чтобы уже было
к четвергу
к следующей субботе
к концу недели кто-нибудь сделает?
дедлайн следующий понедельник
даю на выполнение задачи 3 дня
ожидаю, что это будет сделано к часу дня
к концу месяца
к 1 Март должно быть готово
жду ответ 6 Января
к маю должно быть готово'''

parser = Parser(DATE)


month_order = 'январь февраль март апрель май июнь июль август сентябрь октябрь ноябрь декабрь'.split()


def extract_full_date(s):
    matches = list(parser.extract(s))
    if not matches:
        return
    for ma in matches:
        day = ma.fact.day or 1
        month = month_order.index(ma.fact.month) + 1
        year = ma.fact.year
        if year is None:
            now = datetime.now()
            year = now.year
            dt = datetime(year, month, day)
            if dt < now:
                year += 1
                return datetime(year, month, day)
            else:
                return dt

        return datetime(year, month, day)

if __name__ == '__main__':
    for line in text.splitlines():
        print(extract_full_date(line))
