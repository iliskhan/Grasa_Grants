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

from main.models import Category, Type, DigitalEconomy

def digital_parse(url):

    data = []
    
    response = requests.get(url)

    if response.status_code == 200:

        soup = BS(response.text, features='html5lib')

        posts = soup.find('div', class_='col-md-8').find_all('div', class_='document-link-block')
        
        for post in posts:

            current_data = {}
            
            document_number = post.find('span', class_='document-number')
            
            current_data['document_number'] = document_number.text.strip().replace(u'\xa0', " ") if document_number else None  
            
            doc_header = post.find('div', class_='document-link-block-header')    
            doc_info_arr = doc_header.find_all('span', class_='document-info')

            current_data['label'] = doc_info_arr[0].text.strip()
            current_data['date'] = date_conversion(doc_info_arr[1].text.strip()) if len(doc_info_arr) == 2 else None

            current_data['text'] = post.find('a').text.strip()
            current_data['link'] = 'https://digital.gov.ru' + post.find('a')['href']

            data.append(current_data)

    return data

def date_conversion(date):

    locale.setlocale(locale.LC_ALL, 'ru_RU.UTF-8')

    date = date.lower().split(' ')
    if date[1].startswith('м') and date[1].endswith('я'):
                date[1] = date[1].replace('я', 'й')
    elif date[1].endswith('а'):
        date[1] = date[1][:-1]
    else:
        date[1] = date[1][:-1] + 'ь'

    date = ' '.join(i for i in date)
    date = datetime.datetime.strptime(date, '%d %B %Y').date()
    
    return date

def main():

    DigitalEconomy.objects.all().delete()

    url = 'https://digital.gov.ru/ru/documents/'

    data = digital_parse(url)

    category = Category.objects.get(tab_name='DigitalEconomy').pk
    types = Type.objects.filter(category=category)

    for d in data:

        digital_economy = DigitalEconomy(
            type_name = types.get(name=d['label']),
            document_number = d['document_number'],
            date = d['date'],
            text = d['text'],
            link = d['link'],

        )

        digital_economy.save()

if __name__ == '__main__':
    main()    