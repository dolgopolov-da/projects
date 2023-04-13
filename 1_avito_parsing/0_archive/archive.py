import requests
from bs4 import BeautifulSoup
import lxml
from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import datetime
import time
import pandas as pd

url = "https://www.avito.ru/sankt-peterburg/kvartiry/prodam/2-komnatnye/vtorichka-ASgBAQICAUSSA8YQAkDmBxSMUsoIFIJZ?p=3"


def get_data(url):
    # driver = webdriver.Chrome(ChromeDriverManager().install(), executable_path='/Users/dmitrijdolgopolov/Documents/1_study_python/projects/1_avito_parsing/chromedriver/chromedriver')
    options = webdriver.ChromeOptions()

    # disable webdriver mode
    options.add_argument('--disable-blink-features=AutomationControlled')

    # фоновый режим работы браузера ! отключить, если не нужно
    options.add_argument('--headless')

    driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)

    try:
        driver.get(url=url)
        # print(driver.window_handles)
        # print(driver.current_url)
        file_path = 'index.html'
        with open(file_path, 'w') as f:
            f.write(driver.page_source)
        time.sleep(0)

        '''
        items = driver.find_elements(By.XPATH, '//div[@data-marker="item-photo"]')
        items[0].click()
        # print(driver.window_handles)
        time.sleep(0)
        
        driver.switch_to.window(driver.window_handles[1])
        time.sleep(0)
        # print(driver.current_url)

        price = driver.find_element(By.XPATH, '//div[@class="style-price-value-mHi1T style-item-price-main-jpt3x item-price"]')
        title = driver.find_element(By.CLASS_NAME, 'style-title-info-main-_sKj0')
        params = driver.find_elements(By.CLASS_NAME, 'params-paramsList__item-appQw')
        print(f'Price is: {price.text}')
        print(f'Title is: {title.text}')
        for i in range(len(params)):
            print(f'Params is: {params[i].text}')
        time.sleep(0)
        '''

    except Exception as ex:
        print(ex)
    finally:
        driver.close()
        driver.quit()
        return file_path


def get_items_urls(file_path):
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
    with open(file_path) as file:
        page_code = file.read()

    soup = BeautifulSoup(page_code, 'html.parser')
    item_divs = soup.find_all('div', class_='iva-item-priceStep-uq2CQ')

    prices = []
    for item in item_divs:
        item_price = item.find('span', class_='price-root-RA1pj price-listRedesign-GXB2V').find('span', class_='price-price-JP7qe') \
                               .find('meta', itemprop="price").get('content')
        prices.append(item_price)
    return prices


# функция для конвертации даты типа "2 часа/дня/минуты назад" в дату нужного формата "20.09.2022"
def convert_to_normal_date(date):
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
    else:
        return date


def get_item_parameters(file_path):
    with open(file_path) as file:
        page_code = file.read()

    soup = BeautifulSoup(page_code, 'html.parser')
    item_divs = soup.find_all('div', class_='iva-item-titleStep-pdebR')
    date_divs = soup.find_all('div', class_='date-root-__9qz')

    room_numbers = []
    squares = []
    floors = []
    floors_in_house = []
    dates_days = []
    dates_text = []

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

    return room_numbers, squares, floors, floors_in_house, dates_days, dates_text


def main():
    pages =
    for i in range()
        file_path = get_data(url)

        # data for table
        urls = get_items_urls(file_path)
        prices = get_items_price(file_path)
        room_numbers, squares, floors, floors_in_house, dates_days, dates_text = get_item_parameters(file_path)

        # making df and save it to .csv
        df = pd.DataFrame({'url': urls,
                           'Стоимость': prices,
                           'Кол-во комнат': room_numbers,
                           'Площадь': squares,
                           'Этаж': floors,
                           'Этажей в доме': floors_in_house,
                           'Дата объявления': dates_days,
                           'Дата, примечание': dates_text})
        df.to_csv('Avito_flats.csv')


    # print(room_numbers)
    # print(squares)
    # print(floors)
    # print(floors_in_house)
    # print(dates_days)
    # print(dates_text)

if __name__ == "__main__":
    main()