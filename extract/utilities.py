import datetime

def date_formating(date):
    MONTHS = {'enero': '01',
    'febrero': '02',
    'marzo': '03',
    'abril': '04',
    'mayo': '05',
    'junio': '06',
    'julio': '07',
    'agosto': '08',
    'septiembre': '09',
    'octubre': '10',
    'noviembre': '11',
    'diciembre': '12'
    }
    date = date.split(" ")
    date = date[-1] + "-" + MONTHS[date[2]] + "-" + date[0]
    return date