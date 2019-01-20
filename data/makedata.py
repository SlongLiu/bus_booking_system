import pandas as pd
import mysql.connector
import numpy as np

config = {
    'user': 'root',
    'password': 'yourpassword',
    'host': 'localhost',
    'database': 'test_for_booking'
}

def make_line():
    line = pd.read_csv('line.csv', sep=',', dtype='str')
    # print(len(line))

    cnx = mysql.connector.connect(**config)
    cursor = cnx.cursor(prepared=True)
    for x in range(len(line)):
        row = line.iloc[x]
        one_row = (row['id'], row['name'], row['service_time_start'], row['service_time_end'], \
            row['interval'], row['numname'], row['type'])
        modify = (row['service_time_end'], row['id'])
        print(modify)
        # query = 'replace into booking_line values (%s,%s,%s,%s,%s,%s,%s)'
        # query = 'replace into booking_line values (%s,%s,%s,%s,%s,%s,%s)'
        query = 'UPDATE booking_line SET service_time_end = %s WHERE id = %s'
        cursor.execute(query, modify)

        # print(line.iloc[x]['name'])
    cnx.commit()
    cnx.close()

def make_price():
    price = pd.read_csv('price.csv', sep=',', dtype='str')
    print(price)

    cnx = mysql.connector.connect(**config)
    cursor = cnx.cursor(prepared=True)
    for x in range(len(price)):
        row = price.iloc[x]
        one_row = (str(row['id']), row['site'], row['price'], str(row['line_id']))
        query = 'INSERT INTO booking_priceofline values (%s,%s,%s,%s)'
        cursor.execute(query, one_row)

        # print(price.iloc[x]['name'])
    cnx.commit()
    cnx.close()

def make_shuttle():
    shuttle = pd.read_csv('shuttle.csv', sep=',', dtype='str')
    print(shuttle)

    cnx = mysql.connector.connect(**config)
    cursor = cnx.cursor(prepared=True)
    for x in range(len(shuttle)):
        row = shuttle.iloc[x]
        one_row = (str(row['id']), row['plate'], str(row['line_id']))
        query = 'INSERT INTO booking_shuttle (id, plate, line_id) values (%s,%s,%s)'
        cursor.execute(query, one_row)

        # print(shuttle.iloc[x]['name'])
    cnx.commit()
    cnx.close()

def make_departure():
    departure = pd.read_csv('departure.csv', sep=',', dtype='str')
    print(departure)

    cnx = mysql.connector.connect(**config)
    cursor = cnx.cursor(prepared=True)
    for x in range(len(departure)):
        row = departure.iloc[x]
        one_row = (str(row['id']), row['datetime'], row['busdriver_id'], row['shuttle_id'])
        query = 'UPDATE booking_departure (id, datetime, busdriver_id, shuttle_id) values (%s,%s,%s,%s)'
        cursor.execute(query, one_row)

        # print(departure.iloc[x]['name'])
    cnx.commit()
    cnx.close()

if __name__ == "__main__":
    make_line()
    # make_price()
    # make_shuttle()
    # make_departure()


