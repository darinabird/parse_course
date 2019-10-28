import requests
from bs4 import BeautifulSoup
import csv


def get_html(url):
    r = requests.get(url)
    return r.text


def refined(s):
    # 1,667 total ratings
    r = s.split(' ')[0]
    result = r.replace(',', '')
    return result


def write_csv(data):
    # в переменную 'f' попадает открытый для записи файл .csv
    with open('plugins.csv', 'a') as f:
        writer = csv.writer(f)

        # writerow принимает только 1 аргумент
        # делаю кортеж
        writer.writerow((data['name'],
                         data['url'],
                         data['reviews']))


def get_data(html):
    soup = BeautifulSoup(html, 'lxml')
    popular = soup.find_all('section')[3]
    plugins = popular.find_all('article')

    for plugin in plugins:
        name = plugin.find('h2').text
        url = plugin.find('h2').find('a').get('href')

        r = plugin.find('span', class_='rating-count').find('a').text
        rating = refined(r)
        # создаю словарь для отображения даных
        data = {'name': name,
                'url': url,
                'reviews': rating}
        # print(data)
        write_csv(data)
    # return plugins


def main():
    url = 'https://wordpress.org/plugins/'
    print(get_data(get_html(url)))
    pass


if __name__ == '__main__':
    main()
