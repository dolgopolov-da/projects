import pandas as pd
import gspread
from df2gspread import df2gspread as d2g
from oauth2client.service_account import ServiceAccountCredentials
import json
import datetime
import glob

'1. Подготовка'
json_key = '/Users/dmitrijdolgopolov/Documents/1_study_python/APIs/google_sheet/avito-flats-0d53a14d8aa7.json'
with open(json_key, 'r') as j:
    contents = json.loads(j.read())
scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']
my_mail = 'dima.greensfan@gmail.com'

'2. Авторизация'
credentials = ServiceAccountCredentials.from_json_keyfile_name(json_key, scope)
gs = gspread.authorize(credentials)

'3. Название и создание листа в google sheets, делаем его видимым'
table_name = 'All_flats_test'
sheet = gs.create(table_name)
sheet.share(my_mail, perm_type='user', role='writer')

'4. Загрузка датафрейма в google sheets'
month = datetime.datetime.today().strftime('%Y.%m')
day = '2023.04.19'  # datetime.datetime.today().strftime('%Y.%m.%d')

# заменить при необходимости
files_folder = f'/Users/dmitrijdolgopolov/Documents/1_study_python/projects/\
1_avito_parsing/flats_from_avito/tables_by_districts_{month}/{day}/All_flats'

files = glob.glob(f'{files_folder}/*.csv')
file_name = files[0]
df = pd.read_csv(file_name).drop(columns='Unnamed: 0')

sheet_name = 'df'
d2g.upload(df, table_name, sheet_name, credentials=credentials, row_names=True)
spreadsheet_url = "https://docs.google.com/spreadsheets/d/%s" % sheet.id
print(spreadsheet_url)

