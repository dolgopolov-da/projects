from bs4 import BeautifulSoup
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import datetime
import time
import glob
import os
import pandas as pd
import numpy as np
from avito_urls import *


def get_data(url, headless=True):
    """Функция создает драйвер, подключается к заданному url, записывает в файл код страницы и возвращает название
    этого файла"""
    # задаем переменную с опциями драйвера
    options = webdriver.ChromeOptions()

    # disable webdriver mode
    options.add_argument('--disable-blink-features=AutomationControlled')

    # фоновый режим работы браузера ! отключить, если не нужно
    if headless:
        options.add_argument('--headless')

    # создаем драйвер
    driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)

    # запускаем драйвер и создаем текстовый файл для записи в него кода страниц
    try:
        start_parsing_url = time.time()

        driver.get(url=url)
        time.sleep(10)
        today = datetime.datetime.today().strftime('%d.%m.%Y')
        file_path: str = f'/Users/dmitrijdolgopolov/Documents/1_study_python/projects/1_avito_parsing' \
                         f'/flats_from_avito/page_codes/Page_code_{today}.txt'

        # запишем код первой страницы в файл
        with open(file_path, 'w') as f:
            f.write(f'''

                       <<< Страница {1} >>>

            ''')
            f.write(driver.page_source)

        # get number of pages
        pages_number = number_of_pages(file_path)

        # data for table
        """Для прохода по всем страницам создадим цикл, на каждой итерации будем менять значение переменной url на 
        новое, соответствующее адресу каждой последующей страницы """
        for page in range(1, pages_number + 1):
            if page == 1:
                # на первой итерации ничего не происходит, запрос к урл 1 страницы уже был
                print(f'Парсинг {page} страницы...')
                print(f'''Парсинг {page} страницы завершен.''')
            else:
                print(f'Парсинг {page} страницы...')

                # получаем и записываем код следующей страницы в тот же файл
                driver.get(url=url + f'&p={page}')
                time.sleep(10)
                with open(file_path, 'a') as f:
                    f.write(f'''

                               <<< Страница {page} >>>

                    ''')

                    f.write(driver.page_source)

                print(f'''Парсинг {page} страницы завершен.''')
                end_parsing_url = time.time() - start_parsing_url
                print(f'Время сбора кода страниц: {int(end_parsing_url)} сек.')
    except Exception as ex:
        print(ex)
    finally:
        driver.close()
        driver.quit()
        return file_path, pages_number  # возвращаем путь к текстовому файлу с кодом страниц и кол-во страниц


def get_flat_info(url, headless=True):
    options = webdriver.ChromeOptions()
    options.add_argument('--disable-blink-features=AutomationControlled')
    if headless:
        options.add_argument('--headless')
    driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
    try:
        driver.get(url=url)
        time.sleep(5)
        flat_page_code = driver.page_source
        flat_soup = BeautifulSoup(flat_page_code, 'html.parser')
        flat_square_value = flat_soup.find_all('li', class_='params-paramsList__item-appQw')[1] \
                                     .get_text().split(' ')[2][:-3]
        flat_floor = flat_soup.find_all('li', class_='params-paramsList__item-appQw')[4] \
                                     .get_text().split(' ')[0]
        flat_floors_in_house = flat_soup.find_all('li', class_='params-paramsList__item-appQw')[4] \
            .get_text().split(' ')[-1]
    except Exception as ex:
        print(ex)
    finally:
        driver.close()
        driver.quit()
        return float(flat_square_value), int(flat_floor), int(flat_floors_in_house)


def number_of_pages(file_path):
    """Функция возвращает количество страниц, с которых нужно собрать информацию:
       парсит цифру с первой страницы поиска"""
    with open(file_path) as file:
        page_code = file.read()

    soup = BeautifulSoup(page_code, 'html.parser')
    pagination_div = soup.find('div', class_='js-pages pagination-pagination-_FSNE')
    pagination_spans = pagination_div.find_all('span', class_='styles-module-text_size_s-LNY0Q')
    pages_number = int(pagination_spans[-1].get_text())

    print(f'Количество страниц: {pages_number}')
    return pages_number


# def get_items_urls(file_path):
#     """Функция возвращает список значений с URLами каждого объявления на странице"""
#     with open(file_path) as file:
#         page_code = file.read()
#
#     soup = BeautifulSoup(page_code, 'html.parser')
#     item_divs = soup.find_all('div', class_='iva-item-body-KLUuy')
#
#     urls = []
#     for item in item_divs:
#         item_url = item.find('div', class_='iva-item-titleStep-pdebR').find('a').get('href')
#         urls.append('https://www.avito.ru' + item_url)
#
#     return urls


# def get_items_price(file_path):
#     """Функция возвращает список значений со стоимостями объектов из каждого объявления на странице"""
#     with open(file_path) as file:
#         page_code = file.read()
#
#     soup = BeautifulSoup(page_code, 'html.parser')
#     item_divs = soup.find_all('div', class_='iva-item-priceStep-uq2CQ')
#
#     prices = []
#     for item in item_divs:
#         item_price = item.find('span', class_='price-price-JP7qe') \
#             .find('meta', itemprop="price").get('content')
#         prices.append(int(item_price))
#
#     return prices


def convert_to_normal_date(date):
    """Функция для конвертации даты типа '2 часа/дня/минуты назад' в дату нужного формата '20.09.2022'.
       Применяется внутри функции get_item_parameters()"""

    if any(substr in date for substr in ['день', 'дня', 'дней']):
        days_back = float(date.split()[0])
        normal_date = (datetime.datetime.today() - datetime.timedelta(days=days_back)).strftime('%d.%m.%Y')
        return normal_date
    elif 'час' in date or 'минут' in date:
        normal_date = (datetime.datetime.today()).strftime('%d.%m.%Y')
        return normal_date
    elif 'недел' in date:
        weeks_back = float(date.split()[0])
        normal_date = (datetime.datetime.today() - datetime.timedelta(weeks=weeks_back)).strftime('%d.%m.%Y')
        return normal_date
    else:
        return date


def get_item_parameters(file_path):
    with open(file_path) as file:
        page_code = file.read()

    soup = BeautifulSoup(page_code, 'html.parser')
    item_divs = soup.find_all('div', class_='iva-item-body-KLUuy')

    'Delete ad_divs (рекламные) from item_divs'
    del_items = []
    for i in range(len(item_divs)):
        if item_divs[i].find('div', class_='geo-address-fhHd0 text-text-LurtD text-size-s-BxGpL') is None:
            del_items.append(i)
    for i in del_items[::-1]:
        del item_divs[i]

    'Create lists of parameters'
    urls = []
    prices = []
    room_numbers = []
    squares = []
    floors = []
    floors_in_house = []
    dates_days = []
    dates_text = []
    addresses = []
    metro = []
    metro_distance = []

    for item in item_divs:
        '1. URLs'
        item_url = item.find('div', class_='iva-item-titleStep-pdebR').find('a').get('href')

        '2. Prices'
        item_price = item.find('div', class_='iva-item-priceStep-uq2CQ')\
                         .find('span', class_='price-price-JP7qe') \
                         .find('meta', itemprop="price")\
                         .get('content')

        '3. Number of rooms'
        if any(substr in item.find('h3').get_text() for substr in ['Квартира-студия', 'квартира-студия', 'Студия',
                                                                   'студия', 'Апартаменты-студия',
                                                                   'апартаменты-студия']):
            item_rooms_number = 'Студия'
        else:
            item_rooms_number = item.find('h3').get_text().split('-')[0][-1]

        '4. Square, Floor, floors in house'
        item_floor = item.find('h3').get_text().split(', ')[-1].split('\xa0')[0].split('/')[0]
        item_house_floors = item.find('h3').get_text().split(', ')[-1].split('\xa0')[0].split('/')[-1]
        if len(item.find('h3').get_text().split(', ')) >= 2 and item_floor.isdigit():
            item_square = float(item.find('h3').get_text().split(', ')[1].split('\xa0')[0].replace(',', '.'))
            item_floor, item_house_floors = int(item_floor), int(item_house_floors)
        else:
            flat_url = 'https://www.avito.ru' + item.find('a', class_='link-link-MbQDP').get('href')
            item_square, item_floor, item_house_floors = get_flat_info(flat_url)

        '5. Date'
        item_date_day = convert_to_normal_date(item.find('div', attrs={"data-marker": "item-date"}).get_text())
        item_date_text = item.find('div', attrs={"data-marker": "item-date"}).get_text()

        '6. Address'
        item_address = item.find('div', class_='geo-address-fhHd0 text-text-LurtD text-size-s-BxGpL')\
                           .find('span').get_text()

        '7. Metro, distance (time) to metro'
        metro_div = item.find('div', class_='geo-georeferences-SEtee text-text-LurtD text-size-s-BxGpL')
        if metro_div is not None:
            metro_span = metro_div.find_all('span')
            if len(metro_span) >= 3:
                item_metro = metro_span[2].get_text()
                item_metro_distance = item.find('span', class_='geo-periodSection-bQIE4').get_text()
            else:
                item_metro, item_metro_distance = 'Не указано', 'Не указано'
        else:
            item_metro, item_metro_distance = 'Не указано', 'Не указано'

        '8. ADD to lists'
        urls.append('https://www.avito.ru' + item_url)
        prices.append(int(item_price))
        room_numbers.append(item_rooms_number)
        squares.append(item_square)
        floors.append(item_floor)
        floors_in_house.append(item_house_floors)
        dates_days.append(item_date_day)
        dates_text.append(item_date_text)
        addresses.append(item_address)
        metro.append(item_metro)
        metro_distance.append(item_metro_distance)

    return urls, prices, room_numbers, squares, floors, floors_in_house, dates_days, dates_text, addresses, metro, metro_distance


def main():
    """Запускаем цикл для итерации по списку ссылок на объявления в разных районах СПб"""
    for district, url in zip(list(url_dict.keys())[14:], list(url_dict.values())[14:]):  # url + "&p=1"
        print(f'Начинаю парсинг объявлений в {district.replace("ий", "ом")} районе')

        """1. (РАСКОММЕНТИРОВАТЬ!!!) Блок сбора кода страниц; для отмены фонового режима установить 
              параметр headless=False"""
        # file_path, pages_number = get_data(url=url, headless=True)  # True - для запуска в фоновом режиме

        """2. (ЗАКОМЕНТИРОВАТЬ!!!) Блок для корректировки дальнейшей работы функции, без повторных обращений к сайту 
              (когда код страниц уже есть: например, функция get_data отработала без ошибок, а при сборе параметров 
              ошибка)"""
        today = datetime.datetime.today().strftime('%d.%m.%Y')
        file_path: str = f'/Users/dmitrijdolgopolov/Documents/1_study_python/projects/1_avito_parsing' \
                         f'/flats_from_avito/page_codes/Page_code_{today}.txt'
        pages_number = 1  # number_of_pages(file_path)

        "3. Формирование списков с данными по объявлениям"
        start_parsing_soup = time.time()

        # urls = get_items_urls(file_path)
        # prices = get_items_price(file_path)
        urls, prices, room_numbers, squares, floors, floors_in_house, \
        dates_days, dates_text, addresses, metro, metro_distance = get_item_parameters(file_path)

        end_parsing_soup = time.time() - start_parsing_soup
        print(f'''Время сбора конкретных данных из кода страниц: {int(end_parsing_soup)} сек., в среднем на каждое 
                  объявление - {int(end_parsing_soup / len(urls))} сек.''')

        print(f'''С {pages_number} страниц собрана информация по следующему количеству объявлений:
        - url: {len(urls)}
        - цены: {len(prices)}
        - кол-во комнат: {len(room_numbers)}
        - площадь: {len(squares)}
        - этаж: {len(floors)}
        - кол-во этажей в доме: {len(floors_in_house)}
        - адрес: {len(addresses)}
        - метро: {len(metro)}
        - расстояние до метро: {len(metro_distance)}
        - дата объявления: {len(dates_days)}
        - дата, примечание: {len(dates_text)}
        ''')

        "4. Формирование итогового датафрейма и сохранение его в .csv/xlsx"
        total_df = pd.DataFrame({'url': urls,
                                 'Cost': prices,
                                 'Rooms': room_numbers,
                                 'Square': squares,
                                 'Cost_per_m2': [int(x / a) for x, a in zip(prices, squares)],
                                 'Floor': floors,
                                 'Floors_in_house': floors_in_house,
                                 'District': district,
                                 'Address': addresses,
                                 'Metro': metro,
                                 'Metro_distance': metro_distance,
                                 'Date': dates_days,
                                 'Date_note': dates_text})

        month = datetime.datetime.today().strftime('%Y.%m')
        today_date = datetime.datetime.today().strftime('%Y.%m.%d')
        folder_path = f'/Users/dmitrijdolgopolov/Documents/1_study_python/projects/1_avito_parsing/flats_from_avito/' \
                      f'tables_by_districts_{month}'
        if not os.path.exists(folder_path):
            os.mkdir(folder_path)
        total_df.to_csv(f'{folder_path}/flats_from_avito_{district}_{today_date}.csv')

        print(f'Таблица с объявлениями в {district.replace("ий", "ом")} районе записана в размере {len(urls)} строк')


def concat_tables(path, date):
    """Функция объединяет csv файлы с объявлениями по районам в один общий csv файл.
       Принимает на вход путь к папке с файлами таблиц."""
    is_right_answer = False
    while not is_right_answer:
        need_concat = input('Запустить объединений таблиц в одну общую? (д/н): ')
        if need_concat.lower() in ('д', 'да'):
            is_right_answer = True

            files = glob.glob(f'{path}/*.csv', recursive=True)
            df = pd.concat([pd.read_csv(file).drop(columns='Unnamed: 0') for file in files])\
                   .drop_duplicates()\
                   .reset_index(drop=True)

            if not os.path.exists(path + f'/All_flats'):
                os.mkdir(path + '/All_flats')
            df.to_csv(f'{path}/All_flats/All_flats_{date}.csv')
            print(f'Объединение таблиц завершено. '
                  f'Объединено {len(files)} таблиц.'
                  f'В итоговой таблице {df.url.nunique()} строк.')
        elif need_concat.lower() in ('н', 'нет'):
            is_right_answer = True
        else:
            print('Неверный ответ, ожидается "да" или "нет".')


if __name__ == "__main__":
    start = time.time()

    """Запускаем основную функцию"""
    # main()

    """Если нужно, запускаем функцию склеивания таблиц. Можно запустить отдельно, без запуска main."""
    date = datetime.datetime.today().strftime('%Y.%m')
    files_folder = f'/Users/dmitrijdolgopolov/Documents/1_study_python/projects/1_avito_parsing' \
                   f'/flats_from_avito/tables_by_districts_{date}'  # заменить при необходимости
    concat_tables(files_folder, date)


    end = time.time() - start
    print(f'Время выполнения программы: {int(end)} сек.')
