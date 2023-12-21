import streamlit as st
import pandas as pd
import subprocess

def drowsiness():
    subprocess.run(['python', 'drowsiness_yawn.py'])

def lane():
    subprocess.run(['python', 'lane.py'])

def show_data_drowsiness():
    df = pd.read_csv('drowsiness_yawn_log.csv')
    st.table(df)

    # Add a line chart to visualize data
    st.subheader('Drowsiness Chart')
    st.line_chart(df['Event'])  # Replace 'Column_Name' with the actual column you want to visualize

def show_data_lane():
    df = pd.read_csv('lane_change_events.csv')
    st.table(df)

    # Add a bar chart to visualize data
    st.subheader('Lane Chart')
    st.bar_chart(df['direction'])  # Replace 'Column_Name' with the actual column you want to visualize

# Streamlit app layout
st.title('CV Solutions')

# Create two columns for layout
col1, col2 = st.columns(2)

# Buttons in the first column
with col1:
    drowsiness_btn = st.button('Drowsiness', on_click=drowsiness)
    lane_btn = st.button('Lane Detection', on_click=lane)

# Buttons in the second column
with col2:
    show_drowsiness_btn = st.button('Show Data Drowsiness', on_click=show_data_drowsiness)
    show_lane_btn = st.button('Show Data Lane', on_click=show_data_lane)

# This ensures that the data display is shown below the buttons
st.header('Data Display')

# Display the data tables in the main column
with st.expander('Drowsiness Data'):
    show_data_drowsiness()

with st.expander('Lane Data'):
    show_data_lane()
