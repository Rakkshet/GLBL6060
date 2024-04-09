'''
pip install streamlit
pip install pandas
pip install matplotlib
pip install plotly
pip install numpy
pip install pyarrow
'''

# streamlit run /Users/rakkshetsinghaal/Desktop/Yale\ University/GLBL\ 6060/PycharmProjects/Python_Project/streamlit_app.py

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px

# Title of the app
st.title("Earthquake Data Processor")
st.text("This is an app that explores Earthquake data.")

# Sidebar for file upload and navigation
st.sidebar.title("Upload File")
my_file = st.sidebar.file_uploader("Choose a file")

# Navigation
st.sidebar.title("Navigation")
options = st.sidebar.radio("Select the options you would like to see:",
                           ("Home", "Data Header", "Data Summary", "Scatter-Plot", "Box-Plot"))

# Load the file
if my_file:
    df = pd.read_csv(my_file)
    # Save the dataframe in the session state to avoid reloading on each interaction
    st.session_state['df'] = df
elif 'df' in st.session_state:
    # Use the dataframe from the session state if it exists
    df = st.session_state['df']
else:
    df = None

# Navigation options
if options == "Home" and df is not None:
    st.header("Welcome to the Earthquake Data Processor!")
    st.write("Please upload a dataset to get started.")
elif options == "Data Header" and df is not None:
    st.header("Data Header")
    st.write(df.head())
elif options == "Data Summary" and df is not None:
    st.header("Summary Statistics")
    st.write(df.describe())
elif options == "Scatter-Plot" and df is not None:
    st.header("Plot of Data")
    fig, ax = plt.subplots()
    ax.scatter(x=df["Depth"], y=df["Magnitude"])
    ax.set_xlabel("Depth")
    ax.set_ylabel("Magnitude")
    st.pyplot(fig)
elif options == "Box-Plot" and df is not None:
    st.header("Interactive Box Plot")
    fig = px.box(df, x="year", y="Magnitude", title="Earthquake Magnitude by Year")
    st.plotly_chart(fig, use_container_width=True)
else:
    st.write("Please upload data to explore.")