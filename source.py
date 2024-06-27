import streamlit as st
import os
import json
import pprint
import pandas as pd
import mysql.connector 
import plotly.express as px
import function


st.set_page_config(
    page_title = "Phone Pe Project Dashboard", 
    layout = "wide",
    initial_sidebar_state = "auto"
)


st.title("Dashboard")
tab1, tab2 = st.tabs(["Nation","State"])
with tab1:

    place = 'india'
    
    select = st.selectbox("select one",["Transaction","Insurance","User"],index = 0)

    select_year = st.selectbox('select year',function.no_of_year())
       
    select_quater = st.selectbox('select quater',['Q1','Q2','Q3','Q4'])
    
    col1,col2 = st.columns([0.7,0.3])
    
    with col1:
        st.header("Geo map")
        st.divider()
        fig = function.geo_map(select_year,select_quater)
        st.plotly_chart(fig)
        
            
    with col2:
        st.header(f'{place}-{select}-{select_year}-{select_quater}')
        st.divider()

        if select == "Transaction":
            if place == 'india':
                data = function.india_transaction_data(select_year,select_quater)
                display_data = function.display_transaction_india_data(data)
            if place != 'india':
                data = function.state_transaction_data(place,select_year,select_quater)
                display_data = function.display_transaction_state_data(data)

            st.write(f"All transactions count : {display_data['count']}")
            st.write(f"All transactions Value : ₹ {display_data['value']}")
            st.write(f"Avg.value : ₹ {display_data['avg_value']}")

            st.subheader("Categories")
            st.divider()

            st.write(f"Merchant payments : ₹ {display_data['Merchant_payments']}")
            st.write(f"Peer-to-peer payments : ₹ {display_data['Peer_to_peer_payments']}")
            st.write(f"Recharge & bill payments : ₹ {display_data['Recharge_and_bill_payments']}")
            st.write(f"Financial Services : ₹ {display_data['Financial_Services']}")
            st.write(f"Others : ₹ {display_data['Others']}")

        if select == "Insurance":
            count = 9398466
            value = 5674745
            avg_value = 564

            st.write(f"All transactions : {count}")
            st.write(f"Value : {value}")
            st.write(f"Avg.value : {avg_value}")



