import os
import json
import pandas as pd
import mysql.connector 
import plotly.express as px


def geo_map(year,quater):
    geojson_path = "india_state_ut_administered.geojson"
    with open(geojson_path, 'r',encoding='utf-8') as geojson_open:
        geojson_data = json.load(geojson_open)
    # Create the choropleth map
    fig = px.choropleth(
        data_frame=geo_map_df(year,quater),
        geojson=geojson_data,
        featureidkey='properties.NAME_1',  
        locations='state',
        hover_data = ['count',
                    'avg_value',
                    'Merchant_payments',
                    'Peer_to_peer_payments',
                    'Recharge_and_bill_payments',
                    'Financial_Services',
                    'Others'],
        color='value',
        color_continuous_scale='Viridis',
        fitbounds = 'locations',
        scope="asia",
        basemap_visible = False
    )

    return fig   



# def location_select(geo_map_df):
#     states = geo_map_df['State']
#     location_select = ['india']
#     for i in states:
#         location_select.append(i)
#     return location_select

def india_state():
    State = ['andaman-&-nicobar-islands',
        'andhra-pradesh',
        'arunachal-pradesh',
        'assam',
        'bihar',
        'chandigarh',
        'chhattisgarh',
        'dadra-&-nagar-haveli-&-daman-&-diu',
        'delhi',
        'goa',
        'gujarat',
        'haryana',
        'himachal-pradesh',
        'jammu-&-kashmir',
        'jharkhand',
        'karnataka',
        'kerala',
        'lakshadweep',
        'madhya-pradesh',
        'maharashtra',
        'manipur',
        'meghalaya',
        'mizoram',
        'nagaland',
        'odisha',
        'puducherry',
        'punjab',
        'rajasthan',
        'sikkim',
        'tamil-nadu',
        'telangana',
        'tripura',
        'uttar-pradesh',
        'uttarakhand',
        'west-bengal']
    return State     

def geo_map_data(year,quater):
    india_states = india_state()
    data = []
    for state in india_states:
        fetch_data = state_transaction_data(state,year,quater)
        cleaned_data = display_transaction_state_data(fetch_data)
        cleaned_data['state'] = state
        data.append(cleaned_data)
    return data

def geo_map_df(year,quater):     
    data= geo_map_data(year,quater)
    df = pd.DataFrame(data)
    df.to_csv('C:/Users/GIRI/Desktop/New folder/state_dataframe.csv')
    return df

def mysqlconnector():
        connection = mysql.connector.connect(
            host = 'localhost',
            port = '3306',
            user  = 'root',
            password = '1234',
            database = 'phonepe'
        )
        return connection

def no_of_year():
    connection = mysqlconnector()
    cursor = connection.cursor()
    querry = f'select distinct(year) from transaction;'
    cursor.execute(querry)
    data = cursor.fetchall()
    connection.close()
    distinct_year = []
    for i in data:
        distinct_year.append(i[0])
    return distinct_year
    
#YEAR ----
#select * from transaction where year = 2020 and quater = Q1;
def india_transaction_data(year,quater):
    connection = mysqlconnector()
    cursor = connection.cursor()
    query = f'select * from india where year = {year} and quater = "{quater}";'
    cursor.execute(query)
    data = cursor.fetchall()
    connection.close()
    return data
#state transaction-----
def state_transaction_data(state,year,quater):
    connection = mysqlconnector()
    cursor = connection.cursor()
    query = f'select * from transaction where state = "{state}" and year = {year} and quater = "{quater}";'
    cursor.execute(query)
    data = cursor.fetchall()
    connection.close()
    return data

def display_transaction_india_data(data):
    display_data= {'count' : 0,
        'value' : 0,
        'avg_value': 0,
        'Merchant_payments' : 0,
        'Peer_to_peer_payments': 0,
        'Recharge_and_bill_payments' : 0,
        'Financial_Services' : 0,
        'Others' : 0}
    for i in data:
        
        display_data['count'] = display_data['count'] + int(i[3])
        display_data['value'] = display_data['value'] + float(i[4])
        
        if i[2] == 'Peer-to-peer payments':    
            display_data['Peer_to_peer_payments'] = float(i[4])
        if i[2] == 'Merchant payments':    
            display_data['Merchant_payments'] = float(i[4])
        if i[2] == 'Recharge & bill payments':    
            display_data['Recharge_and_bill_payments'] = float(i[4])
        if i[2] == 'Financial Services':    
            display_data['Financial_Services'] = float(i[4])
        if i[2] == 'Others':    
            display_data['Others'] = float(i[4])

    display_data['avg_value'] = round(display_data['value']/display_data['count'],2)
    return display_data

def display_transaction_state_data(data):
    display_data= {'count' : 0,
        'value' : 0,
        'avg_value': 0,
        'Merchant_payments' : 0,
        'Peer_to_peer_payments': 0,
        'Recharge_and_bill_payments' : 0,
        'Financial_Services' : 0,
        'Others' : 0}
    for i in data:
        
        display_data['count'] = display_data['count'] + int(i[4])
        display_data['value'] = display_data['value'] + float(i[5])
        
        if i[3] == 'Peer-to-peer payments':    
            display_data['Peer_to_peer_payments'] = float(i[5])
        if i[3] == 'Merchant payments':    
            display_data['Merchant_payments'] = float(i[5])
        if i[3] == 'Recharge & bill payments':    
            display_data['Recharge_and_bill_payments'] = float(i[5])
        if i[3] == 'Financial Services':    
            display_data['Financial_Services'] = float(i[5])
        if i[3] == 'Others':    
            display_data['Others'] = float(i[5])

    display_data['avg_value'] = round(display_data['value']/display_data['count'],2)
    return display_data

def insurance_data(year,quater):
    connection = mysqlconnector()
    cursor = connection.cursor()
    query = f'select * from insurance where year = "{year}" and quater = "{quater};"'
    cursor.execute(query)
    data = cursor.fetchall()
    connection.close()
    return data
if __name__ == '__main__':
    print(insurance_data(2020,'Q2'))
    