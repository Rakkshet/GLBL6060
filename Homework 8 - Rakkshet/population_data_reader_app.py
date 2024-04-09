'''
pip install streamlit
pip install pandas
pip install matplotlib
pip install plotly
pip install numpy
pip install pyarrow
'''

# streamlit run /Users/rakkshetsinghaal/Desktop/Yale\ University/GLBL\ 6060/GLBL6060/Homework\ 8\ -\ Rakkshet/population_data_reader_app.py

import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

# Title of the app
st.title("US Population Data Visualizer")
st.text("This app explores population data across US states from 2010 to 2019.")

# Sidebar for file upload and navigation
st.sidebar.title("Upload File")
# Allowing users to upload their data or use the provided dataset
my_file = st.sidebar.file_uploader("Choose a file")

# Navigation
st.sidebar.title("Navigation")
options = st.sidebar.radio("Select the options you would like to see:",
                           ("Home", "Data Header", "Data Summary", "Population Trend",
                            "Population Change", "Population Heatmap", "State Population Distribution"))

# Load the default data or uploaded file
if my_file:
    df = pd.read_csv(my_file)
else:
    df = None

# Save the dataframe in the session state to avoid reloading on each interaction
st.session_state['df'] = df

# Navigation options
if options == "Home":
    st.header("Welcome to the US Population Data Visualizer!")
    st.write("Explore population data across US states from 2010 to 2019.")
elif options == "Data Header":
    st.header("Data Header")
    st.write(df.head())
elif options == "Data Summary":
    st.header("Summary Statistics")
    st.write(df.describe())
elif options == "Population Trend":
    st.header("Population Trend Over Time")
    selected_state = st.selectbox("Select a state to view", df['states'].unique())
    state_data = df[df['states'] == selected_state]
    fig = px.line(state_data, x='year', y='population', title=f'Population Trend for {selected_state}')
    st.plotly_chart(fig, use_container_width=True)
elif options == "Population Change":
    st.header("Population Change by State for a Selected Year")
    year = st.select_slider("Select a year", options=df['year'].unique(), value=df['year'].max())
    year_data = df[df['year'] == year]
    year_data['population_change'] = year_data['population'].diff().fillna(0)
    fig = px.bar(year_data, x='states', y='population_change', title=f'Population Change by State in {year}')
    st.plotly_chart(fig, use_container_width=True)
elif options == "Population Heatmap":
    st.header("Population Heatmap by State and Year")
    fig = go.Figure()
    steps = []
    for year in df['year'].unique():
        year_data = df[df['year'] == year]
        fig.add_trace(
            go.Choropleth(
                locations=year_data['states_code'],  # This assumes you're using state abbreviations
                z=year_data['population'].astype(float),  # Data to be color-coded
                locationmode='USA-states',  # Set to use USA state geographies
                colorscale='Viridis',
                colorbar_title="Population",
            )
        )
        steps.append({
            'method': 'update',
            'args': [{'visible': [False] * len(df['year'].unique())},
                     {'title': f"Population Heatmap by State and Year: {year}"}],  # layout attribute
            'label': str(year),
        })
        fig.data[-1].visible = False
    if fig.data:
        fig.data[0].visible = True
    sliders = [{
        'active': 0,
        'currentvalue': {"prefix": "Year: "},
        'pad': {"t": 50},
        'steps': steps
    }]
    fig.update_layout(
        sliders=sliders,
        geo=dict(scope='usa', projection=go.layout.geo.Projection(type='albers usa')),
        title="Population Heatmap by State and Year",
    )
    st.plotly_chart(fig, use_container_width=True)
elif options == "State Population Distribution":
    st.header("State Population Distribution for a Selected Year")
    year = st.select_slider("Select another year", options=df['year'].unique(), value=df['year'].max())
    year_data = df[df['year'] == year]
    fig = px.pie(year_data, names='states', values='population', title=f'State Population Distribution in {year}')
    st.plotly_chart(fig, use_container_width=True)
else:
    st.write("Please select an option to explore.")
