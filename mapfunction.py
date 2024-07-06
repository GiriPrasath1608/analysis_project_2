import os
import json
import pandas as pd
import mysql.connector 
import plotly.express as px
import streamlit as st

#____________MYSQL CONNECTION_________________________

def mysqlconnector():
        connection = mysql.connector.connect(
            host = 'localhost',
            port = '3306',
            user  = 'root',
            password = '1234',
            database = 'phonepe'
        )
        return connection

#__________________________LOAD GEOJSON DATA________________________

def geojson_data():
    geojson_path = "india_state_ut_administered.geojson"
    with open(geojson_path, 'r',encoding='utf-8') as geojson_open:
        geojsondata = json.load(geojson_open)
    return geojsondata

#_________________________CHOROPLETH MAP TRANSACATION______________________________

def transaction_geo_map(geojsondata,DataFrame):
    # Create the choropleth map
    fig = px.choropleth(
        data_frame=DataFrame,
        geojson=geojsondata,
        featureidkey='properties.NAME_1',  
        locations='state',
        color='amount',
        color_continuous_scale='Viridis',
        basemap_visible = False,
        fitbounds= 'locations',
        scope='asia',
        width = 800,
        height = 600 
    )
    return fig  

#_________________________CHOROPLETH MAP INSURANCE______________________________

# insurance geomap
def insurance_geo_map(geojsondata,year,quater):
    # Create the choropleth map
    fig = px.choropleth(
        data_frame=insurance_dataframe(insurance_data(year,quater)),
        geojson=geojsondata,
        featureidkey='properties.NAME_1',  
        locations='state',
        hover_data='amount',
        color='count',
        color_continuous_scale='Viridis',
        basemap_visible = False,
        fitbounds= 'locations',
        scope='asia',
        width = 800,
        height = 600 
    )
    return fig  

#_________________________CHOROPLETH MAP USER______________________________

# user geomap
def user_geo_map(geojsondata,year,quater):
    # Create the choropleth map
    fig = px.choropleth(
        data_frame=user_dataframe(fetch_user_data(year,quater)),
        geojson=geojsondata,
        featureidkey='properties.NAME_1',  
        locations='state',
        hover_data='appopens',
        color='registeredUsers',
        color_continuous_scale='Viridis',
        basemap_visible = False,
        fitbounds= 'locations',
        scope='asia',
        width = 800,
        height = 600    
    )
    return fig     

#_____________________FETCH TRANSACTION DATAFRAME______________________

def geo_map_data(year,quater):
    connection = mysqlconnector()
    cursor = connection.cursor()
    query = f'select year, quater, state,sum(amount) from transaction where {year} = year and quater = "{quater}" group by state;'
    cursor.execute(query)
    data = cursor.fetchall()
    connection.close()
    initial = []
    for i in data:
        i = list(i)
        i[3] = int(i[3])
        initial.append(i)
    df = pd.DataFrame(initial, columns = ['year', 'quater', 'state', 'amount'])
    return df


#_____________________FETCH INSURANCE DATAFRAME______________________ 

def insurance_data(year,quater):
    connection = mysqlconnector()
    cursor = connection.cursor()
    query = f'select * from stateinsurance where year = "{year}" and quater = "{quater}";'
    cursor.execute(query)
    data = cursor.fetchall()
    connection.close()
    return data

def insurance_dataframe(data):
    df = pd.DataFrame(data,columns=['state','year','quater','count','amount'])
    return df

#_____________________FETCH USER DATAFRAME______________________

def fetch_user_data(year,quater):
    connection = mysqlconnector()
    cursor = connection.cursor()
    query = f'select * from user where year = {year} and quater = "{quater}";'
    cursor.execute(query)
    data = cursor.fetchall()
    connection.close()
    return data

def user_dataframe(data):
    df = pd.DataFrame(data, columns=['state', 'year', 'quater', 'registeredUsers', 'appopens'])
    return df
