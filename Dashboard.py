import streamlit as st
import os
import json
import pprint
import pandas as pd
import mysql.connector 
import plotly.express as px
from pages import function
from pages import mapfunction
from pages import chart

st.set_page_config(
    page_title = "Phone Pe Project Dashboard", 
    layout = "wide",
    initial_sidebar_state = "auto"
)

if 'first_button_clicked' not in st.session_state:
    st.session_state.first_button_clicked = False

if 'second_button_clicked' not in st.session_state:
    st.session_state.second_button_clicked = False

def on_click_first_button():
    st.session_state.first_button_clicked = True

def on_click_second_button():
    st.session_state.second_button_clicked = True

st.title("Dashboard")
tab1, tab2,tab3 = st.tabs(["Nation","State","Analysis"])
# this tab for country
with tab1:
    
    place = 'india'
    
    select = st.selectbox("select one",['transaction','stateinsurance','user'],index = 0)
    
    years =  function.no_of_year(select)
    select_year = st.selectbox('select year',years, index = len(years)-1)
       
    select_quater = st.selectbox('select quater',function.no_of_quater(select_year,select))
    
    if st.button('Submit'):
        on_click_first_button()

    if st.session_state.first_button_clicked:
        if select == "transaction":
            
            display_data = function.india_transaction_data(select_year,select_quater)
            
            st.divider()
            fig = chart.total_barchart(select)
            st.plotly_chart(fig,use_container_width = True)

            col1,col2,col3 = st.columns(3)
            with col1:
                st.subheader('All transactions count :')
                st.write(str(display_data[0]))
            with col2:
                st.subheader('All transactions Value :')
                st.write(f"₹ {str(display_data[1])}")
            with col3:
                st.subheader('Avg.value :')
                st.write(f"₹ {str(round(display_data[7],2))}")

            

            st.divider()
            st.subheader("Categories :-")
            
            col4,col5,col6,col7,col8 = st.columns([0.2,0.2,0.2,0.15,0.25])
            with col4:
                st.subheader('Merchant payments :')
                st.write(f"₹ {str(display_data[2])}")
            with col5:
                st.subheader('Peer-to-peer payments :')
                st.write(f"₹ {str(display_data[3])}")
            with col6:
                st.subheader('Recharge & bill payments :')
                st.write(f"₹ {str(display_data[4])}")
            with col7:
                st.subheader('Financial Services :')
                st.write(f"₹ {str(display_data[5])}")
            with col8:
                st.subheader('Others :')
                st.write(f"₹ {str(display_data[6])}")


            col11,col12 = st.columns([0.6,0.4])
            with col11:
                st.divider()
                fig = chart.quater_barchart(select,select_year)
                st.plotly_chart(fig,use_container_width = True)
            with col12:
                st.divider()
                fig = chart.category_piechart(select_year,select_quater)
                st.plotly_chart(fig,use_container_width = True)
            
            
            if st.button('Show GeoMap'):  
                on_click_second_button()
            col9,col10 = st.columns([0.7,0.3])
            with col9:
                if st.session_state.second_button_clicked:
                    st.divider()
                    st.subheader("Geo map")
                    geojsondata = mapfunction.geojson_data()
                    DataFrame = mapfunction.geo_map_data(select_year,select_quater)
                    fig = mapfunction.transaction_geo_map(geojsondata,DataFrame)
                    st.plotly_chart(fig,use_container_width = True)
            with col10:
                st.divider()
                st.subheader("Top 10 States")
                st.dataframe(function.top_10_transaction_state_df(function.top_10_transaction_state(select_year,select_quater)))
        
        if select == "stateinsurance":
            count,amount = function.fetch_insurance_count_amount(select_year,select_quater)[0]
            
            fig = chart.insurance_total_chart(select)
            st.plotly_chart(fig, use_container_width = True)
            
            Nation,Year,Quater,Count,Amount = st.columns(5)
            with Nation:
                st.subheader('Nation')
                st.write('India')
            with Year:
                st.subheader('Year')
                st.write(str(select_year))
            with Quater:
                st.subheader('Quater')
                st.write(str(select_quater))
            with Count:
                st.subheader('Count')
                st.write(str(count))
            with Amount:
                st.subheader('Amount')
                st.write(str(amount))

            if st.button('Show GeoMap'):  
                on_click_second_button()

            col6,col7 = st.columns([0.7,0.3])

            with col6:
                if st.session_state.second_button_clicked:
                    st.subheader("Geo map")
                    st.divider()
                    geojsondata = mapfunction.geojson_data()
                    fig = mapfunction.insurance_geo_map(geojsondata,select_year,select_quater)
                    st.plotly_chart(fig,use_container_width = True)
            with col7:
                st.subheader("Top 10 States")
                st.divider()
                st.dataframe(function.top_10_insurance_state_df(function.top_10_insurance_state(select_year,select_quater)))
        if select == 'user':
            regsiter_user,appopen = function.fetch_registeruser_appopen(select_year,select_quater)[0]

            fig = chart.user_total_chart(select)
            st.plotly_chart(fig, use_container_width = True)

            col1, col2, col3, col4, col5 = st.columns(5)
            with col1:
                st.subheader('Nation')
                st.write('India')
            with col2:
                st.subheader('Year')
                st.write(str(select_year))
            with col3:
                st.subheader('Quater')
                st.write(str(select_quater))
            with col4:
                st.subheader('Regsiter User')
                st.write(str(regsiter_user))
            with col5:
                st.subheader('App Opens')
                st.write(str(appopen))

            

            if st.button('Show GeoMap'):  
                on_click_second_button()

            col6,col7 = st.columns([0.7,0.3])
            with col6:
                if st.session_state.second_button_clicked:
                    st.subheader("Geo map")
                    st.divider()
                    geojsondata = mapfunction.geojson_data()
                    fig = mapfunction.user_geo_map(geojsondata,select_year,select_quater)
                    st.plotly_chart(fig,use_container_width = True)
            with col7:
                st.subheader("Top 10 States")
                st.divider()
                st.dataframe(function.top_10_user_state_df(function.top_10_user_state(select_year,select_quater)))

#this tab for state
with tab2:
    type_1 = st.selectbox('select Transaction/insurance/user',['transaction','insuranceindia','user'])
    if type_1 == 'transaction':
        fig = chart.state_transaction_chart()
        st.plotly_chart(fig, use_container_width= True)
    if type_1 == 'insuranceindia':
        fig = chart.state_insurance_chart()
        st.plotly_chart(fig, use_container_width= True)
    if type_1 == 'user':
        fig = chart.state_user_chart()
        st.plotly_chart(fig, use_container_width= True)
    
    col1,col2 = st.columns(2)
    with col1:
        state = function.state()
        state = st.selectbox('select one state', state)
        if type_1 == 'transaction':
            fig = chart.one_state_transaction_chart(state)
            st.plotly_chart(fig, use_container_width= True)
        if type_1 == 'insuranceindia':
            fig = chart.one_state_insurance_chart(state)
            st.plotly_chart(fig, use_container_width= True)
        if type_1 == 'user':
            fig = chart.one_state_user_chart(state)
            st.plotly_chart(fig, use_container_width= True)
    with col2:
        state_years =  function.no_of_year(type_1)
        year_ = st.selectbox('select a year',state_years, index = len(state_years)-1)
        if type_1 == 'transaction':
            fig = chart.one_state_year_transaction_chart(state,year_)
            st.plotly_chart(fig, use_container_width= True)
        if type_1 == 'insuranceindia':
            fig = chart.one_state_year_insurance_chart(state,year_)
            st.plotly_chart(fig, use_container_width= True)
        if type_1 == 'user':
            fig = chart.one_state_year_user_chart(state,year_)
            st.plotly_chart(fig, use_container_width= True)

with tab3:
    with st.expander("Yearly Growth"):
        st.text("""
                From 2019 to 2022, there is a marked increase in both the number of transactions and the total value, 
                showcasing the adoption of digital payments over traditional methods.
                """)
    with st.expander("Monthly Trends"):
        st.text("""
                Observing the monthly data, 
                we can see consistent growth with occasional spikes during festival seasons such as Diwali and New Year. 
                This seasonal variation highlights consumer spending patterns.
                """)

    with st.expander("Top States"):
        st.text("""
                Maharashtra shows the highest number of transactions, closely followed by Karnataka and Tamil Nadu. 
                This can be attributed to the high urban population and better internet penetration in these states.                    
                """)
    with st.expander("Growth in Tier-2 Cities"):
        st.text("""
                There is also notable growth in Tier-2 cities such as Jaipur, Indore, and Coimbatore, 
                indicating the spread of digital payment infrastructure beyond metro cities.
                """)
    with st.expander("Festive Season Impact"):
        st.text("""
                Analysis of quarterly data reveals that Q3 and Q4 generally see higher transaction volumes. 
                This is likely due to festivals like Diwali and Christmas, where consumer spending is higher.
                """)
    with st.expander("Urban vs Rural"):
        st.text("""
                Urban districts such as Mumbai, Bangalore Urban, and Chennai lead in transaction volumes. 
                In contrast, rural districts, although showing growth, still lag behind in absolute numbers.
                """)
    with st.expander("Emerging Districts"):
        st.text("""
                Districts like Pune and Gurugram show substantial growth, 
                indicating emerging urban centers adopting digital payments rapidly.
                """)
    with st.expander("UPI vs Other Methods"):
        st.text("""
                UPI transactions account for the majority of digital payments, 
                surpassing traditional card and net banking methods. 
                This is due to the instant and secure nature of UPI payments.
                """)
    with st.expander("Urban Dominance"):
        st.text("""
                Urban areas dominate in transaction volumes, 
                but rural areas are catching up with increasing internet penetration and digital literacy.
                """)
    with st.expander("Regional Variations"):
        st.text("""
                Southern states like Karnataka and Tamil Nadu show higher digital transaction volumes 
                compared to northern states, reflecting regional economic disparities.
                """)
    with st.expander("Economic Benefits"):
        st.text("""
                Benefits include increased transparency, 
                Reduced corruption, 
                And improved tax collection, 
                Contributing to overall economic health.
                """)
        