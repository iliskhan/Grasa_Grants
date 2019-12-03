import requests
import json
from bs4 import BeautifulSoup as BS 

def rsci_parse(url):

    data = []

    response = requests.get(url)

    if response.status_code == 200:

        soup = BS(response.text, features='html5lib')

        posts = soup.find_all(class_='col l4 m6 s12')
        
        for post in posts:

            content = {}
            content['time'] = ''.join(f"{post.find_all('span')[0].text}.{post.find_all('span')[1].text}")
            content['text'] = post.find('div', 'info-card-deskription').find('h4', class_='text-title').text  
            content['link'] = 'http://www.rsci.ru' + post.find('div', 'info-card-deskription').find('a')['href']
            
            fond = post.find('div', class_='info-title')
            if fond:
                content['fond'] = fond.text.strip().replace('\t', '')
            
            fond_link = post.find('div', class_='info-title').find('a')
            if fond_link:
                content['fond_link'] = 'http://www.rsci.ru' + fond_link['href']
                
            data.append(content)
        
    return data         

def main():

    url = 'http://www.rsci.ru/grants/'

    rsci_parse(url)

    with open("data_rsci.json", "w", encoding='utf-8') as f:
        json.dump(rsci_parse(url), f, ensure_ascii=False, indent=4)


if __name__ == '__main__':
    main()    