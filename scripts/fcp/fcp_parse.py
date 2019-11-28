import json
import requests

from tqdm import tqdm

from bs4 import BeautifulSoup as BS 


def content_finder(url, main_url):

    data = []

    page_number = 1
    
    while True:

        response = requests.get(f"{url}?page={page_number}&ajax=feed")

        if response.ok:
            soup = BS(response.text , features="html5lib")

            news_block = soup.find(class_="news-block")
            if news_block:
                
                headline = news_block.find_all("div", class_="headline")

                for chunk in headline:
                    
                    current_content = {}

                    current_content['time'] = chunk.find("time").text
                    current_content['card_name'] = chunk.find("a").text
                    current_content['title'] = chunk.find("span", class_="headline_title_link").text
                    headline_lead = chunk.find("span", class_="headline_lead")
                    if headline_lead:
                        current_content['lead'] = headline_lead.text

                    url_chunk = chunk.find("a", class_="headline__link")['href']
                    current_content['link'] = main_url + url_chunk

                    data.append(current_content)
            else:
                break
        else:
            break
        
        page_number+=1

    title = requests.get(url)

    if title.ok:
        title = BS(title.text, features="html5lib")

        title = title.find("p", class_="vcard_name vcard_name_selection").text
        return {title: data}
    


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
        "http://government.ru/rugovclassifier/821/events/",
        "http://government.ru/rugovclassifier/826/events/",
        ]

    main_url = "http://government.ru"
    data = [content_finder(url, main_url) for url in tqdm(urls)]

    with open("data.json", "w", encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    main()

    