import streamlit as st
import pandas as pd
import numpy as np
import preprocessor,helper
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns


df = pd.read_excel('athlete_events.xlsb')
region_df = pd.read_csv('noc_regions.csv')

df = preprocessor.preprocess(df,region_df)


st.sidebar.title("Olympics Analysis")
image_path = 'olympics.jpeg'

user_menu = st.sidebar.radio(
    'Select An Option',
    ('Medal Tally', 'Overall Analysis', 'Country-wise-Analysis', 'Athlete-wise-Analysis')
    )

if user_menu == 'Medal Tally':
    st.sidebar.header("Medal Tally")
    years,country = helper.country_year_list(df)

    selected_year = st.sidebar.selectbox("Select Year",years)
    selected_country = st.sidebar.selectbox("Select Country", country)

    medal_tally = helper.fetch_medal_tally(df,selected_year,selected_country)
    
    if selected_year == 'Overall' and selected_country == 'Overall':
        st.title("Overall Tally")
    if selected_year != 'Overall' and selected_country == 'Overall':
        st.title("Medal Tally in " + str(selected_year) + " Olympics")
    if selected_year == 'Overall' and selected_country != 'Overall':
        st.title(selected_country + " overall performance")
    if selected_year != 'Overall' and selected_country != 'Overall':
        st.title(selected_country + " performance in " + str(selected_year) + " Olympics")
        
    st.table(medal_tally)


if user_menu == 'Overall Analysis':
    
    st.title("Top Statistics")
    
    editions = df['Year'].unique().shape[0] -1
    cities   = df['City'].unique().shape[0] 
    sports   = df['Sport'].unique().shape[0] 
    events   = df['Event'].unique().shape[0]
    athletes = df['Name'].unique().shape[0]
    nations  = df['region'].unique().shape[0]                                                                                                                                                         
    
    col1, col2, col3 = st.columns(3)
    with col1:
         st.header("Editions")
         st.title(editions)
         
    with col2:
         st.header("Hosts")
         st.title(cities)
         
    with col3:
         st.header("Sports")
         st.title(sports) 
         
    col1, col2, col3 = st.columns(3)
    with col1:
         st.header("Events")
         st.title(events)
         
    with col2:
         st.header("Athletes")
         st.title(athletes)
         
    with col3:
         st.header("Nations")
         st.title(nations)
         
         
    nations_over_time = helper.data_over_time(df,'region')
    fig = px.line(nations_over_time, x="Edition", y='col')
    st.title('Participating Nations Over The Years ')
    
    st.plotly_chart(fig) 
    
    
    events_over_time = helper.data_over_time(df,'Event')
    fig = px.line(events_over_time, x="Edition", y="col")
    st.title('Event Over The Years ')
    
    st.plotly_chart(fig) 
    
    athletes_over_time = helper.data_over_time(df,'Name')
    fig = px.line(athletes_over_time, x="Edition", y="col")
    st.title('Athlete Over The Years ')
    
    st.plotly_chart(fig)   
    
    # Heatmap for Events Over The Time
    st.title("No. Of Events over time(Every Sport)")
    
    fig,ax = plt.subplots(figsize=(20,20)) 
    x = df.drop_duplicates(['Year', 'Event', 'Sport'])
    ax = sns.heatmap(x.pivot_table(index='Sport', columns='Year', values='Event',aggfunc='count')
            .fillna(0).astype('int'),annot=True) 
    
    st.pyplot(fig)                                                   
    
    # Most Successful athletes
    
    st.title("Most Successful Athletes")
    sport_list = df['Sport'].unique().tolist()
    sport_list.sort()
    sport_list.insert(0,'Overall')
    
    selected_sport = st.selectbox("Select a Sport",sport_list)
    result_df = helper.most_successful(df,selected_sport)
    st.table(result_df)
    
    
    
if user_menu == 'Country-wise-Analysis':
    
    st.sidebar.title("Country-Wise Analysis")
    
    country_list = df['region'].dropna().unique().tolist()
    country_list.sort()
    
    selected_country = st.sidebar.selectbox('Select Country',country_list)
    
    country_df = helper.yearwise_medal_tally(df,selected_country)
    fig = px.line(country_df, x="Year", y="Medal")
    st.title(selected_country + ' Medal Tally  Over The Years ')
    
    st.plotly_chart(fig)
    
    # Heatmap of olympics meadls in every sport
    st.title(selected_country + " Excels In The Following Sports")
    
    
    pt = helper.country_event_heatmap(df,selected_country)
    fig, ax = plt.subplots(figsize=(20,20))
    ax = sns.heatmap(pt,annot=True) 
    
    st.pyplot(fig)  
    
    st.title("Top 10 Athletes of Selected Country")
    top10_df = helper.most_successful_countrywise(df,selected_country)
    st.table(top10_df)
    
        