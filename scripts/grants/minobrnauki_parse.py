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

def minobrnauki_parse(url):

    response = requests.get(url, verify=False)
    
    if response.status_code == 200:

        type_grant = Type.objects.get(name='minobrnauki')

        Grant.objects.filter(grant_name=type_grant).delete()
        
        soup = BS(response.text, features='html5lib')
        
        li = soup.find("ul", class_="anons-list_docs").find_all("li")

        if li:

            for i in li:
                
                grant = Grant()

                grant.grant_name = type_grant

                time = i.find("time").text
                time = datetime.datetime.strptime(time, '%d.%m.%Y').date()
                time = time.strftime('%Y-%m-%d')

                grant.time = datetime.datetime.strptime(time, '%Y-%m-%d').date()
                grant.link = 'https://www.minobrnauki.gov.ru' + i.find("a")['href']
                grant.text = i.find("a").text

                grant.save()

                doc_links = i.find('div', class_='doc-links')
                
                if doc_links is not None:
                    
                    for i in doc_links.find_all('a'):
                        
                        link = Link()

                        link.link = 'https://www.minobrnauki.gov.ru'+i['href']

                        link.grant_id = grant

                        link.save()

def main():

    url = 'https://www.minobrnauki.gov.ru/ru/documents/docs/index.php'

    minobrnauki_parse(url)
    
if __name__ == '__main__':
    main()    