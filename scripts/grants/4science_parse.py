import requests
import json
from bs4 import BeautifulSoup as BS 

def science_parse(url):

    data = []

    response = requests.get(url, verify=False)

    if response.status_code == 200:

        soup = BS(response.text, features='html5lib')

        posts = soup.find('div', id='fin-supports-list-inner').find_all('a', class_='fin-list')

        
        for post in posts:
            content = {}

            content['time'] = post.find('span', class_='fin-list-date').text
            content['label'] = post.find('div', class_='fin-list-label').text.strip()
            
            div_text = post.find('div', class_='fin-list-title')
            div_text.span.decompose()   
            content['text'] = div_text.text.strip()                

            content['link'] = 'https://4science.ru' + post['href']


            info = post.find('div', class_='fin-list-info')

            org = info.find_all('div', class_='fin-list-info-in-last')
            if org:
                content['org'] = org[0].text.strip()

            for i in org:
                i.decompose()    

            days = info.find('div', class_='fin-list-location')
            if days:
                content['days'] = days.text.strip()

            days.decompose()

            rouble = info.find('div', class_='fin-list-info-in')
            
            if rouble:
                rouble.span.decompose()
                content['rouble'] = rouble.text.strip()
                
            data.append(content)

    return data         

def main():

    url = 'https://4science.ru/finsupports'

    with open("data_4science.json", "w", encoding='utf-8') as f:
        json.dump(science_parse(url), f, ensure_ascii=False, indent=4)

if __name__ == '__main__':
    main()    