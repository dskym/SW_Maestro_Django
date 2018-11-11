import BithumbAPI
from datetime import datetime
import pymysql.cursors


history = BithumbAPI.get_transaction_history(count=100)
pivotDate = datetime.strptime('2018-11-11 18:30:00', '%Y-%m-%d %H:%M:%S')

coin_data = []

temp_data = {
    'time': '',
    'open': 0.0,
    'high': 0.0,
    'low': 0.0,
    'close': 0.0,
    'volume': 0.0,
}

beforeData = None

while True:
    flag = False

    for index, data in enumerate(history['data']):
        if beforeData is None:
            beforeData = data

            continue

        beforeTime = datetime.strptime(beforeData['transaction_date'], '%Y-%m-%d %H:%M:%S').strftime(
        '%Y-%m-%d %H:%M')

        currentTime = datetime.strptime(data['transaction_date'], '%Y-%m-%d %H:%M:%S').strftime(
        '%Y-%m-%d %H:%M')

        if currentTime == beforeTime:
            if float(data['price']) > temp_data['high']:
                temp_data['high'] = float(data['price'])

            if float(data['price']) < temp_data['low']:
                temp_data['low'] = float(data['price'])

            temp_data['volume'] += float(data['units_traded'])
        else:
            temp_data['volume'] += float(beforeData['units_traded'])
            temp_data['open'] = float(beforeData['price'])

            coin_data.insert(0, temp_data.copy())

            temp_data['time'] = currentTime
            temp_data['open'] = float(data['price'])
            temp_data['close'] = float(data['price'])
            temp_data['high'] = float(data['price'])
            temp_data['low'] = float(data['price'])
            temp_data['volume'] = float(data['units_traded'])

        if pivotDate > datetime.strptime(data['transaction_date'], '%Y-%m-%d %H:%M:%S'):
            flag = True
            break

        beforeData = data

    if flag is True:
        break

    cont_no = beforeData['cont_no']

    history = BithumbAPI.get_transaction_history(count=100, cont_no=cont_no)

conn = pymysql.connect(host='35.201.207.75',
                       user='root',
                       password='crypstal-pw',
                       db='crypstal')

try:
    with conn.cursor() as cursor:
        sql = 'INSERT INTO TestApp_bithumb_btc_1m (time, high, low, open, close, volume) VALUES (%s, %s, %s, %s, %s, %s)'

        for data in coin_data[:-1]:
            cursor.execute(sql, (data['time'], data['high'], data['low'], data['open'], data['close'], data['volume']))
    conn.commit()
finally:
    conn.close()
