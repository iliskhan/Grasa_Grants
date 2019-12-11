import requests
from bs4 import BeautifulSoup as BS 
import sys
import os
import datetime

sys.path.append('../../grasagrant')

os.environ['DJANGO_SETTINGS_MODULE'] = 'grasagrant.settings'
import django
django.setup()

from main.models import Category, Type, Grant

def cbias_parse(url):

    response = requests.get(url)

    if response.status_code == 200:

        type_grant = Type.objects.get(name='cbias')

        Grant.objects.filter(grant_name=type_grant).delete()

        soup = BS(response.text, features='html5lib')

        posts = soup.find_all(class_='post_inner')

        for post in posts:

            grant = Grant()
            
            grant.grant_name = type_grant

            time = post.find('div', class_='post_date').text
            time = datetime.datetime.strptime(time, '%d.%m.%Y').date()
            time = time.strftime('%Y-%m-%d')
            
            grant.time = datetime.datetime.strptime(time, '%Y-%m-%d').date()
            grant.text = post.find_all('p')[0].text
            grant.link = post.find_all('p')[0].find('a')['href']
            
            grant.save()       

def main():

    url = 'http://www.cbias.ru/'

    cbias_parse(url)

if __name__ == '__main__':
    main()    