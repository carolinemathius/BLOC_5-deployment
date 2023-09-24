# Import necessary libraries
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import os

# Get the port from the environment variable or use a default (e.g., 8080)
port = int(os.environ.get('PORT', 8080))

# Load the data from the provided S3 bucket URL
data_url = "https://full-stack-assets.s3.eu-west-3.amazonaws.com/Deployment/get_around_delay_analysis.xlsx"
delay_data = pd.read_excel(data_url)

# Perform data cleaning
delay_data['rental_id'] = delay_data['rental_id'].astype(str)
delay_data['car_id'] = delay_data['car_id'].astype(str)
delay_data['previous_ended_rental_id'] = delay_data['previous_ended_rental_id'].apply(
    lambda x: str(int(x)) if not pd.isna(x) else x
)
conditions = [
    (delay_data['delay_at_checkout_in_minutes'] <= 0),
    (delay_data['delay_at_checkout_in_minutes'] < 60),
    (delay_data['delay_at_checkout_in_minutes'] < 120),
    (delay_data['delay_at_checkout_in_minutes'] < 300),
    (delay_data['delay_at_checkout_in_minutes'] < 1440),
    (delay_data['delay_at_checkout_in_minutes'] >= 1440),
    (delay_data['delay_at_checkout_in_minutes'].isna())
]

labels = ['Early or On Time', '< 1 Hour', '1 to 2 Hours', '2 to 5 Hours', '5 to 24 Hours', '1 day or more', 'Unknown']
delay_data['delay'] = np.select(conditions, labels)

# STREAMLIT PAGE

st.set_page_config(
    page_title="Delay Analysis",
    page_icon="📊",
    layout="wide"
  )
st.title("Getaround: Delay Analysis Dashboard 📊")

st.write("Welcome to this dashboard ! Our goal is to help you to make strategic decisions about how to deal with late returns.")

# SECTION 1: Data Exploration
st.header("Data Exploration")
st.subheader("Data Sample")
st.dataframe(delay_data.head())

# First Graph: Data Visualization - Check-in Type
st.subheader("Check-in Type Visualization")

    # Create a bar chart to visualize check-in type
checkin_type_counts = delay_data['checkin_type'].value_counts()
checkin_type_percentage = (checkin_type_counts / checkin_type_counts.sum()) * 100

fig1 = px.bar(
    x=checkin_type_counts.index,
    y=checkin_type_counts.values,
    title='Distribution of Checkin Types',
    labels={'x': 'Checkin Type', 'y': 'Count'}
)
fig1.update_traces(marker_color='skyblue')
    # Add tags with percentages
percentage_text = [f'{p:.2f}%' for p in checkin_type_percentage]
fig1.update_traces(marker_color='skyblue', text=percentage_text, textposition='outside')

#fig1.update_yaxes(title='Count')
st.plotly_chart(fig1)

# SECTION 2: Delay Analysis
st.header("Delay Analysis")

# Sub-section 1 : How often are drivers late for the next check-in?
st.subheader("How often are drivers late for the next check-in?")

# Build summary table
    # Calculate the number of total entries, late returns, on-time returns, and NaN
total_entries = len(delay_data)
late_returns_count = len(delay_data[delay_data['delay_at_checkout_in_minutes'] > 0])
nan_count = delay_data['delay_at_checkout_in_minutes'].isna().sum()
on_time_or_earlier_count = len(delay_data[delay_data['delay_at_checkout_in_minutes'] <= 0])

    # Calculate percentage for each category
late_return_percentage = (late_returns_count / total_entries) * 100
on_time_percentage = (on_time_or_earlier_count / total_entries) * 100
NaN_percentage = (nan_count / total_entries) * 100

    # Display the results
    # Create a formatted string with line breaks
formatted_text = (
    f"""Total Number of Entries: {total_entries}  
    Number of Late Returns: {late_returns_count}  
    Number of On Time or Earlier Returns: {on_time_or_earlier_count}  
    Number of NaN Values: {nan_count}  
    Percentage of Late Returns: {late_return_percentage:.2f}%  
    Percentage of On Time/Early Returns: {on_time_percentage:.2f}%  
    Percentage of NaN: {NaN_percentage:.2f}%"""
)

    # Use st.write to display the formatted text
st.write(formatted_text)


# Histogram of delay distribution
    # Calculate the counts and percentages of each delay category
delay_counts = delay_data['delay'].value_counts()
delay_percentages = (delay_counts / delay_counts.sum()) * 100

    # Create a histogram manually
fig2 = go.Figure(data=[
    go.Bar(
        x=delay_counts.index,
        y=delay_counts,
        text=delay_percentages.round(2).astype(str) + '%',  # Add percentage to the text
        textposition='outside',  # Show text outside the bars
        marker=dict(color='lightblue'),  # Customize bar color
    )
])

    # Customize the layout
fig2.update_layout(
    title='Distribution of Delays with Percentage Tags',
    xaxis=dict(title='Delay'),
    yaxis=dict(title='Count'),
    showlegend=False,
)
    # Show the chart on streamlit
st.plotly_chart(fig2)

# Sub-section 2 : How does it impact the next driver ?
st.subheader("How does it impact the next driver ?")

# Calculate the frequency of late check-ins
late_checkins = delay_data[delay_data['delay_at_checkout_in_minutes'] > 0]
late_checkin_frequency = (len(late_checkins) / len(delay_data)) * 100
st.write("<u>Frequency of late check-ins</u>",unsafe_allow_html=True)
st.write("Percentage of late check-ins:", f"{late_checkin_frequency:.2f}%")

# Analyze the impact on the next driver
average_delay = late_checkins['time_delta_with_previous_rental_in_minutes'].mean()
max_delay = late_checkins['time_delta_with_previous_rental_in_minutes'].max()
min_delay = late_checkins['time_delta_with_previous_rental_in_minutes'].min()

st.write("<u>Impact on the next driver </u>",unsafe_allow_html=True)
st.write(f"""Average delay in minutes for the next driver: {average_delay:.2f} minutes  
        Maximum delay in minutes for the next driver: {max_delay} minutes  
        Minimum delay in minutes for the next driver: {min_delay} minutes""")

# Create a new DataFrame 'test_df' by merging on 'previous_ended_rental_id'
merge_id_df = delay_data.merge(
    delay_data[['rental_id']],
    left_on='previous_ended_rental_id',
    right_on='rental_id',
    how='inner'
)

# Calculate the new column 'delta_previous_and_delay'
merge_id_df['delta_previous_and_delay'] = merge_id_df['time_delta_with_previous_rental_in_minutes'] - merge_id_df['delay_at_checkout_in_minutes']

# Select rows where 'delta_previous_and_delay' values are strictly negative
negative_delta_rows = merge_id_df[merge_id_df['delta_previous_and_delay'] < 0]

# Calculate the percentage of problematic delays among all the delays
nb_late_checkins = len(late_checkins)
nb_problematic_delays = negative_delta_rows.shape[0]
problematic_delays_rate = nb_problematic_delays * 100 / nb_late_checkins

st.write(f"Among all the delays, **{round(problematic_delays_rate, 2)}%** of delays caused problems to the next rental because the checkout was made later than the new rental check-in.")

# Create a histogram for problematic delays
st.subheader("Distribution of Problematic Delays by Delay Duration")
fig3 = px.histogram(data_frame=negative_delta_rows, x='delay_at_checkout_in_minutes',
                   title='Distribution of Problematic Delays by Delay Duration')
st.plotly_chart(fig3)

# Create a time-based histogram for check-in times
st.subheader("Distribution of Check-in Types by Delay Category")
fig4 = px.histogram(data_frame=negative_delta_rows, x='checkin_type', color='delay',
                   title='Distribution of Check-in Types by Delay Category')
st.plotly_chart(fig4)
st.write("The worst delays concern the rentals made through the **web application**.")

# Sub-section 3 : Threshold - How long should the minimum delay be?
st.subheader("Threshold - How long should the minimum delay be?")

# Define different delay thresholds (in minutes)
thresholds = [60, 90, 120, 150, 180, 210, 240, 300, 360, 420, 480, 600, 720, 1440]  # Define different delay thresholds (in minutes)
problematic_rates = []

for threshold in thresholds:
    # Filter data for delays exceeding the threshold
    delayed_rentals = delay_data[delay_data['delay_at_checkout_in_minutes'] > threshold]

    # Calculate the percentage of problematic delays for each threshold
    problematic_rate = (len(delayed_rentals) / len(delay_data)) * 100
    problematic_rates.append(problematic_rate)

# Create a line plot to visualize the impact of different thresholds
fig5 = px.line(x=thresholds, y=problematic_rates, markers=True, title='Impact of Delay Threshold on Problematic Delays')
fig5.update_layout(xaxis_title='Delay Threshold (minutes)', yaxis_title='Percentage of Problematic Delays')
st.plotly_chart(fig5)

st.write("According to this graph, the threshold should be set at **300 minutes** (5 hours) so that we hope to get less than **5%** of problematic delays.")

# Filter data for 'mobile' check-ins
mobile_checkins = delay_data[delay_data['checkin_type'] == 'mobile']

# Define different delay thresholds (in minutes)
thresholds = [60, 90, 120, 150, 180, 210, 240, 300, 360, 420, 480, 600, 720, 800, 900, 950, 1000, 1200, 1440]

# Initialize a list to store problematic rates for 'mobile' check-ins
mobile_problematic_rates = []

for threshold in thresholds:
    # Filter 'mobile' check-ins for delays exceeding the threshold
    delayed_mobile_checkins = mobile_checkins[mobile_checkins['delay_at_checkout_in_minutes'] > threshold]

    # Calculate the percentage of problematic delays for each threshold and 'mobile' check-ins
    mobile_problematic_rate = (len(delayed_mobile_checkins) / len(mobile_checkins)) * 100
    mobile_problematic_rates.append(mobile_problematic_rate)

# Create a line plot to visualize the impact of different thresholds for 'mobile' check-ins
fig6 = px.line(x=thresholds, y=mobile_problematic_rates, markers=True, title='Impact of Delay Threshold on Problematic Delays for Mobile Check-ins')
fig6.update_layout(xaxis_title='Delay Threshold (minutes)', yaxis_title='Percentage of Problematic Delays')
st.plotly_chart(fig6)

st.write("For *mobile check-in*, the most adapted threshold to get *less than 2% problematic delays* seems to be **950 minutes** (more than 15 hours).")
st.write("If we aim to get less than *5% problematic delays*, then the best threshold seems to be **360 minutes** (6 hours).")

# Filter data for 'connect' check-ins
connect_checkins = delay_data[delay_data['checkin_type'] == 'connect']

# Define different delay thresholds (in minutes)
thresholds = [60, 90, 120, 130, 140, 150, 180, 210, 240, 300, 360]

# Initialize a list to store problematic rates for 'connect' check-ins
connect_problematic_rates = []

for threshold in thresholds:
    # Filter 'connect' check-ins for delays exceeding the threshold
    delayed_connect_checkins = connect_checkins[connect_checkins['delay_at_checkout_in_minutes'] > threshold]

    # Calculate the percentage of problematic delays for each threshold and 'connect' check-ins
    connect_problematic_rate = (len(delayed_connect_checkins) / len(connect_checkins)) * 100
    connect_problematic_rates.append(connect_problematic_rate)

# Create a line plot to visualize the impact of different thresholds for 'connect' check-ins
fig7 = px.line(x=thresholds, y=connect_problematic_rates, markers=True, title='Impact of Delay Threshold on Problematic Delays for Connect Check-ins')
fig7.update_layout(xaxis_title='Delay Threshold (minutes)', yaxis_title='Percentage of Problematic Delays')
st.plotly_chart(fig7)

st.write("On the other hand, for *connect check-in*, the best threshold to get *less than 2% of problematic delays* seems to be **250 minutes** (a bit more than 4 hours), so much less than the mobile check-ins. If we aim to get less than *5% problematic delays*, the threshold should be set at **150 minutes** (2,5 hours).")

st.write("In conclusion, a different ***threshold should definitely be set according to the check-in type***.")
st.write("If we want to *minimize the risk of problematic delays to 2%*, we should choose : **950 minutes** for mobile check-ins and **250 minutes** for connect check-ins. The problem is that this way, we limit the number of times the car can be rented per day, so ***we decrease the owner's revenue***.")
st.write("If we prefer to *higher the risk to 5%* in order to allow the owners to rent their car several times a day, then we should set **360 minutes** for mobile check-in and **150 minutes** for connect check-ins.")

# Sub-section 4 : How many problematic cases will it solve depending on the chosen threshold and scope?
st.subheader("How many problematic cases will it solve depending on the chosen threshold and scope?")

# Define the chosen threshold for mobile and connect check-ins with 5% risk
threshold_mobile_5 = 360  # Minutes for mobile check-ins
threshold_connect_5 = 150  # Minutes for connect check-ins

# Filter data for 'mobile' check-ins with delays below or equal to the threshold
solved_mobile_checkins_5 = negative_delta_rows[
    (negative_delta_rows['checkin_type'] == 'mobile') &
    (negative_delta_rows['delay_at_checkout_in_minutes'] <= threshold_mobile_5)]

# Filter data for 'connect' check-ins with delays below or equal to the threshold
solved_connect_checkins_5 = negative_delta_rows[
    (negative_delta_rows['checkin_type'] == 'connect') &
    (negative_delta_rows['delay_at_checkout_in_minutes'] <= threshold_connect_5)]

# Calculate the number of problematic delays solved for each check-ins
solved_mobile_problems_5 = len(solved_mobile_checkins_5)
solved_connect_problems_5 = len(solved_connect_checkins_5)

# Calculate the percentage of problematic delays solved for each check-in type
total_mobile_problems_5 = len(negative_delta_rows[negative_delta_rows['checkin_type'] == 'mobile'])
total_connect_problems_5 = len(negative_delta_rows[negative_delta_rows['checkin_type'] == 'connect'])

percentage_solved_mobile_5 = (solved_mobile_problems_5 / total_mobile_problems_5) * 100
percentage_solved_connect_5 = (solved_connect_problems_5 / total_connect_problems_5) * 100

st.write("<u>Chosen Thresholds for 5% Risk:</u>",unsafe_allow_html=True)
st.write(f"""Threshold for Mobile Check-ins: {threshold_mobile_5} minutes  
        Threshold for Connect Check-ins: {threshold_connect_5} minutes""")

st.write("<u>Results for 5% Risk:</u>",unsafe_allow_html=True)
st.write(f"""Number of problematic delays solved for mobile check-ins: {solved_mobile_problems_5}  
         Number of problematic delays solved for connect check-ins: {solved_connect_problems_5}""")

st.write(f"""Percentage of problematic delays solved for mobile check-ins: {round(percentage_solved_mobile_5, 2)}%  
         Percentage of problematic delays solved for connect check-ins: {round(percentage_solved_connect_5, 2)}%""")

# Define the chosen threshold for mobile and connect check-ins with 2% risk
threshold_mobile_2 = 950  # Minutes for mobile check-ins
threshold_connect_2 = 250  # Minutes for connect check-ins

# Filter data for 'mobile' check-ins with delays below or equal to the threshold
solved_mobile_checkins_2 = negative_delta_rows[
    (negative_delta_rows['checkin_type'] == 'mobile') &
    (negative_delta_rows['delay_at_checkout_in_minutes'] <= threshold_mobile_2)]

# Filter data for 'connect' check-ins with delays below or equal to the threshold
solved_connect_checkins_2 = negative_delta_rows[
    (negative_delta_rows['checkin_type'] == 'connect') &
    (negative_delta_rows['delay_at_checkout_in_minutes'] <= threshold_connect_2)]

# Calculate the number of problematic delays solved for each check-ins
solved_mobile_problems_2 = len(solved_mobile_checkins_2)
solved_connect_problems_2 = len(solved_connect_checkins_2)

# Calculate the percentage of problematic delays solved for each check-in type
total_mobile_problems_2 = len(negative_delta_rows[negative_delta_rows['checkin_type'] == 'mobile'])
total_connect_problems_2 = len(negative_delta_rows[negative_delta_rows['checkin_type'] == 'connect'])

percentage_solved_mobile_2 = (solved_mobile_problems_2 / total_mobile_problems_2) * 100
percentage_solved_connect_2 = (solved_connect_problems_2 / total_connect_problems_2) * 100

st.write("<u>Chosen Thresholds for 2% Risk:</u>",unsafe_allow_html=True)
st.write(f"""Threshold for Mobile Check-ins: {threshold_mobile_2} minutes  
         Threshold for Connect Check-ins: {threshold_connect_2} minutes""")

st.write("<u>Results for 2% Risk:</u>",unsafe_allow_html=True)
st.write(f"""Number of problematic delays solved for mobile check-ins: {solved_mobile_problems_2}  
         Number of problematic delays solved for connect check-ins: {solved_connect_problems_2}""")

st.write(f"""Percentage of problematic delays solved for mobile check-ins: {round(percentage_solved_mobile_2, 2)}%  
         Percentage of problematic delays solved for connect check-ins: {round(percentage_solved_connect_2, 2)}%""")

st.write("**<u>Conclusion</u>**",unsafe_allow_html=True)
st.write("Results are better with thresholds set to minimize problematic delay risks to **2%**, but I think the loss of income for owners ***is worth a higher risk*** of problematic delays.")

# Sidebar
st.sidebar.header("Getaround dashboard")
st.sidebar.markdown("""
    * [Jump to Data Exploration](#data-exploration)
    * [Jump to Delay Analysis](#delay-analysis)

""")
e = st.sidebar.empty()
e.write("")
st.sidebar.write("Made with 💖 by [Caroline Mathius](https://github.com/carolinemathius)")