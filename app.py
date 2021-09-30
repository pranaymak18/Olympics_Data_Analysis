import streamlit as st
import pandas as pd
import preprocessor
import helper
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns

dff = pd.read_csv('athlete_events.csv')
region_df = pd.read_csv('noc_regions.csv')


df = preprocessor.preprocess(dff,region_df)

st.sidebar.title("Olympics Analysis")
user_menu = st.sidebar.radio(
    'Select an Option',
    ('Medal Tally','Overall Analysis','Country Wise Analysis','Athlete Wise Analysis')
)

if user_menu == 'Medal Tally':
    st.sidebar.header("Medal Tally")

    years,country = helper.county_year_list(df)
    selected_year = st.sidebar.selectbox("Select Year",years)
    selected_country = st.sidebar.selectbox("Select Country", country)
    if selected_year == "Overall" and selected_country == "Overall":
        st.title("Overall Tally")
    if selected_year == "Overall" and selected_country != "Overall":
        st.title("Overall Performance of "+ str(selected_country))
    if selected_year != "Overall" and selected_country == "Overall":
        st.title("Medal Tally in " + str(selected_year)+ " Olympics")
    if selected_year != "Overall" and selected_country != "Overall":
        st.title(str(selected_country) + "'s Performance in " + str(selected_year)+ " Olympics")

    medal_tally = helper.fetch_medal_tally(df,selected_year,selected_country)
    st.table(medal_tally)

if user_menu == 'Overall Analysis':

    st.title("Top Statistics")
    edition = df['Year'].unique().shape[0] - 1
    cities = df['City'].unique().shape[0]
    sports = df['Sport'].unique().shape[0]
    events = df['Event'].unique().shape[0]
    athletes = df['Name'].unique().shape[0]
    nation = df['region'].unique().shape[0]

    col1,col2,col3 = st.columns(3)
    with col1:
        st.header("Editions")
        st.title(edition)
    with col2:
        st.header("Hosts")
        st.title(cities)
    with col3:
        st.header("Sports")
        st.title(sports)

    col1,col2,col3 = st.columns(3)
    with col1:
        st.header("Event")
        st.title(events)
    with col2:
        st.header("Nations")
        st.title(nation)
    with col3:
        st.header("Athletes")
        st.title(athletes)
    nations_over_time = helper.data_over_time(df,'region')
    fig = px.line(nations_over_time, x="Edition", y="region")
    st.title("Participating Nations Over the Years")
    st.plotly_chart(fig)

    event_over_time = helper.data_over_time(df,'Event')
    fig = px.line(event_over_time, x="Edition", y="Event")
    st.title("Events Over the Years")
    st.plotly_chart(fig)

    athlete_over_time = helper.data_over_time(df, 'Name')
    fig = px.line(athlete_over_time, x="Edition", y="Name")
    st.title("Athletes Over the Years")
    st.plotly_chart(fig)

    st.title("No. Of Event Over the Time")
    fig,ax = plt.subplots(figsize=(20,20))
    x = df.drop_duplicates(['Year', 'Sport', 'Event'])
    ax = sns.heatmap(x.pivot_table(index='Sport', columns='Year', values='Event', aggfunc='count').fillna(0).astype(int), annot=True)
    st.pyplot(fig)

    st.title('Most Successful Athletes')
    sport_list = df['Sport'].unique().tolist()
    sport_list.sort()
    sport_list.insert(0,'Overall')

    selected_sport = st.selectbox('Select Sport',sport_list)
    x = helper.most_succesful(df,selected_sport)
    st.table(x)

if user_menu == 'Country Wise Analysis':

    st.title('Country-Wise Analysis')
    country_list = df['region'].dropna().unique().tolist()
    country_list.sort()

    # selected_country = st.selectbox('Select Country', country_list)
    selected_country = st.sidebar.selectbox("Select Country", country_list)

    country_df = helper.yearwise_medal_tally(df, selected_country)
    fig = px.line(country_df, x="Year", y="Medal")
    st.title(selected_country + " Medal Tally Over The Year")
    st.plotly_chart(fig)

    st.title(selected_country + "Excels in the Following Sports")
    pt =helper.country_event_heatmap(df,selected_country)
    fig, ax = plt.subplots(figsize=(20, 20))
    ax = sns.heatmap(pt,annot=True)
    st.pyplot(fig)

    st.title("Top 10 Athletes of " + selected_country)
    top10_df = helper.most_succesful_countryWise(df,selected_country)
    st.table(top10_df)

if user_menu == 'Athlete Wise Analysis':
    st.table(df)

