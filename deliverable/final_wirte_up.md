# Engineering Project
## End-to-end data pipeline and Dashboard for San Diego Housing Market

### Abstract
San Diego is a hot place for jobs, travelers and is one of the places with most housing increase in the past few years. So San Diego attracted many investors or home buyers. The information about San Diego housing market is scattered here and there on the internet. This project aims to build an end-to-end pipeline and a Dashboard for informations that interest holders would like to know before spending their money

### Design
The pipeline is going to fetch data from insideairbnb.com, read data which has been collected from Zillow and San Diego MLS, create a database and save all related dataset into the database. The dashboard app will read data from database, after manipulation and visualize data info by using Streamlit.


### Data
 The data is collected from three resources. The first one is from insideairbnb which gives all airbnb listing in San Diego. The dataset contains feature like ID, latitude, longitude, price per night, room type, review numbers and etc. The second resources is from Zillow. We would like to offer the info of the value index, rent index and also potential value increase index of one specific zip code area estimated by Zillow. The third one is from San Diego multiple Listing System, the system record every selling transaction and part of rentals. We would calculate and offer our interest holder the average rental/selling in the last three month by zip, bedroom numbers, bathroom numbers and home type.  



### tools
- Numpy and Pandas for data manipulation.
- request, b4 for data scraping
- MySql for data storage and data query
- Streamlit for app deployment
- Plotly for geographic plots
- geopy for transfer latitude and longitude to zip code

### Dashboard
![image](https://github.com/PurpleGrace/Engineering_SD_housing_Analysis/blob/main/deliverable/Dashboard1.png)
![image](https://github.com/PurpleGrace/Engineering_SD_housing_Analysis/blob/main/deliverable/Dashboard2.png)

### Communications
A PPT presentation will be presented.
