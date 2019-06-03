import pandas as pd
import mysql.connector
from mysql.connector.cursor import MySQLCursorPrepared
import numpy as np

config = {
    'user': 'root',
    'password': 'yourpassword',
    'host': 'localhost',
    'database': 'test_for_booking'
}

def make_line():
    line = pd.read_csv('line.csv', sep=',', dtype='str')
    # print(line)

    cnx = mysql.connector.MySQLConnection(**config)
    cursor = cnx.cursor(prepared=True)
    for x in range(len(line)):
        row = line.iloc[x]
        one_row = (row['id'], row['name'], row['numname'], row['service_time_start'], row['service_time_end'],  row['type'], \
            row['interval'])
        modify = (row['service_time_end'], row['id'])
        print(one_row)
        query = 'replace into booking_line values (%s,%s,%s,%s,%s,%s,%s)'
        # query = 'replace into booking_line values (%s,%s,%s,%s,%s,%s,%s)'
        # query = 'UPDATE booking_line SET service_time_end = %s WHERE id = %s'
        cursor.execute(query, one_row)

        # print(line.iloc[x]['name'])
    cnx.commit()
    cnx.close()

def make_price():
    price = pd.read_csv('price.csv', sep=',', dtype='str')
    print(price)

    cnx = mysql.connector.MySQLConnection(**config)
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
    shuttle = pd.read_csv('shuttle.csv', sep=',')
    print(shuttle)

    cnx = mysql.connector.MySQLConnection(**config)
    cursor = cnx.cursor(prepared=True)
    for x in range(len(shuttle)):
        row = shuttle.iloc[x]
        one_row = (str(row['id']), row['plate'], str(row['line_id']), 40)
        query = 'INSERT INTO booking_shuttle (id, plate, line_id, seat) values (%s,%s,%s,%s)'
        cursor.execute(query, one_row)

        # print(shuttle.iloc[x]['name'])
    cnx.commit()
    cnx.close()


def make_departure():
    departure = pd.read_csv('departure.csv', sep=',')
    print(departure)

    cnx = mysql.connector.MySQLConnection(**config)
    cursor = cnx.cursor(prepared=True)
    for x in range(len(departure)):
        row = departure.iloc[x]
        one_row = (str(row['id']), row['datetime'], str(row['busdriver_id']), str(row['shuttle_id']))
        # query =
        query = 'INSERT INTO booking_departure (id, datetime, busdriver_id, shuttle_id) values (%s,%s,%s,%s)'
        cursor.execute(query, one_row)

        # print(departure.iloc[x]['name'])
    cnx.commit()
    cnx.close()


# def make_busdriver():
#     shuttle = pd.read_csv('busdriver.csv', sep=',')
#     print(shuttle)
#
#     cnx = mysql.connector.MySQLConnection(**config)
#     cursor = cnx.cursor(prepared=True)
#     # for x in range(len(shuttle)):
#     #     row = shuttle.iloc[x]
#     #     one_row = (str(row['id']), row['plate'], str(row['line_id']), 40)
#     #     query = 'INSERT INTO booking_shuttle (id, plate, line_id, seat) values (%s,%s,%s,%s)'
#     #     cursor.execute(query, one_row)
#     #
#     #     # print(shuttle.iloc[x]['name'])
#     # cnx.commit()
#     # cnx.close()


if __name__ == "__main__":
    # make_line()
    # make_price()
    # make_shuttle()
    make_departure()
    # make_busdriver()


