import requests
import json
from bs4 import BeautifulSoup as BS 

def cbias_parse(url):

    data = []

    response = requests.get(url)

    if response.status_code == 200:

        soup = BS(response.text, features='html5lib')

        posts = soup.find_all(class_='post_inner')

        for post in posts:
            content = {}

            content['time'] = post.find('div', class_='post_date').text
            content['text'] = post.find_all('p')[0].text
            content['link'] = post.find_all('p')[0].find('a')['href']
            
            data.append(content)

    return data         

def main():

    url = 'http://www.cbias.ru/'

    with open("data_cbias.json", "w", encoding='utf-8') as f:
        json.dump(cbias_parse(url), f, ensure_ascii=False, indent=4)



if __name__ == '__main__':
    main()    