import requests
import time
from bs4 import BeautifulSoup

# Seleccionar el recurso a descargar
resource_url = "https://www.macrotrends.net/stocks/charts/TSLA/tesla/revenue"

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
}
 
response = requests.get(resource_url, headers=headers)
 
if response.status_code == 200:
    print(response.text)  # Print the content of the response
else:
    print(f'Request failed with status code: {response.status_code}')

soup = BeautifulSoup(response.text, 'html')
soup
print(soup())


import re

# Obtener todos los elementos de tipo 'span' del documento HTML
tables = soup.find_all("table")


revenue_table= soup.find("table", class_="historical_data_table")
print(revenue_table)

import pandas as pd

for index, table in enumerate(tables):
    if ("Tesla Quarterly Revenue" in str(table)):
        table_index = index
        break
    
# Defining of the dataframe
quarterly_revenue = pd.DataFrame(columns=['Date', 'Revenue'])

# Collecting Ddata
for row in soup.find_all("table")[1].tbody.findAll('tr'):
    # Find all data for each column
    columns = row.find_all('td')
    if(columns != []):
        date = columns[0].text.strip()
        revenue = columns[1].text.replace(",", "").replace("$", "")
        data= pd.DataFrame([[date,revenue]], columns=['Date','Revenue'])   
        quarterly_revenue=pd.concat([quarterly_revenue,data], ignore_index=True)
print(quarterly_revenue.head())

quarterly_df = quarterly_revenue[quarterly_revenue["Revenue"] != ""]
print(quarterly_df.head())

import sqlite3

connection = sqlite3.connect("Tesla_revenue.db")
connection

cursor = connection.cursor()

#Creating the table
cursor.execute("""CREATE TABLE Quarterly_Revenue (Date, Revenue)""")

#Adding the data
quarterly_df.to_sql('Quarterly_Revenue', con=connection, if_exists='replace', index = False)

connection.commit()

# Checking the data
for row in cursor.execute("SELECT * FROM Quarterly_Revenue"):
    print(row)

import matplotlib.pyplot as plt
import seaborn as sns


#Revenue trend over time

quarterly_df['Date'] = pd.to_datetime(quarterly_df['Date'])
quarterly_df["Revenue"] = quarterly_df["Revenue"].astype('int')

plt.figure(figsize = (10, 5))

sns.lineplot(data= quarterly_df, x='Date', y='Revenue')
plt.tight_layout()

plt.show()


#Monthly revenue distribution

plt.figure(figsize = (10, 5))
quarterly_df['Date'] = pd.to_datetime(quarterly_df['Date'])
monthly_distribution= quarterly_df.groupby(quarterly_df['Date'].dt.month).sum().reset_index()

sns.barplot(data= monthly_distribution, x = "Date", y = "Revenue")

plt.show()


#Yearly revenue distribution

plt.figure(figsize = (10, 5))
quarterly_df['Date'] = pd.to_datetime(quarterly_df['Date'])
monthly_distribution= quarterly_df.groupby(quarterly_df['Date'].dt.year).sum().reset_index()

sns.barplot(data= monthly_distribution, x = "Date", y = "Revenue")

plt.show()
