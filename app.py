import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import time
import plotly.express as px

df = pd.read_csv('country_profile_variables.csv')

df1 = df[['country', 'Region', 'Surface area (km2)',
       'Population in thousands (2017)', 'Population density (per km2, 2017)',
       'Sex ratio (m per 100 f, 2017)',
       'GDP: Gross domestic product (million current US$)',
       'GDP growth rate (annual %, const. 2005 prices)',
       'GDP per capita (current US$)', 'Economy: Agriculture (% of GVA)',
       'Economy: Industry (% of GVA)',
       'Economy: Services and other activity (% of GVA)',
       'Employment: Agriculture (% of employed)',
       'Employment: Industry (% of employed)',
       'Employment: Services (% of employed)',
       'Life expectancy at birth (females/males, years)',  
       'CO2 emission estimates (million tons/tons per capita)']]

# Data Cleaning and Processing
df1['Surface area (km2)'] = df1['Surface area (km2)'].str.replace('~', '')
df1['Surface area (km2)'] = pd.to_numeric(df1['Surface area (km2)'])

df1['GDP growth rate (annual %, const. 2005 prices)'] = df1['GDP growth rate (annual %, const. 2005 prices)'].str.replace('-~', '')
df1['GDP growth rate (annual %, const. 2005 prices)'] = pd.to_numeric(df1['GDP growth rate (annual %, const. 2005 prices)'])

df1['Economy: Agriculture (% of GVA)'] = pd.to_numeric(df1['GDP growth rate (annual %, const. 2005 prices)'])

df1['Employment: Agriculture (% of employed)'] = df1['Employment: Agriculture (% of employed)'].str.replace('...', '')
df1['Employment: Agriculture (% of employed)'] = pd.to_numeric(df1['Employment: Agriculture (% of employed)'])
df1['Employment: Agriculture (% of employed)'] = df1['Employment: Agriculture (% of employed)'].fillna(0)

df1['Employment: Industry (% of employed)'] = df1['Employment: Industry (% of employed)'].str.replace('...', '')
df1['Employment: Industry (% of employed)'] = pd.to_numeric(df1['Employment: Industry (% of employed)'])
df1['Employment: Industry (% of employed)'] = df1['Employment: Industry (% of employed)'].fillna(0)

df1['Employment: Services (% of employed)'] = df1['Employment: Services (% of employed)'].str.replace('...', '')
df1['Employment: Services (% of employed)'] = pd.to_numeric(df1['Employment: Services (% of employed)'])
df1['Employment: Services (% of employed)'] = df1['Employment: Services (% of employed)'].fillna(0)

# function creation for country specific Analysis 
def country_event_heatmap(df1,country):
    new_df1 = df1[df1['country'] == country]
    pt = new_df1.pivot_table(index=country,aggfunc='count').fillna(0)
    return pt

 # prerequisite for Scatter plot
global numric_columns
try:
   numeric_columns = list(df1.select_dtypes(['float','int']).columns)
except Exception as e:
    print(e)


# Sidebar for the WebApp
st.sidebar.title('Country Statistics Analysis')
my_page = st.sidebar.radio('Select an Option', ['Overall Analysis','Numeric Analysis','Country Specific Analysis'])
st.title('My Data Analysis Web App')
st.sidebar.image('juliana-kozoski-IoQioGLrz3Y-unsplash.jpg')

if my_page == 'Overall Analysis':
    st.header('Overall Analysis Performed on the Dataset')
    # Bar Chart
    st.subheader('1) Top 5 Regions based on their Surface Area')
    st.bar_chart(x='Region', 
            y='Surface area (km2)',
            data=df1.nlargest(5, 'Surface area (km2)'))

    # Pie Chart
    st.subheader('2) Top 5 Countries based on their Population')
    c = df1.groupby('country')['Population in thousands (2017)'].sum().round().reset_index()
    ans = c.sort_values('Population in thousands (2017)',ascending=False).head(5)
    explode = (0, 0.1, 0, 0,0)
    fig2, ax1 = plt.subplots()
    ax1.pie(ans['Population in thousands (2017)'], explode=explode, labels=ans['country'], autopct='%1.1f%%',shadow=True, startangle=90)
    ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    st.pyplot(fig2)

    # Heat Map
    st.subheader('3) Heatmap For All Columns')
    pt = pd.pivot_table(df1,index=['country'])
    fig_3, ax = plt.subplots()
    sns.heatmap(pt)
    st.write(fig_3)

    # Table
    st.subheader("4) Top 10 countries based on GDP Per Capita ")
    gby = df1.groupby('country')['GDP per capita (current US$)'].sum().round().reset_index()
    ans = gby.sort_values('GDP per capita (current US$)',ascending=False).head(10)
    st.table(ans)

    # Bar Chart for life expectancy
    fig_4 = px.bar(df1,x='Region',y='Life expectancy at birth (females/males, years)')
    st.plotly_chart(fig_4)

    # Catplot
    op = df1.groupby('country')['CO2 emission estimates (million tons/tons per capita)'].sum().round().reset_index()
    op = op.sort_values('CO2 emission estimates (million tons/tons per capita)',ascending=False).head(5)
    fig_9 = sns.catplot(data=op, x='country',y='CO2 emission estimates (million tons/tons per capita)',color='pink')
    plt.xticks(rotation=45)
    st.pyplot(fig_9)

# Numeric Analysis Page
elif my_page == 'Numeric Analysis':
    st.header('Welcome to the Numeric Analysis Page:')
    chart_select = st.selectbox(
        label = 'Select the Chart Type',
        options=['Scatterplots','Histogram','Boxplot']
    )
    
    #Scatterplot
    if chart_select == 'Scatterplots':
        st.subheader('Scatterplots Settings')
        try:
            x_values = st.selectbox('X axis', options= numeric_columns)
            y_values = st.selectbox('Y axis', options= numeric_columns)
            fig_5 = px.scatter(df1, x = x_values, y = y_values)
            st.plotly_chart(fig_5)
        except Exception as e:
            print(e)
    
    #Histogram
    elif chart_select == 'Histogram':
        st.subheader('Plotted Histogram')
        try:
            x_values = st.selectbox('X axis', options= numeric_columns)
            fig_6 = px.histogram(df1, x = x_values)
            st.plotly_chart(fig_6)
        except  Exception as e:
            print(e)

    # Boxplot
    elif chart_select == 'Boxplot':
        st.subheader('Boxplot')
        try:
            y_values = st.selectbox('Y axis', options= numeric_columns)
            fig_7 = px.box(df1, y = y_values)
            st.plotly_chart(fig_7)
        except  Exception as e:
            print(e)

# Country Specific Analysis Page
elif my_page == 'Country Specific Analysis':
    st.header('Welcome to Country Specific Analysis Page:')

    country_list = df['country'].tolist()
    country_list.sort()

    selected_country = st.selectbox('Select a Country',country_list)

    st.title(' Country Wise Heatmap')
    pt = country_event_heatmap(df1,selected_country)
    fig_8, ax = plt.subplots()
    sns.heatmap(pt,annot=True)
    st.write(fig_8)

# Spinner
with st.spinner("Loading..."):
    time.sleep(5)
st.success("Done!")

