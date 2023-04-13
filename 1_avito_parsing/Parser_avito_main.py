import requests
from bs4 import BeautifulSoup
import lxml
import undetected_chromedriver
from selenium import webdriver
import time
import pandas as pd

# product = input() # пока без этого
url = "https://spb.leroymerlin.ru/product/dalnomer-lazernyy-resanta-dl-30-s-dalnostyu-do-30-m-89160871/#reviews"

def get_data(url):
    cookies = {
        'u': '2t9161tu.q3pumi.rq6ng6iesf00',
        'buyer_laas_location': '653240',
        'showedStoryIds': '99-97-96-94-88-83-78-71',
        '_ym_uid': '1648834496679747719',
        'uxs_uid': 'eaf3b800-b5e2-11ec-896a-33488e370e7e',
        'buyer_popup_location': '107621',
        'adrcid': 'AW-iMTkhGyR6t0S8X3Ri8RQ',
        '_ga_9E363E7BES': 'GS1.1.1651171642.11.0.1651171642.60',
        'buyer_location_id': '653240',
        '_gcl_au': '1.1.1848473263.1677345144',
        '_ga': 'GA1.1.1208504154.1648834496',
        '_ym_d': '1677345144',
        'isCriteoSetNew': 'true',
        '__zzatw-avito': 'MDA0dBA=Fz2+aQ==',
        '__zzatw-avito': 'MDA0dBA=Fz2+aQ==',
        'sessid': 'd0c48e94bf03e06fff7928245e8af0fe.1677407731',
        'auth': '1',
        'tmr_lvid': '3f9f934865834a5f4206794a98fd7995',
        'tmr_lvidTS': '1648834503560',
        'cfidsw-avito': 'FW+CEMFxaCvOrq7qd8OCbTxOxGjpNh0mQ27W4tItnTCM2v/MntBtOWuiUhCCc0lncm6zvG636qh7toRMAGXgo+pYoypVjWcnFVjBk8ZBvDWPK5nccN818qqvjmD+XDwT5GK3p5pzOhf16G2SmX8tEZOokjBvWYskIY1a',
        'cfidsw-avito': 'FW+CEMFxaCvOrq7qd8OCbTxOxGjpNh0mQ27W4tItnTCM2v/MntBtOWuiUhCCc0lncm6zvG636qh7toRMAGXgo+pYoypVjWcnFVjBk8ZBvDWPK5nccN818qqvjmD+XDwT5GK3p5pzOhf16G2SmX8tEZOokjBvWYskIY1a',
        'gsscw-avito': '6TRd2FD/1F+PdcuKdjAi8OhNRwzE3nHDJhFJ6JHI7FMTafgcC2pbEdedSUN2Odw2ilCHed9oGgrxOcNRcYkfHSizUYWZTHZuzN3jzN0Y0UzAkyD53fXz0V38zQ7dSwgB7bg87g0ny5f1ylhT1Ix7zaI56AngjuL8jT3PyZeSh7N7v7zSXUU+R1N8RWC/WHvMuMiJggwVBfb/a0lVguJOwEJsHY8nJdX8tXcH8nG+W5cI/rcCdYvEwwWyry3vNQ==',
        'gsscw-avito': '6TRd2FD/1F+PdcuKdjAi8OhNRwzE3nHDJhFJ6JHI7FMTafgcC2pbEdedSUN2Odw2ilCHed9oGgrxOcNRcYkfHSizUYWZTHZuzN3jzN0Y0UzAkyD53fXz0V38zQ7dSwgB7bg87g0ny5f1ylhT1Ix7zaI56AngjuL8jT3PyZeSh7N7v7zSXUU+R1N8RWC/WHvMuMiJggwVBfb/a0lVguJOwEJsHY8nJdX8tXcH8nG+W5cI/rcCdYvEwwWyry3vNQ==',
        'cfidsw-avito': '3z02YEQA6qeIke9dIvllxWJY2g/TGrzjnL2dQT0fl5gB6NpMbzpG8sHSbz6RMB8czwqXgTrNgTCHPA6OOZ5cTdz4IKHEemoH6+zSi9yFqlmgwhNxP+8hyUgFlzZQpHMpUJVGApMmnDJbeP+qiBVa0O2VVIURba1z+7ML',
        'fgsscw-avito': 'Kf6Hb0cf3cab41ee1c045207d233e0b7c2c19a1d',
        'fgsscw-avito': 'Kf6Hb0cf3cab41ee1c045207d233e0b7c2c19a1d',
        'SEARCH_HISTORY_IDS': '1%2C%2C3%2C4%2C0',
        'gMltIuegZN2COuSe': 'EOFGWsm50bhh17prLqaIgdir1V0kgrvN',
        'v': '1679774226',
        'luri': 'sankt-peterburg',
        'sx': 'H4sIAAAAAAAC%2FwTAOxICIQwG4Lv8tQUQHpHbJIBabJWB1dkd7u53g0IfwamIpDIKsacWhSm1V%2Bw%2BkqLeOFFxfvibbMVp19HMfmHqdaiQ9veatvDAQPW5PDm7TG7vfwAAAP%2F%2FaDwIbVsAAAA%3D',
        'dfp_group': '5',
        'isLegalPerson': '0',
        'abp': '0',
        '_ga_M29JC28873': 'GS1.1.1679774231.20.1.1679774248.43.0.0',
        '_ym_isad': '2',
        '_ym_visorc': 'b',
        'tmr_detect': '0%7C1679774252422',
        'cto_bundle': 'DbTAul9UWU1QYlE1TldGbnRWWG5lN0N6OGFNa3FSUlFkQTRER0ZBdzVjYVZuSnlXc3dVbCUyQll1clRPbzA5TkluTVF5cDhUc3hXRldaOCUyQndKeDJQbTgxZms2WjBqNHMxOFpNajQ5TVVoVzV1NXp3Y2x5VUJTVjZEb3dCN1NSazFab2FjSDkyMm1qeGZWanBRd2Y4T2VLWHg3ejhzNnVmM01USUVPdE9QOXdwQUlSWGdCZWF2JTJCVVltcXlIaCUyQjcxVGJ3dSUyRk96',
        '_buzz_fpc': 'JTdCJTIycGF0aCUyMiUzQSUyMiUyRiUyMiUyQyUyMmRvbWFpbiUyMiUzQSUyMi53d3cuYXZpdG8ucnUlMjIlMkMlMjJleHBpcmVzJTIyJTNBJTIyTW9uJTJDJTIwMjUlMjBNYXIlMjAyMDI0JTIwMTklM0E1NyUzQTU1JTIwR01UJTIyJTJDJTIyU2FtZVNpdGUlMjIlM0ElMjJMYXglMjIlMkMlMjJ2YWx1ZSUyMiUzQSUyMiU3QiU1QyUyMnZhbHVlJTVDJTIyJTNBJTVDJTIyMDgwNmMzNzM5ZGQ5OGQ1YzU1ZDc3ZDQ2NjIyZTIyOGUlNUMlMjIlMkMlNUMlMjJmcGpzRm9ybWF0JTVDJTIyJTNBdHJ1ZSU3RCUyMiU3RA==',
        'f': '5.cc913c231fb04ceddc134d8a1938bf88a68643d4d8df96e9a68643d4d8df96e9a68643d4d8df96e9a68643d4d8df96e94f9572e6986d0c624f9572e6986d0c624f9572e6986d0c62ba029cd346349f36c1e8912fd5a48d02c1e8912fd5a48d0246b8ae4e81acb9fa143114829cf33ca746b8ae4e81acb9fa46b8ae4e81acb9fae992ad2cc54b8aa8af305aadb1df8cebc93bf74210ee38d940e3fb81381f359178ba5f931b08c66a59b49948619279110df103df0c26013a2ebf3cb6fd35a0ac71e7cb57bbcb8e0ff0c77052689da50ddc5322845a0cba1aba0ac8037e2b74f92da10fb74cac1eab2da10fb74cac1eab2da10fb74cac1eabdc5322845a0cba1a0df103df0c26013a037e1fbb3ea05095de87ad3b397f946b4c41e97fe93686adcd32509d689180370f76ed43a0b8608802c730c0109b9fbb19f6ed9435e9e0a22aaf3db1f79087b329aa4cecca288d6b826e05e12086efc5220041a3abc2001a46b8ae4e81acb9fa46b8ae4e81acb9fa02c68186b443a7ac304d925f42244dccce4cbe6d0aa4ed0c2da10fb74cac1eab2da10fb74cac1eab25037f810d2d41a812ffd099dad8db31c959d79cca069114',
        'ft': '"6zJ20OOkO4bjcGneeIARS0b2h1WD9Bxx3RKovyUs6egxMjb932XLuMqlFH9OJfaC2Z1/MbWO5A4VHrrjxazAOFHs+cCT/5q2vSF9yzPxBpWrkiYG4oCdcWnRwL70U57MmO5dnPojQGSiwRrB4AEG/UXn4tvEx3PqOeJ484DnBxgwpyn160aqd0GVLEor/RF1"',
        'buyer_from_page': 'catalog',
    }

    headers = {
        'authority': 'www.avito.ru',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
        'cache-control': 'max-age=0',
        # 'cookie': 'u=2t9161tu.q3pumi.rq6ng6iesf00; buyer_laas_location=653240; showedStoryIds=99-97-96-94-88-83-78-71; _ym_uid=1648834496679747719; uxs_uid=eaf3b800-b5e2-11ec-896a-33488e370e7e; buyer_popup_location=107621; adrcid=AW-iMTkhGyR6t0S8X3Ri8RQ; _ga_9E363E7BES=GS1.1.1651171642.11.0.1651171642.60; buyer_location_id=653240; _gcl_au=1.1.1848473263.1677345144; _ga=GA1.1.1208504154.1648834496; _ym_d=1677345144; isCriteoSetNew=true; __zzatw-avito=MDA0dBA=Fz2+aQ==; __zzatw-avito=MDA0dBA=Fz2+aQ==; sessid=d0c48e94bf03e06fff7928245e8af0fe.1677407731; auth=1; tmr_lvid=3f9f934865834a5f4206794a98fd7995; tmr_lvidTS=1648834503560; cfidsw-avito=FW+CEMFxaCvOrq7qd8OCbTxOxGjpNh0mQ27W4tItnTCM2v/MntBtOWuiUhCCc0lncm6zvG636qh7toRMAGXgo+pYoypVjWcnFVjBk8ZBvDWPK5nccN818qqvjmD+XDwT5GK3p5pzOhf16G2SmX8tEZOokjBvWYskIY1a; cfidsw-avito=FW+CEMFxaCvOrq7qd8OCbTxOxGjpNh0mQ27W4tItnTCM2v/MntBtOWuiUhCCc0lncm6zvG636qh7toRMAGXgo+pYoypVjWcnFVjBk8ZBvDWPK5nccN818qqvjmD+XDwT5GK3p5pzOhf16G2SmX8tEZOokjBvWYskIY1a; gsscw-avito=6TRd2FD/1F+PdcuKdjAi8OhNRwzE3nHDJhFJ6JHI7FMTafgcC2pbEdedSUN2Odw2ilCHed9oGgrxOcNRcYkfHSizUYWZTHZuzN3jzN0Y0UzAkyD53fXz0V38zQ7dSwgB7bg87g0ny5f1ylhT1Ix7zaI56AngjuL8jT3PyZeSh7N7v7zSXUU+R1N8RWC/WHvMuMiJggwVBfb/a0lVguJOwEJsHY8nJdX8tXcH8nG+W5cI/rcCdYvEwwWyry3vNQ==; gsscw-avito=6TRd2FD/1F+PdcuKdjAi8OhNRwzE3nHDJhFJ6JHI7FMTafgcC2pbEdedSUN2Odw2ilCHed9oGgrxOcNRcYkfHSizUYWZTHZuzN3jzN0Y0UzAkyD53fXz0V38zQ7dSwgB7bg87g0ny5f1ylhT1Ix7zaI56AngjuL8jT3PyZeSh7N7v7zSXUU+R1N8RWC/WHvMuMiJggwVBfb/a0lVguJOwEJsHY8nJdX8tXcH8nG+W5cI/rcCdYvEwwWyry3vNQ==; cfidsw-avito=3z02YEQA6qeIke9dIvllxWJY2g/TGrzjnL2dQT0fl5gB6NpMbzpG8sHSbz6RMB8czwqXgTrNgTCHPA6OOZ5cTdz4IKHEemoH6+zSi9yFqlmgwhNxP+8hyUgFlzZQpHMpUJVGApMmnDJbeP+qiBVa0O2VVIURba1z+7ML; fgsscw-avito=Kf6Hb0cf3cab41ee1c045207d233e0b7c2c19a1d; fgsscw-avito=Kf6Hb0cf3cab41ee1c045207d233e0b7c2c19a1d; SEARCH_HISTORY_IDS=1%2C%2C3%2C4%2C0; gMltIuegZN2COuSe=EOFGWsm50bhh17prLqaIgdir1V0kgrvN; v=1679774226; luri=sankt-peterburg; sx=H4sIAAAAAAAC%2FwTAOxICIQwG4Lv8tQUQHpHbJIBabJWB1dkd7u53g0IfwamIpDIKsacWhSm1V%2Bw%2BkqLeOFFxfvibbMVp19HMfmHqdaiQ9veatvDAQPW5PDm7TG7vfwAAAP%2F%2FaDwIbVsAAAA%3D; dfp_group=5; isLegalPerson=0; abp=0; _ga_M29JC28873=GS1.1.1679774231.20.1.1679774248.43.0.0; _ym_isad=2; _ym_visorc=b; tmr_detect=0%7C1679774252422; cto_bundle=DbTAul9UWU1QYlE1TldGbnRWWG5lN0N6OGFNa3FSUlFkQTRER0ZBdzVjYVZuSnlXc3dVbCUyQll1clRPbzA5TkluTVF5cDhUc3hXRldaOCUyQndKeDJQbTgxZms2WjBqNHMxOFpNajQ5TVVoVzV1NXp3Y2x5VUJTVjZEb3dCN1NSazFab2FjSDkyMm1qeGZWanBRd2Y4T2VLWHg3ejhzNnVmM01USUVPdE9QOXdwQUlSWGdCZWF2JTJCVVltcXlIaCUyQjcxVGJ3dSUyRk96; _buzz_fpc=JTdCJTIycGF0aCUyMiUzQSUyMiUyRiUyMiUyQyUyMmRvbWFpbiUyMiUzQSUyMi53d3cuYXZpdG8ucnUlMjIlMkMlMjJleHBpcmVzJTIyJTNBJTIyTW9uJTJDJTIwMjUlMjBNYXIlMjAyMDI0JTIwMTklM0E1NyUzQTU1JTIwR01UJTIyJTJDJTIyU2FtZVNpdGUlMjIlM0ElMjJMYXglMjIlMkMlMjJ2YWx1ZSUyMiUzQSUyMiU3QiU1QyUyMnZhbHVlJTVDJTIyJTNBJTVDJTIyMDgwNmMzNzM5ZGQ5OGQ1YzU1ZDc3ZDQ2NjIyZTIyOGUlNUMlMjIlMkMlNUMlMjJmcGpzRm9ybWF0JTVDJTIyJTNBdHJ1ZSU3RCUyMiU3RA==; f=5.cc913c231fb04ceddc134d8a1938bf88a68643d4d8df96e9a68643d4d8df96e9a68643d4d8df96e9a68643d4d8df96e94f9572e6986d0c624f9572e6986d0c624f9572e6986d0c62ba029cd346349f36c1e8912fd5a48d02c1e8912fd5a48d0246b8ae4e81acb9fa143114829cf33ca746b8ae4e81acb9fa46b8ae4e81acb9fae992ad2cc54b8aa8af305aadb1df8cebc93bf74210ee38d940e3fb81381f359178ba5f931b08c66a59b49948619279110df103df0c26013a2ebf3cb6fd35a0ac71e7cb57bbcb8e0ff0c77052689da50ddc5322845a0cba1aba0ac8037e2b74f92da10fb74cac1eab2da10fb74cac1eab2da10fb74cac1eabdc5322845a0cba1a0df103df0c26013a037e1fbb3ea05095de87ad3b397f946b4c41e97fe93686adcd32509d689180370f76ed43a0b8608802c730c0109b9fbb19f6ed9435e9e0a22aaf3db1f79087b329aa4cecca288d6b826e05e12086efc5220041a3abc2001a46b8ae4e81acb9fa46b8ae4e81acb9fa02c68186b443a7ac304d925f42244dccce4cbe6d0aa4ed0c2da10fb74cac1eab2da10fb74cac1eab25037f810d2d41a812ffd099dad8db31c959d79cca069114; ft="6zJ20OOkO4bjcGneeIARS0b2h1WD9Bxx3RKovyUs6egxMjb932XLuMqlFH9OJfaC2Z1/MbWO5A4VHrrjxazAOFHs+cCT/5q2vSF9yzPxBpWrkiYG4oCdcWnRwL70U57MmO5dnPojQGSiwRrB4AEG/UXn4tvEx3PqOeJ484DnBxgwpyn160aqd0GVLEor/RF1"; buyer_from_page=catalog',
        'if-none-match': 'W/"3492ab-uaND7Y7oEqRBhZmM/bqbfRoFnVA"',
        'sec-ch-ua': '"Chromium";v="110", "Not A(Brand";v="24", "Google Chrome";v="110"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"macOS"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'none',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36',
    }

    request = requests.get(url=url, cookies=cookies, headers=headers)

    with open("index.html", "w") as file:
        file.write(request.text)

    #bs = BeautifulSoup(request.text, "html.parser")
    #print(bs)

    #all_links = bs.find_all('a', class_='iva-item-title-py3i_')

    #for link in all_links:
        #print(link['href'], 0)

def main():
    get_data(url)


if __name__ == "__main__":
    main()