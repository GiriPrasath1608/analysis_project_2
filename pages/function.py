import os
import json
import pandas as pd
import mysql.connector 
import plotly.express as px
import streamlit as st
from pages import mapfunction

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

#______________________SELECT YEAR___________________________________

def no_of_year(type):
    connection = mysqlconnector()
    cursor = connection.cursor()
    query = f'select distinct(year) from {type};'
    cursor.execute(query)
    data = cursor.fetchall()
    connection.close()
    distinct_year = []
    for i in data:
        distinct_year.append(i[0])
    return distinct_year

#___________________________SELECT QUATER_________________________________

def no_of_quater(year,type):
    connection = mysqlconnector()
    cursor = connection.cursor()
    querry = f'select distinct(quater) from {type} where year = {year};'
    cursor.execute(querry)
    data = cursor.fetchall()
    connection.close()
    distinct_quater = []
    for i in data:
        distinct_quater.append(i[0])
    return distinct_quater



def clear_cache():
    st.cache_data.clear()

#____________________TRANSACTION DISPLAY DATA___________________

def india_transaction_data(year,quater):
    display_data_list = []
    
    connection = mysqlconnector()
    cursor = connection.cursor()
    query = [
        f'select sum(count) from india where year = {year} and quater = "{quater}";',
        f'select sum(amount) from india where year = {year} and quater = "{quater}";',
        f'select sum(amount) from india where year = {year} and quater = "{quater}" and type = "Merchant payments";',
        f'select sum(amount) from india where year = {year} and quater = "{quater}" and type = "Peer-to-peer payments";',
        f'select sum(amount) from india where year = {year} and quater = "{quater}" and type = "Recharge & bill payments";',
        f'select sum(amount) from india where year = {year} and quater = "{quater}" and type = "Financial Services";',
        f'select sum(amount) from india where year = {year} and quater = "{quater}" and type = "Others";'
    ]
    for q in query:
        cursor.execute(q)
        data = cursor.fetchall()
        display_data_list.append(data[0][0])
    connection.close()
    display_data_list.append(display_data_list[1]/display_data_list[0])
    return display_data_list

#________________________INSURANCE DISPLAY DATA_________________________

def fetch_insurance_count_amount(year,quater):
    connection = mysqlconnector()
    cursor = connection.cursor()
    query = f'select count,amount from insuranceindia where year = {year} and quater = "{quater}";'
    cursor.execute(query)
    data = cursor.fetchall()
    connection.close()
    return data

#___________________USER DISPLAY DATA__________________________________

def fetch_registeruser_appopen(year,quater):
    connection = mysqlconnector()
    cursor = connection.cursor()
    query = f'select registeredUsers,appOpens from indiauser where year = {year} and quater = "{quater}";'
    cursor.execute(query)
    data = cursor.fetchall()
    connection.close()
    return data

#_________________ TOP 10 STATES USER ___________________

def top_10_user_state(year,quater):
    connection = mysqlconnector()
    cursor = connection.cursor()
    query = f'select state,registeredUsers from user where year = {year} and quater = "{quater}" order by registeredUsers desc limit 10;'
    cursor.execute(query)
    data = cursor.fetchall()
    connection.close()
    return data

def top_10_user_state_df(data):
    df = pd.DataFrame(data, columns = ['state','registeredUsers'],index= range(1,11))
    return df

#_________________ TOP 10 STATES INSURANCE ___________________

def top_10_insurance_state(year,quater):
    connection = mysqlconnector()
    cursor = connection.cursor()
    query = f'select state, count from stateinsurance where year = {year} and quater = "{quater}" order by count desc limit 10;'
    cursor.execute(query)
    data = cursor.fetchall()
    connection.close()
    return data

def top_10_insurance_state_df(data):
    df = pd.DataFrame(data, columns = ['state', 'count'],index= range(1,11))
    return df

#_________________ TOP 10 STATES TRANSACTION ___________________

def top_10_transaction_state(year,quater):
    connection = mysqlconnector()
    cursor = connection.cursor()
    query = f'select state, sum(amount) as amount from transaction where year = {year} and quater = "{quater}" group by state order by amount desc limit 10;'
    cursor.execute(query)
    data = cursor.fetchall()
    connection.close()
    return data

def top_10_transaction_state_df(data):
    df = pd.DataFrame(data, columns = ['state', 'amount'],index= range(1,11))
    return df

def state():
    data = mapfunction.geo_map_data(2023,'Q1')
    state = list(data['state'])
    return state

# if __name__ == '__main__':
#     year = 2024
#     quater = 'Q1'
#     print(geo_map_data(year,quater))
    
    