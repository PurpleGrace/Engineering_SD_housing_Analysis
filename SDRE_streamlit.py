
import plotly
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import mysql.connector
import pandas as pd
import numpy as np
import pydeck as pdk
from Load_data_to_Database import *




os.chdir('/Users/kristy/Documents/Data Science Material/Metis/7 Engineering/Engineering Project/Engineering_SD_housing_Analysis')

st.set_page_config(
     page_title="SDRE Dashboard",
     page_icon=":bar_chart:",
     layout="wide",
     initial_sidebar_state="expanded",
 )

#db_con = mysql.connector.connect(host='localhost', user='root',password='root1234',database = 'SDRE_data')
def init_connection():
    return mysql.connector.connect(**st.secrets["mysql"])

db_con = init_connection()
if db_con.is_connected():
    print('Database connected')
cursor = db_con.cursor()

query = ('''
        SELECT vf.zipcode as zipcode,
                vf.city as city,
                vf._2022_03_31 as vf_2022_03_31,
                vf._2022_05_31 as vf_2022_05_31,
                vf._2023_02_28 as vf_2023_02_28,
                vi._2022_02_28 as vi__2022_02_28,
                ri._2022_02 as ri__2022_02
        FROM zillow_value_forcast_tb AS vf
        LEFT JOIN (zillow_value_index_tb AS vi,zillow_rent_index_tb AS ri)
        ON (vf.zipcode = vi.zipcode And vf.zipcode = ri.zipcode) ;
''')

df_zillow = pd.read_sql_query(query, db_con)

query = ('''
        SELECT zipcode,count(id) as listings,avg(price), avg(number_of_reviews ) as avg_reviws
        FROM airbnb_tb
        GROUP BY zipcode
 ''')

airbnb_zip_info = pd.read_sql_query(query,db_con)

query = ('''
        SELECT * FROM mls_rental_tb
 ''')

df_rental = pd.read_sql_query(query,db_con)

query = ('''
        SELECT * FROM mls_selling_tb
 ''')

df_selling = pd.read_sql_query(query,db_con)

query = ('''
        SELECT * FROM mls_rental_tb
 ''')

df_rental= pd.read_sql_query(query,db_con)



query = ('''
     SELECT * FROM airbnb_tb;
''')
df_airbnb= pd.read_sql_query(query,db_con)



query = ('''
        ALTER TABLE airbnb_tb MODIFY longitude Float(15,8);
 ''')
cursor.execute(query)

query = ('''
         ALTER TABLE airbnb_tb MODIFY latitude Float(15,8);
  ''')
cursor.execute(query)

query = ('''
         ALTER TABLE airbnb_tb MODIFY price Float(15,8);
  ''')
cursor.execute(query)

query = ('''
         SELECT * FROM airbnb_tb;
  ''')
df_airbnb= pd.read_sql_query(query,db_con)


db_con.close()

# -------- sidebar -----------------------
st.sidebar.header("Please Input Inquery Info:")


# cursor.execute(query)
# df_zillow= pd.DataFrame(cursor.fetchall())
# df_zillow.columns = ['zipcode','city',]

inquiry_zip = st.sidebar.selectbox('Input ZipCode:',options = df_zillow.zipcode.unique(),index=1)
inquriry_room_number = st.sidebar.number_input('Inpurt Bedroom numbers', value = 1)
inquiry_bath_number =  st.sidebar.number_input('Input Bath numbers', value  = 2)

# city = df_zillow[df_zillow.zipcode ==inquiry_zip ].city
# vf_2022_03_31 = df_zillow[df_zillow.zipcode ==inquiry_zip ].vf_2022_03_31
# vf_2022_05_31 = df_zillow[df_zillow.zipcode ==inquiry_zip ].vf_2022_05_31
# vf_2023_02_28 = df_zillow[df_zillow.zipcode ==inquiry_zip ].vf_2023_02_28
# vi__2022_02_28 = df_zillow[df_zillow.zipcode ==inquiry_zip ].vi__2022_02_28
# ri__2022_02 = df_zillow[df_zillow.zipcode ==inquiry_zip ].ri__2022_02

df_z_zip  = df_zillow.query('zipcode == @inquiry_zip')
df_a_zip_agg = airbnb_zip_info.query('zipcode == @inquiry_zip')
df_selling_zip = df_selling.query('zip == @inquiry_zip')
df_rental_zip = df_rental.query('zip == @inquiry_zip')


#--------------------main page------------------------------
st.title(":bar_chart: San Diego Real Estate Dashboard")

#-------------------subhead --------------------------------
st.markdown("### Rental Info")
rent_avg = df_rental_zip[df_rental_zip.status == 'Rented'].rented_price.astype(float).mean()
mask = (df_rental_zip.bedrooms_total == str(inquriry_room_number)) & (df_rental_zip.baths_full == str(inquiry_bath_number))

column1, column2= st.columns(2)

with column1:
    st.markdown(f"##### {inquiry_zip} Zillow Rental Index: ${df_z_zip['ri__2022_02'].values[0]}")

with column2:
    st.markdown(f"##### Average Rented Price In Past Three Month: ${rent_avg}")

if (len(df_rental_zip[mask]) == 0):
    st.markdown(f'No Rental Info for {inquriry_room_number} bedrooms and {inquiry_bath_number} bathrooms Property')
else:
    rental_his= px.histogram(df_rental_zip[mask].list_price.astype(float),
                title = f"      AveragePrice for {inquriry_room_number}b/{inquiry_bath_number}ba Property: ${int(df_rental_zip[mask].list_price.astype(float).mean())}  ")
    st.plotly_chart(rental_his,template="simple_white",use_container_width = True)


st.markdown("""---""")
# -----------------subhead-------------------------
st.subheader("Market Value Info")

x=['2022_03_31','2022_05_31','2023_02_28']
y = df_z_zip.iloc[0][2:5].astype(float)
df_v_increase = pd.DataFrame({'Date':x, 'Increase Expection':y})

mask = (df_selling_zip.bedrooms_total == str(inquriry_room_number)) & (df_selling_zip.baths_full == str(inquiry_bath_number))
sold_avg = df_selling_zip[df_selling_zip.status == 'Sold'].sold_price.astype(float).mean()


column1, column2 = st.columns(2)

column1.markdown(f"###### {inquiry_zip} Zillow House Value Index: $ {df_z_zip['vi__2022_02_28'].values[0]}")
column1.markdown(f"##### $ {df_z_zip['vi__2022_02_28'].values[0]}")

column2.markdown(f"###### Average Sold Price In Past Three Month:")
column2.markdown(f"#####  ${int(sold_avg)}")


v_increase_chart = px.bar(df_v_increase,x='Date', y='Increase Expection', title='Zillow Value Increase Forcast :',template="simple_white")

column1, column2 = st.columns(2)
with column1:
    st.plotly_chart(v_increase_chart,use_container_width=True)

with column2:
     df_selling_zip[mask].residential_styles.unique()
     df_stype = pd.DataFrame([ df_selling_zip[mask].residential_styles,df_selling_zip[mask]['list_price'].astype(float)]).transpose()
     df_stype
     style_price_fig = px.box(df_stype, x="residential_styles", y="list_price",
                        title = f'Listing Price Boxplot By Styles of {inquriry_room_number}b/{inquiry_bath_number}ba Property ',
                        template="simple_white")
     st.plotly_chart(style_price_fig,use_container_width= True)


st.markdown("""---""")


# -------------------subhead--------------------------------------
st.subheader("Airbnb Listing Info")
df_airbnb_zip = df_airbnb[df_airbnb.zipcode == inquiry_zip]
mean_airbnb_zip =  df_airbnb_zip.price.mean()
df_aibnb_most = df_airbnb.groupby(['zipcode'])['id'].count().sort_values(ascending = False)[:10]
df_aibnb_most = pd.DataFrame({'zipcode':df_aibnb_most.index, 'total':df_aibnb_most.values})

column1, column2 = st.columns(2)
zip_airbnb_fig = px.bar(df_aibnb_most,x='zipcode',y='total',title='Most Popular ZipCode With Aibnb',template="simple_white")
with column1:
    st.plotly_chart(zip_airbnb_fig)

with column2:
    type_price_fig = px.box(df_airbnb_zip, x="room_type", y="price",
                            title = f'Airbnbn Average Price is ${int(mean_airbnb_zip)} and Price Boxplot By type in Zip {inquiry_zip} ',
                            template="simple_white")
    st.plotly_chart(type_price_fig,use_container_width= True)




#df_airbnb_zip['latitude'].tolist()[0]
st.pydeck_chart(pdk.Deck(
     map_style='mapbox://styles/mapbox/light-v9',
     initial_view_state=pdk.ViewState(
         latitude=float(df_airbnb_zip['latitude'].tolist()[0]),
         longitude=float(df_airbnb_zip['longitude'].tolist()[0]),
         zoom=11,
         pitch=50,
     ),
     layers=[
         pdk.Layer(
            'HexagonLayer',
            data=df_airbnb_zip,
            get_position='[longitude,latitude]',
            radius=200,
            elevation_scale=2,
            elevation_range=[0, 10],
            pickable=True,
            extruded=True,
         ),
         # pdk.Layer(
         #     'ScatterplotLayer',
         #     data=df_airbnb_zip,
         #     get_position='[longitude,latitude]',
         #     get_color='[200, 30, 0, 160]',
         #     get_radius=200,
         # ),
     ],
 ))
