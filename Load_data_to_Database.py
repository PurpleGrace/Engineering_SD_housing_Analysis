# Import packages
import requests
# import re
from bs4 import BeautifulSoup
import pandas as pd
# import sys
import mysql.connector
from mysql.connector import Error
import mysql
# from sqlalchemy import create_engine
# import pymysql
import geopy
import os


def load_data(href):
    return pd.read_csv(href)


def get_zillow_link():
    url = "https://www.zillow.com/research/data/"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, features="lxml")
    href = (soup.find('a',
            attrs={'id': 'home-values-forecasts-download-link'}).attrs['href'])
    print('Getting data from the following link:\n', href)
    return href


def get_airbnb_link():
    url = "http://insideairbnb.com/get-the-data.html"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, features="lxml")
    href = soup.find('a', attrs={'href': 'http://data.insideairbnb.com/united-states/ca/san-diego/2021-12-20/visualisations/listings.csv'}).attrs['href']
    print('Getting data from the following link:\n', href)
    return href


# reference https://github.com/kevinchiv/Predicting-Kickstarter-Success/blob/master/00%20-%20PostgreSQL%20Through%20Jupyter.ipynb

def create_table_schema(dataframe, table_name):
    col_names = dataframe.dtypes.index.values
    dtypes = dataframe.dtypes.values

    table_name = table_name.lower()

    create_table = "CREATE TABLE IF NOT EXISTS %s (\n" %table_name

    for i, col_name in enumerate(col_names):

        dtype = dtypes[i]
        # col_name = col_name.lower().replace(' ', '_')
        create_table += "\t"

        # assign column types and default values of null
        if dtype == 'int64':
            create_table = create_table + col_name + " INT DEFAULT NULL"

        elif dtype == 'object':
            create_table = create_table + col_name+" VARCHAR(255) DEFAULT NULL"

        elif dtype == 'float64':
            create_table = create_table + col_name+" DECIMAL(10,2) DEFAULT NULL"

        if i != len(col_names) - 1:
            create_table += ", \n"

    create_table += "\n);"
    print(create_table)
    return create_table

# Save data into database
# Create database
def set_database(db_name):
    try:
        db_con = mysql.connector.connect(host='localhost', user='root',password='root1234')
        if db_con.is_connected():
            cursor = db_con.cursor()
#             cursor.execute("SHOW DATABASES")
#             print([x for x in cursor])
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS {db_name}")
            print("Database %s is created" %db_name)
        db_con.close()
    except Error as e:
        print("Error while connecting to MySQL", e)


def create_tables(tables):
    db_con = mysql.connector.connect(host='localhost', user='root',password='root1234',database = 'SDRE_data')
    if db_con.is_connected():
        cursor = db_con.cursor()
        for table in TABLES:
            cursor.execute(f'DROP TABLE IF EXISTS {table};')
            #data.to_sql(tb_name, db_con, if_exists='fail');
            cursor.execute(TABLES[table])

def insert_table_statement(df, table_name):

    col_names = df.columns
    col_n = len(col_names)

    # statement for inserting values into table
    insert_statement = "INSERT INTO %s (" %table_name

    for i, col_name in enumerate(col_names):

        col_name = col_name.lower().replace(' ', '_')

        insert_statement = insert_statement + col_name
        if i != col_n-1:
            insert_statement += ","

    insert_statement += ") VALUES (" + "%s,"*(col_n-1) + "%s" + ")"

    return insert_statement


def insert_data_to_table(data, tb_name):
    db_con = mysql.connector.connect(host='localhost', user='root', password='root1234', database = 'SDRE_data')

    if db_con.is_connected():
        cursor = db_con.cursor()

        insert_statement = insert_table_statement(data, tb_name)
        for i in range(len(data)):
            cursor.execute(insert_statement, tuple(data.iloc[i].to_list()))
        db_con.commit()
        db_con.close()


if  __name__ == '__main__':
    zillow_link = get_zillow_link()
    df_zillow = load_data(zillow_link)

    airbnb_link = get_airbnb_link()
    df_airbnb = load_data(airbnb_link)
    # df_airbnb.drop(columns=['name'],inplace = True)
    df_airbnb = df_airbnb[['id','neighbourhood','latitude','longitude','room_type','price','minimum_nights','reviews_per_month']]

    # Check if df_coor_zip.csv extist
    if os.path.exists('df_coor_zip.csv') is False:
        # Transfer latitude and longitude to zipcode with geopy.Nominatim
        geolocator = geopy.Nominatim(user_agent='user_agent')
        zipcodes = []
        for i in range(len(df_airbnb)):
            info = geolocator.reverse((df_airbnb.iloc[i].latitude, df_airbnb.iloc[i].longitude))
            if 'postcode' in info.raw['address'].keys():
                zipcodes.append(info.raw['address']['postcode'])
            else:
                zipcodes.append('Unknown')

        df_airbnb['zipcode'] = [x.split('-')[0] for x in zipcodes]
        df_coor_zip = df_airbnb.loc[:,['id','latitude','longitude','zipcode']]
        df_coor_zip.to_csv('df_coor_zip.csv')
    else:
        df_coor_zip = pd.read_csv('df_coor_zip.csv')
        df_airbnb['zipcode'] = df_coor_zip['zipcode']

        df_airbnb = df_airbnb.where(pd.notnull(df_airbnb), None)
        df_airbnb = df_airbnb.astype(str)

    TABLES = {}
    TABLES['zillow_tb'] = create_table_schema(df_zillow, 'zillow_tb')
    TABLES['airbnb_tb'] = create_table_schema(df_airbnb, 'airbnb_tb')

    set_database("SDRE_data")
    create_tables(TABLES)
    insert_data_to_table(df_zillow, tb_name='zillow_tb')
    insert_data_to_table(df_airbnb, tb_name='airbnb_tb')
