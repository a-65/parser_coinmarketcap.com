import requests
from bs4 import BeautifulSoup
from datetime import datetime
import time
import csv

'''
ТЗ: 
Собрать данные о криптовалютах с сайта https://coinmarketcap.com/.
Поля таблицы: 'n', 'current_date_time', 'name', 'symbol', 'price', 'url'.
Формат файла .csv .
'''

coin_count = 0

def headers_str_to_dict(s):
    headers = {}
    for row in s.strip().split('\n'):
        key, value = row.split(': ')
        headers[key] = value
    return headers


def refine_price(s):
    # '$36,285.34' -> '36285.34'
    return s[1:].replace(',', '')


def get_html(url, params=None):
    r = requests.get(url, params)
    if r.ok:
        return r.text
    else:
        print('Error', r.status_code)


def write_csw(data, f_name='new_file.csv'):
    with open(f_name, 'a') as f:
        writer = csv.writer(f)
        writer.writerow([data['n'], data['current_date_time'], data['name'], data['symbol'], data['price'], data['url']])


def get_page_data(html):
    soup = BeautifulSoup(html, 'lxml')

    trs = soup\
        .find('body', class_='DAY')\
        .find('div', class_='main-content')\
        .find('div', class_='sc-57oli2-0 dEqHl cmc-body-wrapper')\
        .find('div', class_='tableWrapper___3utdq cmc-table-homepage-wrapper___22rL4')\
        .find('table')\
        .find('tbody')\
        .find_all('tr')

    for tr in trs:
        try:
            dom = tr.find('a', class_='cmc-link').get('href')
            url = 'https://coinmarketcap.com' + dom
            data = get_data_from_coin(url)
            write_csw(data, "Today's Cryptocurrency Prices by Market Cap.csv")
            print(f"{data['n']}. {data['name']} is written to the file ...")
            time.sleep(1)
        except:
            pass


def get_data_from_coin(url):
    global coin_count

    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:88.0) Gecko/20100101 Firefox/88.0', 'Accept': '*/*'}
    html = get_html(url, headers)
    soup = BeautifulSoup(html, 'lxml')

    coin_count += 1
    n = str(coin_count)
    current_date_time = str(datetime.now().strftime('%d.%m.%Y %H:%M'))

    try:
        symbol = soup.find('h2').find('small').text
    except:
        symbol = 'None'

    try:
        name = soup.find('h2').text[:-len(symbol)]
    except:
        name = 'None'

    try:
        p = soup\
            .find('div', class_='sc-16r8icm-0 dOJIkS priceTitle___1cXUG')\
            .find('div', class_='priceValue___11gHJ').text
        price = (refine_price(p))
    except:
        price = 'None'

    data = {'n': n,
            'current_date_time': current_date_time,
            'name': name,
            'symbol': symbol,
            'price': price,
            'url': url
            }

    return data


def main():
    s = '''
    Host: coinmarketcap.com
    User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:88.0) Gecko/20100101 Firefox/88.0
    Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8
    Accept-Language: ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3
    Accept-Encoding: gzip, deflate, br
    DNT: 1
    Upgrade-Insecure-Requests: 1
    Connection: keep-alive
    Cookie: sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%22179da3a050c547-0a9bb7d5cf2318-445460-1296000-179da3a050d1d8%22%2C%22first_id%22%3A%22%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%2C%22%24latest_referrer%22%3A%22%22%7D%2C%22%24device_id%22%3A%22179da3a050c547-0a9bb7d5cf2318-445460-1296000-179da3a050d1d8%22%7D; gtm_session_first=%222021-06-05T03%3A31%3A46.853Z%22; gtm_session_last=%222021-06-06T18%3A01%3A09.566Z%22; c=fRwjzso_Cfny2DLPk53_7tPbCK9ZpbT3niXTXPy1N74; _hjid=c2a9b2fd-9064-4de1-a632-4cc41b2a4a89; _fbp=fb.1.1622863907993.1114070424; _ga=GA1.2.442685663.1622863908; _gid=GA1.2.511688575.1622863908; _gali=cmc-cookie-policy-banner; cmc_gdpr_hide=1
    Cache-Control: max-age=0
    TE: Trailers
    '''
    headers = headers_str_to_dict(s)
    url = 'https://coinmarketcap.com/{}/'
    page_count = 0

    while True:
        page_count += 56
        u = url.format(page_count)

        try:
            get_page_data(get_html(u, headers))
        except:
            print('Loading is complete.')
            break


if __name__ == '__main__':
    main()