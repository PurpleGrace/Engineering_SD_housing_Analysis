#!pip install mysql-connector
import streamlit as st
import sqlalchemy
import mysql.connector
import pandas as pd

st.write('''
### San Diego County Housing Market inquriry Dashboard:
''')

db_con = mysql.connector.connect(host='localhost', user='root',password='root1234',database = 'SDRE_data')
if db_con.is_connected():
    print('Database connected')
cursor = db_con.cursor()

st.sidebar.header("Please input inquriry info:")
inquiry_zip = st.sidebar.text_input('Input Zipcode:', value = '92121')
inquriry_room_number = st.sidebar.number_input('Inpurt Bedroom numbers', value = 2)
inquiry_bath_number =  st. sidebar.number_input('Input Bath numbers', value  = 2)


query = (f"SELECT * from zillow_tb where RegionName = {inquiry_zip }")

cursor.execute(query)
results = list(cursor.fetchall())

#st.dataframe(results)

pd.DataFrame(results)


st.write(f"""
Zipcode {inquiry_zip} is located in city of {results[0][4]}  the expected house market increase : {results[0][6]}%
""")


st.subheader(f"""
 Airbnb properties in zipcode {inquiry_zip}
""")
query = (f"SELECT id,latitude,longitude,room_type,price from airbnb_tb where zipcode = {inquiry_zip}")

cursor.execute(query)
results = cursor.fetchall()

airbnb_set = pd.DataFrame(results,columns=['id','latitude','longitude','room_type','price'])
airbnb_set['latitude'] = airbnb_set['latitude'].astype(float)
airbnb_set['longitude'] = airbnb_set['longitude'].astype(float)

st.map(airbnb_set.loc[:,['latitude','longitude']])
