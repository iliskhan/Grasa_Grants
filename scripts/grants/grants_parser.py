import requests
from requests_html import HTMLSession
from bs4 import BeautifulSoup as BS
import sys
from os import environ, path
import datetime, time

abs_path = path.join(path.dirname(path.dirname(path.dirname(path.abspath(__file__)))), 'grasagrant')
sys.path.append(abs_path)

environ['DJANGO_SETTINGS_MODULE'] = 'grasagrant.settings'
import django
django.setup()

from main.models import Category, Type, Grant, Link

from main.services import clean_4science, clean_grant

def science_parse(url):

    page_number = 1

    type_grant = Type.objects.get(name='4science')
    clean_4science(type_grant)

    while True:

        response = requests.get(f'{url}?view=list&page={page_number}', verify=False)

        if response.status_code == 200:

            soup = BS(response.text, features='html5lib')
            posts = soup.find('div', id='fin-supports-list-inner').find_all('a', class_='fin-list')
            
            if posts:
        
                for post in posts:

                    time = post.find('span', class_='fin-list-date').text
                    time = datetime.datetime.strptime(time, '%d.%m.%Y').date()
                    div_text = post.find('div', class_='fin-list-title')
                    div_text.span.decompose()
                    text = div_text.text.strip()

                    if Grant.objects.filter(grant_name=type_grant, text=text, time=time).exists():                     
                        return
                    
                    grant = Grant()

                    grant.grant_name = type_grant
                    grant.time = time
                    grant.label = post.find('div', class_='fin-list-label').text.strip()
                    grant.text = text          
                    grant.link = 'https://4science.ru' + post['href']

                    info = post.find('div', class_='fin-list-info')
                    org = info.find_all('div', class_='fin-list-info-in-last')
                    if org:
                        grant.org = org[0].text.strip()

                    for i in org:
                        i.decompose()    

                    days = info.find('div', class_='fin-list-location')
                    if days:
                        grant.days = days.text.strip().split()[0]
                        days.decompose()

                    rouble = info.find('div', class_='fin-list-info-in')
                    
                    if rouble:
                        rouble.span.decompose()
                        grant.rouble = rouble.text.strip()
                        
                    grant.save()

            else:
                break
        else:
            break

        page_number += 1


def cbias_parse(url):

    page_number = 1

    type_grant = Type.objects.get(name='cbias')
    clean_grant(type_grant)

    while True:

        try:
            response = requests.get(f'{url}page/{page_number}/')

        except requests.exceptions.RequestException as e:
            print(e)
            break
        
        if response.status_code == 200:

            soup = BS(response.text, features='html5lib')
            posts = soup.find_all(class_='post_inner')

            if posts:

                for post in posts:

                    text = post.find_all('p')
                    text = ' '.join(i.text.strip() for i in text)
                    time = post.find('div', class_='post_date').text
                    time = datetime.datetime.strptime(time, '%d.%m.%Y').date()     
                    
                    if Grant.objects.filter(grant_name=type_grant, text=text, time=time).exists():

                        return
                
                    grant = Grant()

                    grant.grant_name = type_grant                   
                    grant.time = time     
                    grant.text = text                   
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
            else:
                break
        else:
            break
    
        page_number += 1

def fcpir_parse(url):

    page_number = 1

    type_grant = Type.objects.get(name='fcpir')
    clean_grant(type_grant)

    while True:

        response = requests.get(f'{url}?PAGEN_1={page_number}')
        
        if response.status_code == 200:
        
            soup = BS(response.text, features='html5lib')
            tr = soup.find('table', class_='contest').find_all('tr')

            for i in tr:

                text = i.find('a').text
                time = i.find('span', class_='gray').text
                time = date_conversion(time)

                if Grant.objects.filter(grant_name=type_grant, text=text, time=time).exists():
                    return
                
                grant = Grant()
                grant.grant_name = type_grant
                
                grant.time = time
                grant.text = text
                grant.link = 'http://www.fcpir.ru' + i.find('a')['href']
                grant.save()

            pagination = soup.find('div', class_='pagination')           
            if pagination.find('span', class_='pagination__next _disabled') is not None:
                break
        else:
            break

        page_number += 1


def minobrnauki_parse(url):

    page_number = 1

    type_grant = Type.objects.get(name='minobrnauki')
    clean_grant(type_grant)

    while True:

        response = requests.get(f'{url}?order_4=P_DATE&dir_4=DESC&page_4={page_number}', verify=False)
        
        if response.status_code == 200:

            soup = BS(response.text, features='html5lib') 
            li = soup.find("ul", class_="anons-list_docs").find_all("li")

            if li:
                
                for i in li:

                    text = i.find("a").text
                    time = i.find("time").text
                    time = datetime.datetime.strptime(time, '%d.%m.%Y').date()
                    link = 'https://www.minobrnauki.gov.ru' + i.find("a")['href']

                    if Grant.objects.filter(grant_name=type_grant, text=text, time=time, link=link).exists():
                        return

                    else:
                        grant = Grant()
                        grant.grant_name = type_grant
                        grant.time = time
                        grant.link = link
                        grant.text = text
                        grant.save()

                        doc_links = i.find('div', class_='doc-links')
                        
                        if doc_links is not None:
                            
                            for i in doc_links.find_all('a'):
                                
                                link = Link()
                                link.link = 'https://www.minobrnauki.gov.ru'+i['href']
                                link.grant_id = grant
                                link.save()
            else:
                break
        else:
            break

        page_number += 1

def rsci_parse(url):

    page_number = 1

    type_grant = Type.objects.get(name='rsci')
    clean_grant(type_grant)

    today_date = datetime.date.today() - datetime.timedelta(days=1)

    while True:

        response = requests.get(f'{url}?PAGEN_1={page_number}&SIZEN_1=9')

        if response.status_code == 200:

            soup = BS(response.text, features='html5lib')
            posts = soup.find_all(class_='col l4 m6 s12')
        
            for post in posts:

                text = post.find('div', 'info-card-deskription').find('h4', class_='text-title').text
                time = ''.join(f"{post.find_all('span')[0].text}.{post.find_all('span')[1].text}")
                time = datetime.datetime.strptime(time, '%d.%m.%Y').date()
    
                if time >= today_date and Grant.objects.filter(grant_name=type_grant, text=text).exists() is not True:
                    
                    grant = Grant()
                    grant.grant_name = type_grant

                    grant.time = time
                    grant.text = text  
                    grant.link = 'http://www.rsci.ru' + post.find('div', 'info-card-deskription').find('a')['href']
                    
                    fond = post.find('div', class_='info-title')
                    if fond:
                        grant.fond = fond.text
                    
                    fond_link = post.find('div', class_='info-title').find('a')
                    if fond_link:
                        grant.fond_link = 'http://www.rsci.ru' + fond_link['href']
                        
                    grant.save()

                else: return
        else:
            break

        page_number += 1

def edu_parse(url):

    session = HTMLSession()
    response = session.get(url)

    type_grant = Type.objects.get(name='edu')
    clean_grant(type_grant)

    today_date = datetime.date.today() - datetime.timedelta(days=1)

    if response.status_code == 200:

        response.html.render(timeout=10)

        soup = BS(response.html.html, features="lxml")
        doc_list = soup.find_all("div", class_="section page-main__searchresult-item")

        for doc in doc_list:

            text = doc.find('a').text.strip()
            time = doc.find('div', class_='date page-main__searchresult-item-meta-date mr-2 pr-2').text.strip()
            time = date_conversion(time)

            if time >= today_date and Grant.objects.filter(grant_name=type_grant, text=text, time=time).exists() is not True:
                
                grant = Grant()
                grant.grant_name = type_grant     
                grant.time = time
                grant.text = text
                grant.link = doc.find('a')['href']
                grant.label = doc.find('div', class_='d-flex').find_all('div')[1].text.strip()

                grant.save()
    
    session.close()    
     
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

    print('ПАРСИНГ 4SCIENCE')
    science_parse('https://4science.ru/finsupports')

    print('ПАРСИНГ CBIAS - start') 
    cbias_parse('http://www.cbias.ru/category/news/')
    print('ПАРСИНГ CBIAS - end')
    
    print('ПАРСИНГ FCPIR') 
    fcpir_parse('http://www.fcpir.ru/events_and_publications/_contest/')

    print('ПАРСИНГ MINOBRNAUKI') 
    minobrnauki_parse('https://www.minobrnauki.gov.ru/ru/documents/docs/index.php')

    print('ПАРСИНГ RSCI') 
    rsci_parse('http://www.rsci.ru/grants/')

    print('ПАРСИНГ EDU') 
    edu_parse('https://docs.edu.gov.ru/')  

if __name__ == '__main__':
    main()    