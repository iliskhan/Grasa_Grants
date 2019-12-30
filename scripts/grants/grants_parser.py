import requests
from requests_html import HTMLSession
from bs4 import BeautifulSoup as BS
import sys
import os
import datetime, time
import locale

sys.path.append('../../grasagrant')

os.environ['DJANGO_SETTINGS_MODULE'] = 'grasagrant.settings'
import django
django.setup()

from main.models import Category, Type, Grant, Link

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
            grant.time = datetime.datetime.strptime(time, '%d.%m.%Y').date()

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
            grant.time = datetime.datetime.strptime(time, '%d.%m.%Y').date()
            
            text = post.find_all('p')
            grant.text = ' '.join(i.text.strip() for i in text)
            
            grant.save() 

            doc_link = post.find_all('p')
            doc_link = [i.find('a') for i in doc_link]
            
            for doc in doc_link:
                if doc is not None: 

                    doc = doc['href']
                    
                    if doc.endswith('.pdf') or doc.endswith('.doc'):

                        link = Link()
                        link.grant_id = grant
                        link.link = doc
                        
                        link.save()             


def fcpir_parse(url):

    response = requests.get(url)

    if response.status_code == 200:

        type_grant = Type.objects.get(name='fcpir')
        Grant.objects.filter(grant_name=type_grant).delete()
        
        soup = BS(response.text, features='html5lib')
        tr = soup.find('table', class_='contest').find_all('tr')

        for i in tr:

            grant = Grant()
            grant.grant_name = type_grant
            
            time = i.find('span', class_='gray').text
            grant.time = date_conversion(time)
            grant.text = i.find('a').text
            grant.link = 'http://www.fcpir.ru' + i.find('a')['href']

            grant.save()


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
                grant.time = datetime.datetime.strptime(time, '%d.%m.%Y').date()
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

            grant.time = datetime.datetime.strptime(time, '%d.%m.%Y').date()
            grant.text = post.find('div', 'info-card-deskription').find('h4', class_='text-title').text  
            grant.link = 'http://www.rsci.ru' + post.find('div', 'info-card-deskription').find('a')['href']
            
            fond = post.find('div', class_='info-title')
            if fond:
                grant.fond = fond.text
            
            fond_link = post.find('div', class_='info-title').find('a')
            if fond_link:
                grant.fond_link = 'http://www.rsci.ru' + fond_link['href']
                
            grant.save()      


def edu_parse(url):

    session = HTMLSession()
    response = session.get(url)

    if response.status_code == 200:

        type_grant = Type.objects.get(name='edu')
        Grant.objects.filter(grant_name=type_grant).delete()

        response.html.render(timeout=30)

        soup = BS(response.html.html, features="lxml")
        doc_list = soup.find_all("div", class_="section page-main__searchresult-item")

        for doc in doc_list:

            grant = Grant()
            grant.grant_name = type_grant

            time = doc.find('div', class_='date page-main__searchresult-item-meta-date mr-2 pr-2').text.strip()      
            grant.time = date_conversion(time)

            grant.text = doc.find('a').text.strip()
            grant.link = doc.find('a')['href']
            grant.label = doc.find('div', class_='d-flex').find_all('div')[1].text.strip()

            grant.save()
    
    # session.close()    
     
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

    science_parse('https://4science.ru/finsupports')
    cbias_parse('http://www.cbias.ru/')
    fcpir_parse('http://www.fcpir.ru/events_and_publications/_contest/')
    minobrnauki_parse('https://www.minobrnauki.gov.ru/ru/documents/docs/index.php')
    rsci_parse('http://www.rsci.ru/grants/') 
    edu_parse('https://docs.edu.gov.ru/')  

if __name__ == '__main__':
    main()    