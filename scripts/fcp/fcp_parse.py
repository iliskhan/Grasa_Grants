import requests

from bs4 import BeautifulSoup as BS 


def content_finder(url):

    page_number = 1
    
    while True:

        response = requests.get(f"{url}?page={page_number}&ajax=feed")

        if response.status_code == 200:
            soup = BS(response.text , features="html5lib")

            news_block = soup.find(class_="news-block")
            if news_block:
                
                headline = news_block.find_all("div", class_="headline")
                for chunk in headline:
                    print(chunk.find("time").text)
                    print(chunk.find("a").text)
                    print(chunk.find("span", class_="headline_title_link").text)
                    headline_lead = chunk.find("span", class_="headline_lead")
                    if headline_lead:
                        print(headline_lead.text)

                    print(chunk.find("a", class_="headline__link")['href'])
            else:
                break
        else:
            break
        
        page_number+=1


def main():
    url = "http://government.ru/rugovclassifier/860/events/"

    content_finder(url)

    # main_url = "http://government.ru/"

if __name__ == "__main__":
    main()

    