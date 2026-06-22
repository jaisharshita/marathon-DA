import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

st.title("Ultra Marathon Race Data Analytics Dashboard")
st.markdown("""
This interactive dashboard performs a full Exploratory Data Analysis (EDA) on the Ultra Marathon dataset using **Streamlit** and **Plotly**.
""")

@st.cache_data
def load_and_clean_data():
    df = pd.read_csv("TWO_CENTURIES_OF_UM_RACES.csv")
    df2 = df[
        (df['Event distance/length'].isin(['50km', '50mi'])) & 
        (df['Year of event'] == 2020) & 
        (df['Event name'].str.split('(').str.get(1).str.split(')').str.get(0) == 'USA')
    ].copy()
    
    df2['Event name'] =  df2['Event name'].str.split('(').str.get(0)
    df2['athlete age'] = 2020 - df2['Athlete year of birth']
    df2['Athlete performance']=df2['Athlete performance'].str.split(' ').str.get(0)
    df2 = df2.drop( columns=['Athlete club', 'Athlete country', 'Athlete year of birth', 'Athlete age category'], axis = 1)
    df2 = df2.dropna()
    df2 = df2.drop_duplicates()
    df2 = df2.reset_index(drop=True)
    df2['athlete age'] = df2['athlete age'].astype(int)
    df2['Athlete average speed'] = df2['Athlete average speed'].astype(float)
    
    df2=df2.rename(
        columns={'Year of event':'year','Event dates':'race_day',
                'Event name':'race_name','Event distance/length':'race_length',
                'Event number of finishers':'race_number_of_finishers',
                'Athlete performance':'athlete_performance','Athlete gender':'athlete_gender',
                'Athlete average speed':'athlete_average_speed',
                 'Athlete ID':'athlete_id','athlete age':'athlete_age'})
    
    df2['race_month'] = df2['race_day'].str.split('.').str[1].astype(int)
    season_mapping = {
        12: 'Winter', 1: 'Winter', 2: 'Winter',
        3: 'Spring', 4: 'Spring', 5: 'Spring',
        6: 'Summer', 7: 'Summer', 8: 'Summer',
        9: 'Fall', 10: 'Fall', 11: 'Fall'
    }
    df2['race_season'] = df2['race_month'].map(season_mapping)
    
    df3 = df2[['race_day','race_name','race_length','race_number_of_finishers',
          'athlete_id','athlete_gender','athlete_age','athlete_performance','athlete_average_speed',
               'year','race_season','race_month']]
    
    return df3

df3 = load_and_clean_data()
st.header("Dataset Overview")
st.write("Rows:", df3.shape[0])
st.write("Columns:", df3.shape[1])
st.write("Some of the details from data is shown below:")
st.dataframe(df3.head())

col1, col2 = st.columns(2)
with col1:
    st.subheader("Which race distance is more popular?")
    race_length_count = df3['race_length'].value_counts()
    fig = px.pie(
        values=race_length_count.values,
        names=race_length_count.index,
    )
    st.plotly_chart(fig, use_container_width=True)
with col2:
    st.subheader("Gender Participation Distribution")
    gender_count = df3['athlete_gender'].value_counts()
    fig = px.pie(
        values=gender_count.values,
        names=gender_count.index,
    )
    st.plotly_chart(fig, use_container_width=True)


st.subheader('Male vs Female avg speed comparison')
fig = px.box(
    df3,
    x='athlete_gender',
    y='athlete_average_speed',
    color='athlete_gender',
    title='Average Speed by Gender'
)
st.plotly_chart(fig, use_container_width=True)


st.subheader('50km vs 50mi speed comparison')
st.write('does the distance affect the speed of runners')
fig = px.violin(
    df3,
    x='race_length',
    y='athlete_average_speed',
    color='race_length',
    box=True,
    title='Speed Distribution by Race Length'
)
st.plotly_chart(fig, use_container_width=True)

st.subheader('Top 10 fastest events')
st.write('meaning that what are the events where the avg speed of runners were high')
top_events = (df3.groupby('race_name')['athlete_average_speed'].mean().sort_values(ascending=False).head(10))
fig = px.bar(
    x=top_events.values,
    y=top_events.index,
    orientation='h',
    title='Top 10 Fastest Race Events'
)
st.plotly_chart(fig, use_container_width=True)


st.subheader('Age vs Speed of runners')
st.write('does the age of runners affect their speed')
fig = px.scatter(
    df3,
    x='athlete_age',
    y='athlete_average_speed',
    trendline='ols',
    opacity=0.5,
    title='Age vs Athlete Speed'
)
st.plotly_chart(fig, use_container_width=True)

st.subheader('Best performing Age group')
bins = [18,25,35,45,55,100]
labels = ['18-25','26-35','36-45','46-55','56+']
df3['age_group'] = pd.cut(df3['athlete_age'],bins=bins,labels=labels)
speed_age = (df3.groupby('age_group')['athlete_average_speed'].mean().reset_index())
fig = px.bar(
    speed_age,
    x='age_group',
    y='athlete_average_speed',
    title='Average Speed by Age Group'
)
st.plotly_chart(fig, use_container_width=True)


st.header('Which age group participats the most?')
age_count = (df3['age_group'].value_counts().reset_index())
age_count.columns = ['age_group','count']
fig = px.bar(
    age_count,
    x='age_group',
    y='count',
    title='Participation by Age Group'
)
st.plotly_chart(fig, use_container_width=True)


st.subheader('Which season hosts the most races?')
season_count = (df3['race_season'].value_counts().reset_index())
season_count.columns = ['season','count']
fig = px.bar(
    season_count,
    x='season',
    y='count',
    color='season',
    title='Participation by Season'
)
st.plotly_chart(fig, use_container_width=True)

st.subheader('Does season affect performance?')
season_speed = (df3.groupby('race_season')['athlete_average_speed'].mean().reset_index())
fig = px.line(
    season_speed,
    x='race_season',
    y='athlete_average_speed',
    markers=True,
    title='Average Speed by Season'
)
st.plotly_chart(fig, use_container_width=True)


st.subheader('Which age group dominate each race distance?')
heat = pd.crosstab(df3['age_group'],df3['race_length'])
fig, ax = plt.subplots(figsize=(6, 3))
sns.heatmap(heat, annot=True, cmap='YlOrRd', fmt='d', ax=ax)
ax.set_title('Age Group vs Race Length')
st.pyplot(fig, use_container_width=True)


st.subheader('Which races attract the most runners?')
top_events = (df3.groupby('race_name')['athlete_id'].count().sort_values(ascending=False).head(15))
fig = px.bar(
    x=top_events.values,
    y=top_events.index,
    orientation='h',
    title='Top 15 Events by Participation'
)
st.plotly_chart(fig, use_container_width=True)


st.header('Do larger events produce faster performances?')
event_stats = ( df3.groupby('race_name')
        .agg(participants=('athlete_id','count'),avg_speed=('athlete_average_speed','mean')).reset_index())
fig = px.scatter(
    event_stats,
    x='participants',
    y='avg_speed',
    size='participants',
    hover_name='race_name',
    title='Participation vs Average Speed'
)
st.plotly_chart(fig, use_container_width=True)


st.header('Do Larger Races Attract Slower Runners?')
st.write('(Is there a relationship between event size and average performance?)')
event_stats = (df3.groupby('race_name')
    .agg(participants=('athlete_id','count'),avg_speed=('athlete_average_speed','mean')).reset_index())

fig = px.scatter(
    event_stats,
    x='participants',
    y='avg_speed',
    size='participants',
    hover_name='race_name',
    trendline='ols',
    title='Do Larger Races Attract Slower Runners?'
)
st.plotly_chart(fig, use_container_width=True)



st.header('Are Older Athletes Overrepresented In Longer Races?')
st.write('Do older runners prefer 50mi races over 50km races?')
distance_age = (df3.groupby('race_length')['athlete_age'].mean().reset_index())
fig = px.bar(
    distance_age,
    x='race_length',
    y='athlete_age',
    color='race_length',
    title='Average Athlete Age by Race Distance'
)
st.plotly_chart(fig, use_container_width=True)



st.header('Which Races Appear To Be The Most Difficult?')
st.write('Which races have the lowest average speeds? or Lower average speed often suggests tougher courses.')
hardest_races = (df3.groupby('race_name')['athlete_average_speed'].mean().sort_values().head(15))
fig = px.bar(
    x=hardest_races.values,
    y=hardest_races.index,
    orientation='h',
    title='15 Most Difficult Races (Lowest Average Speed)'
)
st.plotly_chart(fig, use_container_width=True)


st.header('Which Season Produces The Fastest Runners?')
season_gender = (df3.groupby(['race_season','athlete_gender'])['athlete_average_speed'].mean().reset_index())
fig = px.bar(
    season_gender,
    x='race_season',
    y='athlete_average_speed',
    color='athlete_gender',
    barmode='group',
    title='Average Speed by Season and Gender'
)
st.plotly_chart(fig, use_container_width=True)



st.header('Which Race Is The Most Competitive?')
st.write('Logic: \n A race is considered more competitive if runners finish with similar speeds.')
competitive_races = (df3.groupby('race_name')['athlete_average_speed'].std().sort_values().head(15))
fig = px.bar(
    x=competitive_races.values,
    y=competitive_races.index,
    orientation='h',
    title='Top 15 Most Competitive Races',
    labels={
        'x':'Speed Standard Deviation',
        'y':'Race Name'
    }
)
st.plotly_chart(fig, use_container_width=True)


