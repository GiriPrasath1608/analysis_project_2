import pandas as pd
import mysql.connector 
import plotly.express as px
import function
import mapfunction

#__________________________transaction category pie chart_____________
def category_piechart(year,quater):
    data = function.india_transaction_data(year,quater)
    data=data[2:len(data)-1]
    name = ["Merchant payments","Peer-to-peer payments","Recharge & bill payments","Financial Services","Others"]
    new_data = []
    for i in data:
        new_data.append(int(i))
    df = pd.DataFrame({'type':name,'values':new_data})
    fig = px.pie(df,names = 'type',
                values = 'values',
                color = 'type',
                color_discrete_sequence = ['red','green','blue','yellow','orange'],
                title = f'Categories Of Transaction in {year} {quater}'
                )
    return fig

#___________________________transaction quater wise data in a year________________

def quater_barchart(type,year):
    initial=[]
    quater = function.no_of_quater(year,type)
    if len(quater) == 4:
        for j in quater:
            data = function.india_transaction_data(year,j)
            data=data[2:len(data)-1]
            new_data = []
            for i in data:
                new_data.append(int(i))
            name = ["Merchant payments","Peer-to-peer payments","Recharge & bill payments","Financial Services","Others"]
            for k in range(len(name)):
                initial.append([year,j,name[k],new_data[k]])
    df = pd.DataFrame(initial,columns=['year','quater','categories','amount'])
    fig = px.bar(df,
                x = 'quater',
                y = 'amount',
                color = 'categories',
                color_discrete_sequence = ['red','green','blue','yellow','orange'],
                title = f'Quater wise data in year {year}'
                )
    return fig

#____________________________transaction total bar chart_______________

def total_barchart(type):
    year = function.no_of_year(type)
    initial=[]
    for l in year:
        quater = function.no_of_quater(l,type)
        if len(quater) == 4:
            for j in quater:
                data = function.india_transaction_data(l,j)
                data=data[2:len(data)-1]
                new_data = []
                for i in data:
                    new_data.append(int(i))
                name = ["Merchant payments","Peer-to-peer payments","Recharge & bill payments","Financial Services","Others"]
                for k in range(len(name)):
                    initial.append([l,j,name[k],new_data[k]])
    df = pd.DataFrame(initial,columns=['year','quater','categories','amount'])
    fig = px.bar(df,
                x = 'year',
                y = 'amount',
                color = 'categories',
                color_discrete_sequence = ['red','green','blue','yellow','orange'],
                title = f'Year wise data'
                )
    return fig

#_______________ INSURANCE CHART____________

def insurance_total_chart(type):
    year = function.no_of_year(type)
    initial=[]
    for i in year:
        quater = function.no_of_quater(i,type)
        if len(quater) == 4:
            count_init = 0
            amount_init = 0
            for j in quater:
                count,amount = function.fetch_insurance_count_amount(i,j)[0]
                count_init = count_init + count
                amount_init = amount_init + amount
            initial.append([str(i),count_init,amount_init])
            df = pd.DataFrame(initial,columns = ['year', 'count', 'amount'])
            fig1 = px.bar(data_frame=df, 
                        x = 'year',
                        y = 'amount', 
                        color_discrete_sequence=['blue'],
                        title = 'Insurance')
            fig2 = px.line(data_frame=df, 
                        x = 'year',
                        y = 'amount', 
                        color_discrete_sequence=['green'])
            fig3 = px.scatter(data_frame=df,
                            x = 'year',
                            y = 'amount', 
                            color_discrete_sequence=['black'])
            for trace in fig2.data:
                fig1.add_trace(trace)
            for trace in fig3.data:
                fig1.add_trace(trace)
            fig1.update_layout(xaxis_type = 'category')
    return fig1

#_______________________user chart _________________________
#_______________ INSURANCE CHART____________

def user_total_chart(type):
    year = function.no_of_year(type)
    initial=[]
    for i in year:
        quater = function.no_of_quater(i,type)
        if len(quater) == 4:
            registeredUsers = 0
            appOpens = 0
            for j in quater:
                Users,Opens = function.fetch_registeruser_appopen(i,j)[0]
                registeredUsers = registeredUsers + Users
                appOpens = appOpens + Opens
            initial.append([str(i),registeredUsers,appOpens])
            df = pd.DataFrame(initial,columns = ['year', 'registeredUsers', 'appOpens'])
            fig1 = px.bar(data_frame=df, 
                        x = 'year',
                        y = 'registeredUsers', 
                        color_discrete_sequence=['blue'],
                        title = 'Insurance')
            fig2 = px.line(data_frame=df, 
                        x = 'year',
                        y = 'registeredUsers', 
                        color_discrete_sequence=['green'])
            fig3 = px.scatter(data_frame=df,
                            x = 'year',
                            y = 'registeredUsers', 
                            color_discrete_sequence=['black'])
            for trace in fig2.data:
                fig1.add_trace(trace)
            for trace in fig3.data:
                fig1.add_trace(trace)
            fig1.update_layout(xaxis_type = 'category')
    return fig1

#_______________chart state wise____________
def state_transaction_chart():
    type = 'transaction'
    year = function.no_of_year(type)
    initial={'state':[], 'amount':[]}
    for i in year:
        quater = function.no_of_quater(i,type)
        for j in quater:
            data = mapfunction.geo_map_data(i,j)
            initial['state'] = initial['state'] + list(data['state'])
            initial['amount'] = initial['amount'] + list(data['amount'])
    df = pd.DataFrame(initial)
    fig = px.bar(
        data_frame = df,
        x = 'state',
        y = 'amount',
        color_discrete_sequence= ['blue'],
        title = 'overall transaction of india'
    )
    return fig

#_________________state user chart india______________
def state_user_chart():
    type = 'user'
    year = function.no_of_year(type)
    initial=[]
    for i in year:
        quater = function.no_of_quater(i,type)
        for j in quater:
            data = mapfunction.fetch_user_data(i,j)
            for d in data:
                initial.append(d)

    df = pd.DataFrame(initial , columns = ['state', 'year', 'quater', 'regsiter_user','appopen'])
    fig = px.bar(
        data_frame=df,
        x = 'state',
        y = 'regsiter_user',
        color_discrete_sequence = ['blue'],
        title = 'Users over all india'
    )
    return fig

#___________________________state insurance chart___________________
def state_insurance_chart():
    type = 'insuranceindia'
    year = function.no_of_year(type)
    initial=[]
    for i in year:
        quater = function.no_of_quater(i,type)
        for j in quater:
            data = mapfunction.insurance_data(i,j)
            for d in data:
                initial.append(d)
    df = pd.DataFrame(initial , columns = ['state', 'year', 'quater', 'count', 'amount'])
    fig = px.bar(
    data_frame=df,
    x = 'state',
    y = 'count',
    color_discrete_sequence = ['blue'],
    title = 'insurance over all india'
    )
    return fig

#______________________overall transaction in one state___________________
def one_state_transaction_chart(state):
    type = 'transaction'
    year = function.no_of_year(type)
    initial={'year':[], 'state':[], 'amount':[]}
    for i in year:
        quater = function.no_of_quater(i,type)
        for j in quater:
            data = mapfunction.geo_map_data(i,j)
            initial['year'] = initial['year'] + list(data['year'])
            initial['state'] = initial['state'] + list(data['state'])
            initial['amount'] = initial['amount'] + list(data['amount'])
    df = pd.DataFrame(initial)
    fig = px.bar(
        data_frame = df[df['state']==state],
        x = 'year',
        y = 'amount',
        color_discrete_sequence= ['blue'],
        title = f'overall transaction of {state}'
    )
    return fig
#_________________state user chart on one state______________
def one_state_user_chart(state):
    type = 'user'
    year = function.no_of_year(type)
    initial=[]
    for i in year:
        quater = function.no_of_quater(i,type)
        for j in quater:
            data = mapfunction.fetch_user_data(i,j)
            for d in data:
                initial.append(d)

    df = pd.DataFrame(initial , columns = ['state', 'year', 'quater', 'regsiter_user','appopen'])
    fig = px.bar(
        data_frame=df[df['state']==state],
        x = 'year',
        y = 'regsiter_user',
        color_discrete_sequence = ['blue'],
        title = f'Users over all {state}'
    )
    return fig

#___________________________state insurance chart on one state___________________
def one_state_insurance_chart(state):
    type = 'insuranceindia'
    year = function.no_of_year(type)
    initial=[]
    for i in year:
        quater = function.no_of_quater(i,type)
        for j in quater:
            data = mapfunction.insurance_data(i,j)
            for d in data:
                initial.append(d)
    df = pd.DataFrame(initial , columns = ['state', 'year', 'quater', 'count', 'amount'])
    fig = px.bar(
    data_frame=df[df['state']==state],
    x = 'year',
    y = 'count',
    color_discrete_sequence = ['blue'],
    title = f'insurance over all {state}'
    )
    return fig

#______________STATE TRANSACTION PREFORMANCE IN THAT YEAR______________________

def one_state_year_transaction_chart(state, year_):
    type = 'transaction'
    year = function.no_of_year(type)
    initial={'year':[], 'quater':[],'state':[], 'amount':[]}
    for i in year:
        quater = function.no_of_quater(i,type)
        for j in quater:
            data = mapfunction.geo_map_data(i,j)
            initial['year'] = initial['year'] + list(data['year'])
            initial['quater'] = initial['quater'] + list(data['quater'])
            initial['state'] = initial['state'] + list(data['state'])
            initial['amount'] = initial['amount'] + list(data['amount'])
    df = pd.DataFrame(initial)
    fig = px.bar(
        data_frame = df[(df['state']==state) & (df['year']==year_)],
        x = 'quater',
        y = 'amount',
        color_discrete_sequence= ['blue'],
        title = f'overall transaction of {state} in year {year_}'
    )
    return fig
#_________________state user chart on THAT ONE YEAR______________
def one_state_year_user_chart(state, year_):
    type = 'user'
    year = function.no_of_year(type)
    initial=[]
    for i in year:
        quater = function.no_of_quater(i,type)
        for j in quater:
            data = mapfunction.fetch_user_data(i,j)
            for d in data:
                initial.append(d)

    df = pd.DataFrame(initial , columns = ['state', 'year', 'quater', 'regsiter_user','appopen'])
    fig = px.bar(
        data_frame=df[(df['state']==state) & (df['year']==year_)],
        x = 'quater',
        y = 'regsiter_user',
        color_discrete_sequence = ['blue'],
        title = f'Users over all {state} in year {year_}'
    )
    return fig

#___________________________state insurance chart on THAT ONE YEAR___________________
def one_state_year_insurance_chart(state, year_):
    type = 'insuranceindia'
    year = function.no_of_year(type)
    initial=[]
    for i in year:
        quater = function.no_of_quater(i,type)
        for j in quater:
            data = mapfunction.insurance_data(i,j)
            for d in data:
                initial.append(d)
    df = pd.DataFrame(initial , columns = ['state', 'year', 'quater', 'count', 'amount'])
    fig = px.bar(
    data_frame=df[(df['state']==state) & (df['year']==year_)],
    x = 'quater',
    y = 'count',
    color_discrete_sequence = ['blue'],
    title = f'insurance over all {state} in year {year_}'
    )
    return fig
