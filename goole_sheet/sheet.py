from datetime import datetime, timezone, timedelta
import gspread
import pandas as pd
import asyncio
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
    sheet = client.open(title = 'Eldik_Express_Products').sheet1
    values = df.values.tolist()
    data = []
    for index, row in df.iterrows():
        track_code = row.iloc[1]
        status = 'В Пути'
        date = row.iloc[2]
        data.append([track_code, '', status, date])
    sheet.append_rows(data)
    return True

import time
def sort_status(data):
    tz = timezone(timedelta(hours=6))
    date = datetime.now(tz)
    current_date = date.strftime("%m-%d")

    sheet = client.open(title='Eldik_Express_Products').sheet1
    sheet_data = sheet.get_all_records()

    count = 0  # Счётчик запросов
    for index, row in data.iterrows():
        for i, row2 in enumerate(sheet_data, start=2):
            if str(row.iloc[1]) == str(row2['Трек Код']) and row2['Статус'] != 'Сортировка':
                while True:  # Бесконечный цикл, пока не удастся обновить
                    try:
                        sheet.update(f'C{i}:D{i}', [['Сортировка', current_date]])
                        break  # Если успешно — выходим из цикла
                    except:
                        time.sleep(2)
                count += 1
                if count % 100 == 0:  # Пауза после 100 обновлений
                    time.sleep(1)



async def update_google_sheet(data, new_status, bot):
    sheet = client.open(title='Eldik_Express_Products').sheet1
    sheet_data = sheet.get_all_records()
    
    tz = timezone(timedelta(hours=6))
    current_date = datetime.now(tz).strftime("%m-%d")

    spreadsheet2 = client.open('Eldik_Express_Clients')
    sheets2 =  spreadsheet2.worksheets()
    clients = sheets2[0]
    data2 = clients.get_all_records()

    updates = []  # Список для массового обновления

    for index, row in data.iterrows():
        track_code = row['Трек код']
        client_code = row['Код клиента'] if not pd.isna(row['Код клиента']) else ''
        price = row['Общ.сумма'] if not pd.isna(row['Общ.сумма']) else ''

        # Отправляем сообщение клиенту
        for i, row in enumerate(data2, start=2):
            if str(row['id']) == str(client_code) and row['tg_id']:
                try:
                    await bot.send_message(text=f'Ваша посылка с трек кодом {track_code} прибыла на склад', chat_id=int(row['tg_id']))
                except:
                    continue

        # Подготовка данных для массового обновления
        for i, row in enumerate(sheet_data, start=2):
            if row['Трек Код'] == track_code:
                updates.append({
                    'range': f'A{i}:E{i}',
                    'values': [[track_code, client_code, new_status, current_date, price if price not in ['0', 0] else '']]
                })

        # Добавляем паузы, если слишком много данных
        if len(updates) >= 1000:  
            sheet.batch_update(updates)
            updates.clear()
            await asyncio.sleep(2)  

    # Обновляем оставшиеся данные
    if updates:
        sheet.batch_update(updates)




def find_order_by_id(item_id,lang):
    spreadsheet = client.open(title='Eldik_Express_Products')
    sheets = spreadsheet.worksheets()
    sheet = sheets[0]
    data = sheet.get_all_values()
    df = pd.DataFrame(data[1:], columns=data[0])
    items = df[df['Код клиента'] == item_id]
    orders_info = ""
    k = 0
    extra = ''
    extra_date = ''
    summ = 0
    for index, row in items.iterrows():
        extra = ''
        extra_date = ''
        if row['Дата']:
            extra_date = f"Дата: {row['Дата']}"
        if row['Статус'] == 'В Пути':
            status = '🚛 В Пути'
        if row['Статус'] == 'Сортировка':
            status = ' 🇰🇬Сортировка'
        if row['Статус'] == 'Готов к выдаче':
            status = 'Готов к выдаче'
        if row['Статус'] == 'Выдан':
            status = 'Выдан'
        orders_info += f"Код: {row['Трек Код']}, {status}{extra}\n{extra_date},\n———————————————-\n"
        if summ == 0:
            summ = row['Сумма']
    if orders_info and summ:
        orders_info += f"Общая сумма: {summ}"
        return orders_info
    if orders_info:
        return orders_info
    if lang == 'RU':
        return f"У вас пока-что нет товаров"
    else:
        return f"Сизде товар жок"

def register_client(data):
    spreadsheet = client.open(title='Eldik_Express_Clients')
    sheets = spreadsheet.worksheets()
    sheet = sheets[0]
    sheet.append_row([data['city'],data['full_name'] + ' ' + data['name'],data['phone_number'],str(data['id']), data['tg_id']])
    return True

def update_client_by_id(client_id, new_data,ref):
    spreadsheet = client.open('Eldik_Express_Clients')
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
    spreadsheet = client.open('Eldik_Express_Clients')
    sheets = spreadsheet.worksheets()
    sheet = sheets[0]
    data = sheet.get_all_records()
    for i, row in enumerate(data, start=2):
        if row['id'] == client_id and row['Номер'] == int(phone_number):
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


def set_client_id_to_product(track_code, client_id):
    spreadsheet = client.open('Eldik_Express_Products')
    sheets = spreadsheet.worksheets()
    sheet = sheets[0]
    data = sheet.get_all_records()
    for i, row in enumerate(data, start=2):  # start=2, т.к. первая строка — заголовок
        if str(row['Трек Код']) == str(track_code):
            # Обновляем значение в столбце "Статус" для найденной строки
            status_col_index = list(row.keys()).index('Код клиента') + 1
            sheet.update_cell(i, status_col_index, client_id)
            return True
    return False

async def send_notification(track_code, bot):
    spreadsheet = client.open('Eldik_Express_Products')
    sheets = spreadsheet.worksheets()
    products = sheets[0]
    data = products.get_all_records()
    for i, row in enumerate(data, start=2):
        if str(row['Трек Код']) == str(track_code):
            if str(row['Статус']) == 'Выдан':
                return f'{track_code} уже был выдан'
            client_id = str(row['Код клиента'])
            i_product = i
            status_col_index = list(row.keys()).index('Статус') + 1
            break
    if not client_id:
        return f'Не найден клиент для трек кода {track_code}'
    spreadsheet2 = client.open('Eldik_Express_Clients')
    sheets2 = spreadsheet2.worksheets()
    clients = sheets2[0]
    data2 = clients.get_all_records()
    for i, row in enumerate(data2, start=2):
        if str(row['id']) == str(client_id):
            tg_id = row['tg_id']
            break
    if not tg_id:
        return f'У клиента с id {client_id} не установлен tg_id'
    text = f'Посылка с трек кодом {track_code} успешно выдана'
    await bot.send_message(chat_id=int(tg_id), text = text)
    products.update_cell(i_product, status_col_index, 'Выдан')
    return f'{track_code} ✅'
