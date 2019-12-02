import requests
import json
from bs4 import BeautifulSoup as BS 

def parse(url):

    data = []

    response = requests.get(url, verify=False)
    
    if response.status_code == 200:
        
        soup = BS(response.text, features='html5lib')
        
        li = soup.find("ul", class_="anons-list_docs").find_all("li")

        if li:

            for i in li:
                content = {}
                content['time'] = i.find("time").text
                content['link'] = 'https://www.minobrnauki.gov.ru' + i.find("a")['href']
                content['text'] = i.find("a").text

                doc = i.find('div', class_='doc-links')
                
                if doc is not None:
                    content['doc-links'] = ['https://www.minobrnauki.gov.ru'+link['href'] for link in doc.find_all('a')]   
                
                data.append(content)


    return data

def main():

    url = 'https://www.minobrnauki.gov.ru/ru/documents/docs/index.php'

    with open("data_minobr.json", "w", encoding='utf-8') as f:
        json.dump(parse(url), f, ensure_ascii=False, indent=4)
    

if __name__ == '__main__':
    main()    