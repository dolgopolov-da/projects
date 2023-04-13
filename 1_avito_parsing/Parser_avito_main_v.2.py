from bs4 import BeautifulSoup
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import datetime
import time
import pandas as pd
import numpy as np

'''URL: 2-комнатные кв. в Невском районе СПб'''
url = "https://www.avito.ru/sankt-peterburg/kvartiry/prodam/2-komnatnye/vtorichka-ASgBAQICAUSSA8YQAkDmBxSMUsoIFIJZ?district=773" # + "&p=1"


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
        driver.get(url=url)
        time.sleep(5)
        today = datetime.datetime.today().strftime('%d.%m.%Y')
        file_path: str = f'/Users/dmitrijdolgopolov/Documents/1_study_python/projects/1_avito_parsing/flats_from_avito/page_codes/Page_code_{today}.txt'

        # запишем код первой страницы в файл
        with open(file_path, 'w') as f:
            f.write(f'''

                       <<< Страница {1} >>>

            ''')
            f.write(driver.page_source)

        # get number of pages
        pages_number = number_of_pages(file_path)

        # data for table
        """Для прохода по всем страницам создадим цикл, на каждой итерации будем менять значение переменной url на новое,
        соответствующее адресу каждой последующей страницы"""
        for page in range(1, pages_number + 1):
            if page == 1:
                # на первой итерации ничего не происходит, запрос к урл 1 страницы уже был
                print(f'Парсинг {page} страницы...')
                print(f'''Парсинг {page} страницы завершен.''')
            else:
                print(f'Парсинг {page} страницы...')

                # получаем и записываем код следующей страницы в тот же файл
                driver.get(url=url + f'&p={page}')
                time.sleep(5)
                with open(file_path, 'a') as f:
                    f.write(f'''

                               <<< Страница {page} >>>

                    ''')

                    f.write(driver.page_source)

                print(f'''Парсинг {page} страницы завершен.''')
    except Exception as ex:
        print(ex)
    finally:
        driver.close()
        driver.quit()
        return file_path, pages_number  # возвращаем путь к текстовому файлу с кодом страниц и кол-во страниц


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


def get_items_urls(file_path):
    """Функция возвращает список значений с URLами каждого объявления на странице"""
    with open(file_path) as file:
        page_code = file.read()

    soup = BeautifulSoup(page_code, 'html.parser')
    item_divs = soup.find_all('div', class_='iva-item-titleStep-pdebR')

    urls = []
    for item in item_divs:
        item_url = item.find('a').get('href')
        urls.append('https://www.avito.ru' + item_url)

    return urls


def get_items_price(file_path):
    """Функция возвращает список значений со стоимостями объектов из каждого объявления на странице"""
    with open(file_path) as file:
        page_code = file.read()

    soup = BeautifulSoup(page_code, 'html.parser')
    item_divs = soup.find_all('div', class_='iva-item-priceStep-uq2CQ')

    prices = []
    for item in item_divs:
        item_price = item.find('span', class_='price-price-JP7qe') \
                               .find('meta', itemprop="price").get('content')
        prices.append(int(item_price))

    return prices


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
    item_divs = soup.find_all('div', class_='iva-item-titleStep-pdebR')
    date_divs = soup.find_all('div', class_='date-root-__9qz')
    adress_divs = soup.find_all('div', class_='geo-address-fhHd0 text-text-LurtD text-size-s-BxGpL')
    metro_divs = soup.find_all('div', class_='geo-georeferences-SEtee text-text-LurtD text-size-s-BxGpL')

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
        item_rooms_number = item.find('h3').get_text().split('-')[0][-1]
        item_square = float(item.find('h3').get_text().split(', ')[1].split('\xa0')[0].replace(',', '.'))
        item_floor = item.find('h3').get_text().split(', ')[-1].split('\xa0')[0].split('/')[0]
        item_house_floors = item.find('h3').get_text().split(', ')[-1].split('\xa0')[0].split('/')[-1]

        room_numbers.append(item_rooms_number)
        squares.append(item_square)
        floors.append(item_floor)
        floors_in_house.append(item_house_floors)

    for item in date_divs:
        item_date_day = convert_to_normal_date(item.find('div', attrs={"data-marker": "item-date"}).get_text())
        item_date_text = item.find('div', attrs={"data-marker": "item-date"}).get_text()

        dates_days.append(item_date_day)
        dates_text.append(item_date_text)

    for item in adress_divs:
        item_address = item.find('span').get_text()

        addresses.append(item_address)

    for item in metro_divs:
        metro_span = item.find_all('span')
        item_metro = metro_span[2].get_text()

        item_metro_distance = item.find('span', class_='geo-periodSection-bQIE4').get_text()

        metro.append(item_metro)
        metro_distance.append(item_metro_distance)

    return room_numbers, squares, floors, floors_in_house, dates_days, dates_text, addresses, metro, metro_distance


def main():
    # (РАСКОММЕНТИРОВАТЬ!!!) блок сбора кода страниц; для фонового режима установить параметр headless=False
    # file_path, pages_number = get_data(url=url, headless=True)  # True - для запуска в фоновом режиме

    # (ЗАКОМЕНТИРОВАТЬ!!!) блок для корректировки дальнейшей работы функции, без повторных обращений к сайту
    today = datetime.datetime.today().strftime('%d.%m.%Y')
    file_path: str = f'/Users/dmitrijdolgopolov/Documents/1_study_python/projects/1_avito_parsing/flats_from_avito/page_codes/Page_code_{today}.txt'
    pages_number = number_of_pages(file_path)

    # формирование списков с данными по объявлениям
    urls = get_items_urls(file_path)
    prices = get_items_price(file_path)
    room_numbers, squares, floors, floors_in_house, dates_days, dates_text, \
                                                addresses, metro, metro_distance = get_item_parameters(file_path)

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

    # making df and save it to .csv/xlsx
    total_df = pd.DataFrame({'url': urls,
                             'Cost': prices,
                             'Rooms': room_numbers,
                             'Square': squares,
                             'Cost_per_m2': [int(x / a) for x, a in zip(prices, squares)],
                             'Floor': floors,
                             'Floors_in_house': floors_in_house,
                             'Address': addresses,
                             'Metro': metro,
                             'Metro_distance': metro_distance,
                             'Date': dates_days,
                             'Date_note': dates_text})

    current_date = datetime.datetime.today().strftime('%d.%m.%Y')
    total_df.to_csv(f'/Users/dmitrijdolgopolov/Documents/1_study_python/projects/1_avito_parsing/flats_from_avito/flats_from_avito_{current_date}.csv')



if __name__ == "__main__":
    start = time.time()

    main()

    end = time.time() - start
    print(f'Время выполнения программы: {end}')