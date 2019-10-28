import requests
from bs4 import BeautifulSoup
import csv


def get_html(url):
    r = requests.get(url)
    return r.text


def refined(s):
    # 1,667 total ratings
    # вызвала метод .split разделяет строку по какому-то критерию
    r = s.split(' ')[0]   # 1,667
    result = r.replace(',', '')  # строковый метод replace (что меняем, на что меняем)
    return result


def write_csv(data):
    # в переменную 'f' попадает открытый для записи файл .csv
    # with автоматически закрывает файл после работы с ним
    with open('plugins.csv', 'a') as f:
        writer = csv.writer(f)

        # writerow принимает только 1 аргумент
        # делаю кортеж
        writer.writerow((data['name'],
                         data['url'],
                         data['reviews']))


def get_data(html):
    # создала экземпляр класса BS
    soup = BeautifulSoup(html, 'lxml')

    # собрала раздел 'popular plugins'
    popular = soup.find_all('section')[3]

    # собрала плагины раздела 'popular plugins' - 4 элемента
    plugins = popular.find_all('article')

    for plugin in plugins:
        # [plugin1, plugin2, plugin3, plugin4]
        # обращаемся к элементу класса 'soup'
        name = plugin.find('h2').text
        url = plugin.find('h2').find('a').get('href')

        # обратилась к тексту ссылки .text
        r = plugin.find('span', class_='rating-count').find('a').text
        # создала ссылку-фильтр, очистила данные от лишних слов и запятых
        rating = refined(r)

        # создаю словарь для упаковки даных - получаю один объект
        data = {'name': name,
                'url': url,
                'reviews': rating}
        # print(data)
        write_csv(data)
    # return plugins


def main():
    url = 'https://wordpress.org/plugins/'
    # получаем html код с конкретной страницы
    get_data(get_html(url))
    pass


if __name__ == '__main__':
    main()
