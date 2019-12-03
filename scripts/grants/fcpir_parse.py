import requests
import json
from bs4 import BeautifulSoup as BS 

def parse_fcpir(url):

    data = []

    response = requests.get(url)

    if response.status_code == 200:
        
        soup = BS(response.text, features='html5lib')

        tr = soup.find('table', class_='contest').find_all('tr')

        for i in tr:

            content = {}
            content['time'] = i.find('span', class_='gray').text
            content['text'] = i.find('a').text
            content['link'] = 'http://www.fcpir.ru' + i.find('a')['href']

            data.append(content)

    return data
    

def main():
    
    url = 'http://www.fcpir.ru/events_and_publications/_contest/'

    with open("data_fcpir.json", "w", encoding='utf-8') as f:
        json.dump(parse_fcpir(url), f, ensure_ascii=False, indent=4)


if __name__ == '__main__':
    main()