# Engineering Project
## End-to-end Data Engineering Pipeline of San Diego Airbnb Analysis

### Question/Need:

- What is the end service that your project will provide? What is the purpose of the system you plan to build?

The Project will build a end-to-end data Engineering pipeline to provide statistical nearby airbnb property information for an interested property given zip, bedroom information



- Who is your client and how will that client benefits from your end service?
  - Note: What we’re looking for here is more about who would be interested in the practical application of your work rather than details of a specific organization.

People who are interested in airbnb business in San Diego.

- What does your end-to-end data pipeline look like? You should submit a preliminary sketch of your pipeline in the form of a diagram or workflow list with your proposal. For more directions and examples see the Data Pipeline and Project Workflow pages.

![image](https://github.com/PurpleGrace/Engineering_SD_housing_Analysis/blob/main/Proposal/flowchart.png)



### Data Description:

- What dataset(s) do you plan to use, and how will you obtain the data? Please include a link! (The link can be to the dataset you’re downloading, the site you’re scraping, etc.)

The dataset the project is going to use is from [zillow](https://www.zillow.com/research/data/) and [insideairbnb](http://insideairbnb.com/index.html),potentially also from redfin. Zillow provides estimated market value increase in the next year at different level of county and zipcode. Insideairbnb offer San Diego airbnb data up to the end of 2021.

- Do you plan to be able to automatically pull in new data at a regular cadence (e.g with Airflow or a cron job)?  

The project plan to automatically pull data only once, not at a regular cadence.

- What is an individual sample/unit of analysis in this project? In other words, what does one row or observation of the data represent?

The individual one row of the data represent information of an airbnb property listing, including owner, price, location, address, reviews, description, availability and etc.

- What characteristics/features do you expect to work with? In other words, what are your columns of interest?

Property zipcode, location, bedroom number, bathroom number, renting price and etc.

- If modeling, what will you predict as your target?
No plan for Modeling




###  Tools:
- How do you intend to meet the tools requirements of the project (data storage solution and at least one tool for cloud computing, big data handling, or web deployment)?

The project is going to use mysql for data storage solution and use flask or Streamlit for app deployment.

- Are you planning in advance to need or use additional tools beyond those required?

To be decided.

### MVP Goal:
- What would a minimum viable product (MVP) look like for this project?

Basic web deployment.
