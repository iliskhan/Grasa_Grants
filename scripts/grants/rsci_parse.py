import requests
from bs4 import BeautifulSoup as BS
import sys
import os
import datetime

sys.path.append('../../grasagrant')

os.environ['DJANGO_SETTINGS_MODULE'] = 'grasagrant.settings'
import django
django.setup()

from main.models import Category, Type, Grant, Link

def rsci_parse(url):

    response = requests.get(url)

    if response.status_code == 200:

        type_grant = Type.objects.get(name='rsci')

        Grant.objects.filter(grant_name=type_grant).delete()

        soup = BS(response.text, features='html5lib')

        posts = soup.find_all(class_='col l4 m6 s12')
        
        for post in posts:

            grant = Grant()

            grant.grant_name = type_grant

            time = ''.join(f"{post.find_all('span')[0].text}.{post.find_all('span')[1].text}")
            time = datetime.datetime.strptime(time, '%d.%m.%Y').date()
            time = time.strftime('%Y-%m-%d')

            grant.time = datetime.datetime.strptime(time, '%Y-%m-%d').date()
            grant.text = post.find('div', 'info-card-deskription').find('h4', class_='text-title').text  
            grant.link = 'http://www.rsci.ru' + post.find('div', 'info-card-deskription').find('a')['href']
            
            fond = post.find('div', class_='info-title')
            if fond:
                grant.fond = fond.text
            
            fond_link = post.find('div', class_='info-title').find('a')
            if fond_link:
                grant.fond_link = 'http://www.rsci.ru' + fond_link['href']
                
            grant.save()         

def main():

    url = 'http://www.rsci.ru/grants/'

    rsci_parse(url)

if __name__ == '__main__':
    main()    