import requests
from bs4 import BeautifulSoup as BS
import sys
import os
import datetime
import locale

sys.path.append('../../grasagrant')

os.environ['DJANGO_SETTINGS_MODULE'] = 'grasagrant.settings'
import django
django.setup()

from main.models import Category, Type, Grant

def parse_fcpir(url):

    response = requests.get(url)

    if response.status_code == 200:

        type_grant = Type.objects.get(name='fcpir')

        Grant.objects.filter(grant_name=type_grant).delete()
        
        soup = BS(response.text, features='html5lib')

        tr = soup.find('table', class_='contest').find_all('tr')

        for i in tr:

            grant = Grant()

            grant.grant_name = type_grant
            
            locale.setlocale(locale.LC_ALL, 'ru_RU.UTF-8')
            time = i.find('span', class_='gray').text
            time = time.lower().split(' ')

            if time[1].startswith('м') and time[1].endswith('я'):
                time[1] = time[1].replace('я', 'й')
            elif time[1].endswith('а'):
                time[1] = time[1][:-1]
            else:
                time[1] = time[1][:-1] + 'ь'

            time = ' '.join(i for i in time)

            grant.time = datetime.datetime.strptime(time, '%d %B %Y').date()
            grant.text = i.find('a').text
            grant.link = 'http://www.fcpir.ru' + i.find('a')['href']

            grant.save()

def main():
    
    url = 'http://www.fcpir.ru/events_and_publications/_contest/'

    parse_fcpir(url)

if __name__ == '__main__':
    main()