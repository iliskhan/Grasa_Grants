from requests_html import HTMLSession
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

def edu_parse(url):

    session = HTMLSession()

    response = session.get('https://docs.edu.gov.ru/')

    if response.status_code == 200:

        type_grant = Type.objects.get(name='edu')

        Grant.objects.filter(grant_name=type_grant)

        response.html.render()

        soup = BS(response.html.html, features="lxml")

        doc_list = soup.find_all("div", class_="section page-main__searchresult-item")

        for doc in doc_list:

            grant = Grant()

            grant.grant_name = type_grant

            locale.setlocale(locale.LC_ALL, 'ru_RU.UTF-8')
            time = doc.find('div', class_='date page-main__searchresult-item-meta-date mr-2 pr-2').text.strip()
            time = time.lower().split(' ')

            if time[1].startswith('м') and time[1].endswith('я'):
                time[1] = time[1].replace('я', 'й')
            elif time[1].endswith('а'):
                time[1] = time[1][:-1]
            else:
                time[1] = time[1][:-1] + 'ь'

            time = ' '.join(i for i in time)          
            
            grant.time = datetime.datetime.strptime(time, '%d %B %Y').date()
            grant.text = doc.find('a').text.strip()
            grant.link = doc.find('a')['href']
            grant.label = doc.find('div', class_='d-flex').find_all('div')[1].text.strip()

            grant.save()

def main():

    url = 'https://docs.edu.gov.ru/'

    edu_parse(url)

if __name__ == '__main__':
    main()    