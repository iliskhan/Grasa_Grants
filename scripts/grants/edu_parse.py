from requests_html import HTMLSession
import json
from bs4 import BeautifulSoup as BS 

def edu_parse(url):

    data = []

    session = HTMLSession()

    response = session.get('https://docs.edu.gov.ru/')

    if response.status_code == 200:

        response.html.render()

        soup = BS(response.html.html, features="lxml")

        doc_list = soup.find_all("div", class_="section page-main__searchresult-item")

        for doc in doc_list:
            content = {}

            content['time'] = doc.find('div', class_='date page-main__searchresult-item-meta-date mr-2 pr-2').text.strip()
            content['text'] = doc.find('a').text.strip()
            content['link'] = doc.find('a')['href']
            content['label'] = doc.find('div', class_='d-flex').find_all('div')[1].text.strip()

            data.append(content)

    return data

def main():

    url = 'https://docs.edu.gov.ru/'

    with open("data_edu.json", "w", encoding='utf-8') as f:
        json.dump(edu_parse(url), f, ensure_ascii=False, indent=4)


if __name__ == '__main__':
    main()    