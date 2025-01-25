import json
import datetime

import requests
from bs4 import BeautifulSoup

import config

def get_current_date():
    now = datetime.datetime.now()
    return now.strftime("%d-%m-%Y")

def format_date(date):
    return date.strftime("%d-%m-%Y")

def format_multiple_dates(initial, days):
    dates = []
    for i in range(days):
        date = initial - datetime.timedelta(days=i)
        dates.append(date.strftime("%d-%m-%Y"))
    return dates

def get_diario_as_json(date=None):
    if date is None:
        date = get_current_date()
    url = config.BASE_DOU3_URL.format(date=date)
    print(url)
    response = requests.get(url, timeout=30)
    body = response.text
    print('aa')
    soup = BeautifulSoup(body, features="html.parser")
    diario = soup.find("script", {"id":"params"})
    print('bb')
    diario = json.loads(diario.text)
    print('cc')
    return diario



def get_pub_complete_content(url_id):
    url = config.BASE_PUB_DETAIL_URL+url_id
    print(url)
    try:
        response = requests.get(url)
        body = response.text
        
        soup = BeautifulSoup(body, features="html.parser")
        diario = soup.find("div", {"class":"texto-dou"})
        return diario.text
    except Exception as e:
        if config.DEBUG:
            print("ERROR - get_pub_complete_content: ", e.__class__, e)
            
    return ''
    
