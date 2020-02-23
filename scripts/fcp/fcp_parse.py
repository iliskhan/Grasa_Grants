import json
import requests
from os import path, environ
import sys

#in order to work with django
abs_path = path.join(path.dirname(path.dirname(path.dirname(path.abspath(__file__)))), 'grasagrant')
sys.path.append(abs_path)
environ.setdefault("DJANGO_SETTINGS_MODULE", "grasagrant.settings")
import django
django.setup()


from datetime import datetime, date
import locale

from tqdm import tqdm
from bs4 import BeautifulSoup as BS

from main.models import Type, Fcp, Category

def content_finder(url, main_url):
    
    data = []

    page_number = 1

    flag = False

    while True:

        response = requests.get(f"{url}?page={page_number}&ajax=feed")
        
        if response.ok:
            soup = BS(response.text, features="html5lib")
            news_block = soup.find(class_="news-block")

            if news_block:

                headline = news_block.find_all("div", class_="headline")

                for chunk in headline:

                    title = chunk.find("span", class_="headline_title_link").text
                    if Fcp.objects.filter(title=title).exists() is True:
                        flag = True
                        break
        
                    current_content = {}

                    current_content['time'] = chunk.find("time").text
                    current_content['card_name'] = chunk.find("a").text
                    current_content['title'] = title
                    headline_lead = chunk.find("span", class_="headline_lead")

                    current_content['lead'] = headline_lead.text if headline_lead else None


                    url_chunk = chunk.find("a", class_="headline__link")['href']
                    current_content['link'] = main_url + url_chunk

                    data.append(current_content)
                    
            else:
                break
        else:
            break
        if flag: break
        page_number+=1

    title = requests.get(url)

    if title.ok:
        title = BS(title.text, features="html5lib")
        title = title.find("p", class_="vcard_name vcard_name_selection").text
        return {'type_name': title, 'data': data}

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
    date = datetime.strptime(date, '%d %m %Y').date()
    
    return date


def main():
    urls = [
        "http://government.ru/rugovclassifier/860/events/",
        "http://government.ru/rugovclassifier/856/events/",
        "http://government.ru/rugovclassifier/821/events/",
        "http://government.ru/rugovclassifier/858/events/",
        "http://government.ru/rugovclassifier/823/events/",
        "http://government.ru/rugovclassifier/862/events/",
        "http://government.ru/rugovclassifier/845/events/",
        "http://government.ru/rugovclassifier/837/events/",
        "http://government.ru/rugovclassifier/854/events/",
        "http://government.ru/rugovclassifier/817/events/",
        "http://government.ru/rugovclassifier/826/events/",
        ]

    main_url = "http://government.ru"

    print('ПАРСИНГ FCP')

    data = [content_finder(url, main_url) for url in urls]
    
    category = Category.objects.filter(tab_name='Fcp').first()
    for t in data:
        try:
            type = Type.objects.get(name=t['type_name'])
        except:
            type = Type(name=t['type_name'], category=category)
            type.save()

        for d in t['data']:
            
            if not Fcp.objects.filter(link=d['link']).first():
                fcp = Fcp(
                            fcp_name=type,
                            time=date_conversion(d['time']),
                            card_name=d['card_name'],
                            title=d['title'],
                            lead=d['lead'],
                            link=d['link'],
                        )
                fcp.save()

if __name__ == "__main__":
    main()

