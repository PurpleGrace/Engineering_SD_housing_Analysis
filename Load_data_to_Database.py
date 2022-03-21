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
import csv
import numpy as np

#os.chdir('/Users/kristy/Documents/Data Science Material/Metis/7 Engineering/Engineering Project/Engineering_SD_housing_Analysis')

# Load zillow data from zillow website
def zillow_value_forcast():
    if os.path.exists('data/zillow_value_forcast.csv'):
        df_zillow_value_forcast = pd.read_csv('data/zillow_value_forcast.csv')
    else:
        try:
            url  = "https://www.zillow.com/research/data/"
            response = requests.get(url)
            soup = BeautifulSoup(response.content,features="lxml")
            href = soup.find('a', attrs={'id':'home-values-forecasts-download-link'}).attrs['href']
            print('Getting data from the following link:\n',href)
            df_zillow_value_forcast = pd.read_csv(href)
        except:
            return print('Load zillow data failed')
    return df_zillow_value_forcast


df_zillow_value_forcast = zillow_value_forcast()
df_zillow_value_forcast = df_zillow_value_forcast[df_zillow_value_forcast.CountyName == "San Diego County"]
df_zillow_value_forcast = df_zillow_value_forcast[['SizeRank','RegionName',
                        'City','CountyName','BaseDate','2022-03-31',
                        '2022-05-31','2023-02-28']]
df_zillow_value_forcast.rename(columns = {'RegionName':'ZipCode'},
                                inplace = True)
df_zillow_value_forcast = df_zillow_value_forcast.where(pd.notnull(df_zillow_value_forcast), None)
df_zillow_value_forcast = df_zillow_value_forcast.astype(str)
df_zillow_value_forcast.dtypes


# Load zillow value index dataset and only take San Diego County data
def zillow_value_index():
    if os.path.exists('data/zillow_value_index.csv'):
        df_zillow_value_index = pd.read_csv('data/zillow_value_index.csv')
    else:
        try:
            url  = "https://www.zillow.com/research/data/"
            response = requests.get(url)
            soup = BeautifulSoup(response.content,features="lxml")
            href = soup.find('a', attrs={'id':'home-values-forecasts-download-link'}).attrs['href']
            print('Getting data from the following link:\n',href)
            df_zillow_value_index = pd.read_csv(href)
        except:
            return print('Load zillow data failed')
    return df_zillow_value_index


df_zillow_value_index = zillow_value_index()
Total_rigion = df_zillow_value_index.shape[0]
df_zillow_value_index = df_zillow_value_index[df_zillow_value_index.CountyName == "San Diego County"]
df_zillow_value_index = df_zillow_value_index[['SizeRank','RegionName','City','CountyName','2022-02-28']]
df_zillow_value_index.rename(columns = {'RegionName':'ZipCode'},inplace = True)
df_zillow_value_index = df_zillow_value_index.where(pd.notnull(df_zillow_value_index), None)
df_zillow_value_index = df_zillow_value_index.astype(str)
df_zillow_value_index.dtypes
df_zillow_value_index.shape
df_zillow_value_index.head()


# Load zillow rent index dataset and only take San Diego County data
def zillow_rent_index():
    if os.path.exists('data/zillow_rental_index.csv'):
        df_zillow_rent_index = pd.read_csv('data/zillow_rental_index.csv')
    else:
        try:
            url  = "https://www.zillow.com/research/data/"
            response = requests.get(url)
            soup = BeautifulSoup(response.content,features="lxml")
            href = soup.find('a', attrs={'id':'home-values-forecasts-download-link'}).attrs['href']
            print('Getting data from the following link:\n',href)
            df_zillow_rent_index = pd.read_csv(href)
        except:
            return print('Load zillow data failed')
    return df_zillow_rent_index


df_zillow_rent_index = zillow_rent_index()
df_zillow_rent_index.shape[0]
df_zillow_rent_index = df_zillow_rent_index[df_zillow_rent_index.MsaName == "San Diego, CA"]
df_zillow_rent_index = df_zillow_rent_index[['SizeRank','RegionName','2022-02']]
df_zillow_rent_index.rename(columns = {'RegionName':'ZipCode'},inplace = True)
df_zillow_rent_index = df_zillow_rent_index.where(pd.notnull(df_zillow_rent_index), None)
df_zillow_rent_index = df_zillow_rent_index.astype(str)
df_zillow_rent_index.dtypes
df_zillow_rent_index.shape
df_zillow_rent_index.head()



# load airbnb data from insideairbnb website
def get_airbnb_data():
    try:
        url  = "http://insideairbnb.com/get-the-data.html"
        response = requests.get(url)
        soup = BeautifulSoup(response.content,features="lxml")
        href = soup.find('a', attrs={'href':'http://data.insideairbnb.com/united-states/ca/san-diego/2021-12-20/visualisations/listings.csv'}).attrs['href']
        print('Getting data from the following link:\n',href)
    except:
        return print('Load airbnb data failed')
    return pd.read_csv(href)

df_airbnb = get_airbnb_data( )

df_airbnb = df_airbnb[['id','neighbourhood','latitude','longitude','room_type','price','minimum_nights','number_of_reviews','reviews_per_month']]



# Check if df_coor_zip.csv extist
if not os.path.exists('data/df_coor_zip.csv'):
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
# else:
#     df_coor_zip = pd.read_csv('data/df_coor_zip.csv')

df_coor_zip = pd.read_csv('data/df_coor_zip.csv')
df_airbnb['zipcode'] = df_coor_zip['zipcode']
df_airbnb = df_airbnb.where(pd.notnull(df_airbnb), None)
df_airbnb = df_airbnb.astype("str")

df_airbnb.dtypes


# load rental sample data

df_mls_rental_sample = pd.read_csv('data/mls_rental.csv',nrows =10)
df_mls_rental_sample = df_mls_rental_sample.astype(str)
df_mls_rental_sample.dtypes


# load selling sampe data
df_mls_selling_sample = pd.read_csv('data/mls_selling.csv',nrows = 10)
df_mls_selling_sample = df_mls_selling_sample.astype(str)
df_mls_selling_sample.dtypes



# reference https://github.com/kevinchiv/Predicting-Kickstarter-Success/blob/master/00%20-%20PostgreSQL%20Through%20Jupyter.ipynb
def create_table_schema(dataframe, table_name):
    col_names = dataframe.dtypes.index.values

    dtypes = dataframe.dtypes.values

    table_name = table_name.lower()

    create_table = "CREATE TABLE IF NOT EXISTS %s (\n" %table_name

    for i, col_name in enumerate(col_names):

        dtype = dtypes[i]
        if col_name[0].isdigit():
            col_name = "_"+col_name.lower().replace(' ', '_').replace('-', '_')
        else:
            col_name = col_name.lower().replace(' ', '_').replace('-', '_')
        create_table += "\t"

        # assign column types and default values of null
        if dtype == 'int64':
            create_table = create_table + col_name + " INT DEFAULT NULL"

        elif dtype == 'object':
            create_table = create_table + col_name+" VARCHAR(255) DEFAULT NULL"

        elif dtype == 'float32':
            create_table = create_table + col_name+" FLOAT(36) DEFAULT NULL"

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
            #cursor.execute(f"DROP DATABASE IF EXISTS {db_name}")
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS {db_name}")
            print("Database %s is created" %db_name)
        db_con.commit()

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
        db_con.commit()




def insert_table_statement(df, table_name):

    col_names = df.columns
    col_n = len(col_names)

    # statement for inserting values into table
    insert_statement = "INSERT INTO %s (" %table_name

    for i, col_name in enumerate(col_names):
        if col_name[0].isdigit():
            col_name = "_"+col_name.lower().replace(' ', '_').replace('-', '_')
        else:
            col_name = col_name.lower().replace(' ', '_').replace('-', '_')

        insert_statement = insert_statement + '`'+ col_name +'`'
        if i != col_n-1:
            insert_statement += ","

    insert_statement += ") VALUES (" + "%s,"*(col_n-1) + "%s" + ")"

    return insert_statement


# Save a datafrme into database
def insert_dataframe_to_table(data,tb_name):
    db_con = mysql.connector.connect(host='localhost', user='root',password='root1234',database = 'SDRE_data')

    if db_con.is_connected():
        cursor = db_con.cursor()

        insert_statement = insert_table_statement(data,tb_name)
        for i in range(len(data)):
            cursor.execute(insert_statement,tuple(data.iloc[i].to_list()))
        db_con.commit()



# insert csv file into table
def insert_csv_into_table(df_sample,file, tb_name):

    db_con = mysql.connector.connect(host='localhost', user='root',password='root1234',database = 'SDRE_data')
    num_correct = 0
    if db_con.is_connected():
        cursor = db_con.cursor()
        insert_statement = insert_table_statement(df_sample,tb_name)
        with open(file,'r') as csv_file:
            reader = csv.reader(csv_file,delimiter = ',')
            next(reader)
            for index, row in enumerate(reader):
                cursor.execute(insert_statement, tuple(row))
                try:
                    cursor.execute(insert_statement, tuple(row))
                    num_correct += 1
                except Exception as error:
                    with open(f'data/error/{tb_name}_error.csv', mode = 'a') as error_file:
                        error_file.write(str(index+1))


        db_con.commit()
        db_con.close()



TABLES = {}
TABLES['zillow_rent_index_tb']= create_table_schema(df_zillow_rent_index,'zillow_rent_index_tb')
TABLES['zillow_value_index_tb']= create_table_schema(df_zillow_value_index,'zillow_value_index_tb')
TABLES['zillow_value_forcast_tb']= create_table_schema(df_zillow_value_forcast,'zillow_value_forcast_tb')

TABLES['airbnb_tb'] = create_table_schema(df_airbnb,'airbnb_tb')
TABLES['mls_rental_tb'] = create_table_schema(df_mls_rental_sample,'mls_rental_tb')
TABLES['mls_selling_tb'] = create_table_schema(df_mls_selling_sample,'mls_selling_tb')

set_database("SDRE_data")
create_tables(TABLES)
insert_dataframe_to_table(df_zillow_rent_index,tb_name = 'zillow_rent_index_tb')
insert_dataframe_to_table(df_zillow_value_index,tb_name = 'zillow_value_index_tb')
insert_dataframe_to_table(df_zillow_value_forcast,tb_name = 'zillow_value_forcast_tb')
insert_dataframe_to_table(df_airbnb,tb_name = 'airbnb_tb')
insert_csv_into_table(df_mls_selling_sample, "data/mls_selling.csv",'mls_selling_tb' )
insert_csv_into_table(df_mls_rental_sample,"data/mls_rental.csv",'mls_rental_tb' )


print('All data are loaded into database')
