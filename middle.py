import requests
from bs4 import BeautifulSoup as BS
import csv

CSV = 'cards.csv'
URL = 'https://www.mashina.kg/search/all/'
HOST = 'https://www.mashina.kg/'

HEADERS = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36'
}

def get_html(url, params=''):
    r = requests.get(url, headers=HEADERS, params=params)
    return r
def get_content(html):
    soup = BS(html, 'html.parser')
    items = soup.find_all('div', class_="list-item list-label")
    cards = []
    for item in items:
        cards.append(
            {
                'model': item.find('h2', class_="name").text.strip(),
                'price': item.find('div', class_="block price").find('strong').get_text(strip=True),
                'image': item.find('div', class_='thumb-item-carousel').find('img', class_='lazy-image').get('data-src'),
                'aboutCar': item.find('div', 'block info-wrapper item-info-wrapper').get_text(strip=True)
            }
        )

    return cards

def save_data(items, path):
    with open(path, 'a', newline='') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow(['model', 'price', 'image', 'aboutCar'])
        for item in items:
            writer.writerow([item['model'], item['price'], item['image'], item['aboutCar']])



def parser():
    PAGENATION = input('Количество страниц: ')
    PAGENATION = int(PAGENATION.strip())
    html = get_html(URL)
    if html.status_code == 200:
        cards = []
        for page in range(1, PAGENATION):
            print(f'Parsing {page}')
            html = get_html(URL, params={'page': page})
            cards.extend(get_content(html.text))
            save_data(cards, CSV)
        print('parsing end')
        
    else:
        print('Error')
parser()
