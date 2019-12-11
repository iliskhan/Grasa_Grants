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

def science_parse(url):

    response = requests.get(url, verify=False)

    if response.status_code == 200:

        type_grant = Type.objects.get(name='4science')

        Grant.objects.filter(grant_name=type_grant).delete()

        soup = BS(response.text, features='html5lib')

        posts = soup.find('div', id='fin-supports-list-inner').find_all('a', class_='fin-list')
        
        for post in posts:
            
            grant = Grant()

            grant.grant_name = type_grant

            time = post.find('span', class_='fin-list-date').text
            time = datetime.datetime.strptime(time, '%d.%m.%Y').date()
            time = time.strftime('%Y-%m-%d')

            grant.time = datetime.datetime.strptime(time, '%Y-%m-%d').date()
            grant.label = post.find('div', class_='fin-list-label').text.strip()
            
            div_text = post.find('div', class_='fin-list-title')
            div_text.span.decompose()   

            grant.text = div_text.text.strip()                
            grant.link = 'https://4science.ru' + post['href']

            info = post.find('div', class_='fin-list-info')

            org = info.find_all('div', class_='fin-list-info-in-last')
            if org:
                grant.org = org[0].text.strip()

            for i in org:
                i.decompose()    

            days = info.find('div', class_='fin-list-location')
            if days:
                grant.days = days.text.strip()

            days.decompose()

            rouble = info.find('div', class_='fin-list-info-in')
            
            if rouble:
                rouble.span.decompose()
                grant.rouble = rouble.text.strip()
                
            grant.save()    
  

def main():

    url = 'https://4science.ru/finsupports'

    science_parse(url)

if __name__ == '__main__':
    main()    