import requests
from bs4 import BeautifulSoup as BS
import sys
from os import path, environ
import datetime
import locale

abs_path = path.join(path.dirname(path.dirname(path.dirname(path.abspath(__file__)))), 'grasagrant')
sys.path.append(abs_path)

environ['DJANGO_SETTINGS_MODULE'] = 'grasagrant.settings'
import django
django.setup()

from main.models import Category, Type, DigitalEconomy

# from main.services import clean_digitaleconomy

def digital_parse(url):

    page_number = 1

    while True:
    
        response = requests.get(f'{url}?words=&type=&directions=&department=&start_date=&end_date=&page={page_number}')
        
        category = Category.objects.get(tab_name='DigitalEconomy').pk
        types = Type.objects.filter(category=category)

        if response.status_code == 200:

            soup = BS(response.text, features='html5lib')

            posts = soup.find('div', class_='col-md-8').find_all('div', class_='document-link-block')

            if posts:
        
                for post in posts:

                    text = post.find('a').text.strip()
                    link = 'https://digital.gov.ru' + post.find('a')['href']

                    if DigitalEconomy.objects.filter(text=text, link=link).exists():
                        return 

                    document_number = post.find('span', class_='document-number')

                    doc_header = post.find('div', class_='document-link-block-header')    
                    doc_info_arr = doc_header.find_all('span', class_='document-info')

                    if doc_info_arr:
                        
                        try:

                            type_post = types.get(name=doc_info_arr[0].text.strip())
                            
                            digital_economy = DigitalEconomy()
                            digital_economy.digitaleconomy_name = type_post
                        
                            if len(doc_info_arr) == 2: digital_economy.date = date_conversion(doc_info_arr[1].text.strip())
                            
                            if document_number: digital_economy.document_number = document_number.text.strip().replace(u'\xa0', " ")  

                            digital_economy.text = text
                            digital_economy.link = link
                            digital_economy.save()

                        except Type.DoesNotExist:
                            pass
            else:
                break
        else:
            break
        
        page_number += 1

def date_conversion(date):
    
    dict_month = {
        'января' : '1', 'февраля' : '2',
        'марта' : '3', 'апреля' : '4', 
        'мая' : '5', 'июня' : '6', 
        'июля' : '7', 'августа' : '8', 
        'сентября' : '9', 'октября' : '10', 
        'ноября' : '11', 'декабря' : '12'
    }

    date = date.lower().split(' ')

    date[1] = dict_month.get(date[1])
    date = ' '.join(i for i in date)    
    date = datetime.datetime.strptime(date, '%d %m %Y').date()
    
    return date

def main():

    # clean_digitaleconomy()

    url = 'https://digital.gov.ru/ru/documents/'

    digital_parse(url)

if __name__ == '__main__':
    main()    