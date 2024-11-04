from datetime import datetime, timezone, timedelta
import gspread
import pandas as pd
from google.oauth2.service_account import Credentials
from gspread_formatting import Color, CellFormat,format_cell_range

scopes = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive'
]
credentials = Credentials.from_service_account_file('./credentials.json', scopes=scopes)
client = gspread.authorize(credentials)

def append_products(df):
    tz = timezone(timedelta(hours=6))
    date = datetime.now(tz)
    current_date = date.strftime("%m-%d")
    sheet = client.open(title = 'Line_cargo-PRODUCTS').sheet1
    values = df.values.tolist()
    data = []
    for index, row in df.iterrows():
        track_code = row[0]
        client_id = row[1]
        status = 'В Китае'
        date = current_date
        if len(row) == 3:
            weight = str(row[2]) if not pd.isnull(row.iloc[2]) else ""
        else:
            weight = ''
        data.append([track_code, client_id, status, date, weight])
        # for row in values:
        #     row.append('В Китае')
        #     row.append(current_date)
        #     row = [str(value) for value in row]
        # sheet.append_rows(values)
        # return True
    sheet.append_rows(data)
    # length = len(df)
    # new_statuses = ['В Китае' for x in range(length)]
    # new_dates = [str(current_date) for x in range(length)]
    # column_weights = []
    # for l in values:
    #     column_weights.append(l.pop())
    #     l = [str(value) for value in l]
    # sheet.append_rows(values)
    # result = [new_statuses,new_dates,column_weights]
    # transposed_result = list(map(list, zip(*result)))
    # sheet.update('C2', transposed_result)
    return True




def update_google_sheet(track_codes, new_status):
    sheet = client.open(title = 'Line_cargo-PRODUCTS').sheet1 
    data = sheet.get_all_records()
    tz = timezone(timedelta(hours=6))
    date = datetime.now(tz)
    current_date = date.strftime("%m-%d")
    for row in data:
        if row['Трек Код'] in track_codes:
            row['Статус'] = new_status
            row['Дата'] = current_date
    add_track_codes = {code for code in track_codes if code not in {row['Трек Код'] for row in data}}
    current_row = len(sheet.get_all_records())+2
    last_row = current_row-1
    if add_track_codes:
        for code in add_track_codes:
            sheet.append_row([code])
            last_row += 1
    if add_track_codes:
        diapazon = f'A{current_row}:A{last_row}'
        sheet.format(diapazon,{"backgroundColor": {"red": 1.0}})
    formatted_data = [
        [str(value) if isinstance(value, (int, float)) else value for value in row.values()]
        for row in data
    ]
    sheet.update([list(data[0].keys())] + formatted_data)
    return True


def find_order_by_id(item_id,lang):
    spreadsheet = client.open(title='Line_cargo-PRODUCTS')
    sheets = spreadsheet.worksheets()
    sheet = sheets[0]
    data = sheet.get_all_values()
    df = pd.DataFrame(data[1:], columns=data[0])
    items = df[df['Код клиента'] == item_id]  
    orders_info = ""
    k = 0
    extra = ''
    extra_date = ''
    for index, row in items.iterrows():
        extra = ''
        extra_date = ''
        if row['Дата']:
            extra_date = f"Дата: {row['Дата']}"
        if row['Вес']:
            extra = f", Вес: {row['Вес']} кг"
        if row['Статус'] == 'В Пути':
            status = '🚛 В Пути'
        if row['Статус'] == 'В Китае':
            status = '🇨🇳 В Китае'
        if row['Статус'] == 'В Москве':
            status = '🇷🇺 в Москве'
        orders_info += f"Код: {row['Трек Код']}, {status}{extra}\n{extra_date},\n———————————————-\n"
    if orders_info:
        return orders_info  
    if lang == 'RU':
        return f"У вас пока-что нет товаров"
    else:
        return f"Сизде товар жок"

def find_order_by_track_code(track_code,lang):
    track_code = str(track_code)  
    spreadsheet = client.open(title='Line_cargo-PRODUCTS')
    sheets = spreadsheet.worksheets()
    sheet = sheets[0]
    data = sheet.get_all_values()
    df = pd.DataFrame(data[1:], columns=data[0]) 
    item = df[df['Трек Код'] == track_code]
    extra = ''
    extra_date = ''
    if not item.empty:
        status = item.iloc[0]['Статус']
        time = item.iloc[0]['Дата']
        weight = item.iloc[0]['Вес']
        if weight:
            extra = f', Вес: {weight} кг'
        if time:
            extra_date = f"Дата: {time}"
        if status == 'В Пути':
            status = '🚛 В Пути'
        if status == 'В Китае':
            status = '🇨🇳 В Китае'
        if status == 'В Москве':
            status = '🇷🇺 в Москве'
        info = f'Код: {track_code}, {status}{extra}\n{extra_date}\n'
        return info
    if lang == 'RU':
        return 'Товар с таким трек-кодом не найден в базе'
    else:
        return 'Бул товар табылганжок'

def register_client(data):
    # if data.get('ref'):
    #     spreadsheet = client.open(title='TEST-BOT-CLIENTS')
    #     sheets = spreadsheet.worksheets()
    #     sheet = sheets[0]
        # sheet.append_row([data['city'],data['full_name'] + ' ' + data['name'],data['phone_number'],data['id']])
    spreadsheet = client.open(title='Line_cargo-CLIENTS')
    sheets = spreadsheet.worksheets()
    sheet = sheets[0]
    sheet.append_row([data['city'],data['full_name'] + ' ' + data['name'],data['phone_number'],data['id']])
    return True

def update_client_by_id(client_id, new_data,ref):
    # if ref:
    #     spreadsheet = client.open('SonunExpress-clients')
    #     sheets = spreadsheet.worksheets()
    #     sheet = sheets[0]
    #     data = sheet.get_all_records()
    #     for i, row in enumerate(data, start=2):
    #         if row['id'] == client_id:
    #             for key, value in new_data.items():
    #                 sheet.update_cell(i, sheet.find(key).col, value)
    spreadsheet = client.open('Line_cargo-CLIENTS')
    sheets = spreadsheet.worksheets()
    sheet = sheets[0]
    data = sheet.get_all_records()
    for i, row in enumerate(data, start=2):
        if row['id'] == client_id:
            for key, value in new_data.items():
                sheet.update_cell(i, sheet.find(key).col, value)
            return True
    return False

def find_user_by_data(phone_number,client_id,lang):
    spreadsheet = client.open('Line_cargo-CLIENTS')
    sheets = spreadsheet.worksheets()
    sheet = sheets[0]
    if client_id.isdigit() == False:
        if lang == 'RU':
            return 'Извините, неверный номер или код'
        else:
            return 'Кечиресиз, номер же жеке код туура эмес'


    data = sheet.get_all_records()
    for i, row in enumerate(data, start=2):
        if row['id'] == int(client_id) and row['Номер'] == int(phone_number):
            data = {'id':client_id,
                    'name':row['ФИО'].split()[0],
                    'full_name':row['ФИО'].split()[1],
                    'phone_number':row['Номер'],
                    'city':row['Город'],
                    'language':lang
                    }
            return data
    if lang == 'RU':
        return 'Извините, неверный номер или код'
    else:
        return 'Кечиресиз, номер же жеке код туура эмес'

    


