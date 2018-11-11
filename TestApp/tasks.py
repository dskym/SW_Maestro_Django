from __future__ import absolute_import
from TestServer.celery import app
from ExchangeAPI import BithumbAPI
from datetime import datetime
import pymysql.cursors


@app.task
def save_bithumb_btc_1m():
    history = BithumbAPI.get_transaction_history(count=100)

    temp_data = {
        'time': '',
        'open': 0.0,
        'high': 0.0,
        'low': 0.0,
        'close': 0.0,
        'volume': 0.0,
    }

    beforeData = None

    conn = pymysql.connect(host='35.201.207.75',
                           user='root',
                           password='crypstal-pw',
                           db='crypstal')

    try:
        history['data'].sort(key=lambda v: v['transaction_date'], reverse=True)

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

                if temp_data['time'] != '':
                    with conn.cursor() as cursor:
                        sql = 'INSERT INTO TestApp_bithumb_btc_1m (time, high, low, open, close, volume) VALUES (%s, %s, %s, %s, %s, %s)'

                        cursor.execute(sql, (
                            temp_data['time'], temp_data['high'], temp_data['low'], temp_data['open'],
                            temp_data['close'], temp_data['volume']))

                        conn.commit()

                        break

                temp_data['time'] = currentTime
                temp_data['open'] = float(data['price'])
                temp_data['close'] = float(data['price'])
                temp_data['high'] = float(data['price'])
                temp_data['low'] = float(data['price'])
                temp_data['volume'] = float(data['units_traded'])

            beforeData = data

    finally:
        conn.close()

    return temp_data
