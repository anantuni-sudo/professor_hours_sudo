import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns



st.set_page_config(page_title=None, page_icon=None, layout="centered", initial_sidebar_state="expanded", menu_items=None)

df = pd.read_excel("data.xlsx")


# Streamlit interface
st.header('Anant National University')
# st.set_page_config(page_title='Professor and Course Analysis', layout='wide', initial_sidebar_state='expanded')

# Sidebar for selections
st.sidebar.header('Filter Options')


course_type = st.sidebar.selectbox('Select Course Type:', df['course_type'].unique())
prof_types = df['prof_type'].unique().tolist()
prof_types.append('All')  # Adding 'All' option
prof_type = st.sidebar.selectbox('Select Professor Type:', prof_types)

# Filter data based on selected course_type and prof_type
if prof_type == 'All':
    filtered_df = df[df['course_type'] == course_type]
else:
    filtered_df = df[(df['course_type'] == course_type) & (df['prof_type'] == prof_type)]

# Dropdown for professors based on selected prof_type
if prof_type == 'All':
    professors = filtered_df['name_prof'].unique()
else:
    professors = filtered_df['name_prof'].unique().tolist()
selected_prof = st.sidebar.selectbox('Select Professor:', professors)

# Filter data for the selected professor
prof_df = filtered_df[filtered_df['name_prof'] == selected_prof]

if st.sidebar.button('Show Sorted Dataset'):
    df_sorted = df.sort_values(by='total_hrs_per_week', ascending=False)
    st.subheader('Sorted Dataset')
    st.write(df_sorted)
    # Clear plots by setting them to None
    fig, ax = None, None
    fig2, ax2 = None, None

show_dataset = False

# Button to display sorted dataset
if st.sidebar.button('Toggle Sorted Dataset'):
    show_dataset = not show_dataset  # Toggle flag

# Layout for displaying graphs and information
col1, col2 = st.columns(2)

# Plot total hours per week for each course
with col1:
    st.subheader('Total Hours per Week for Each Course')
    fig, ax = plt.subplots(figsize=(5, 4))  # Adjust figsize as per your preference
    sns.barplot(x='course', y='total_hrs_per_week', data=prof_df, ax=ax, palette='viridis')
    ax.set_xlabel('Course')
    ax.set_ylabel('Total Hours per Week')
    st.pyplot(fig)

# Plot number of weeks per semester for each course
with col2:
    st.subheader('Number of Weeks per Semester for Each Course')
    fig2, ax2 = plt.subplots(figsize=(5, 4))  # Adjust figsize as per your preference
    sns.barplot(x='course', y='no_of_weeks_per_sem', data=prof_df, ax=ax2, palette='viridis')
    ax2.set_xlabel('Course')
    ax2.set_ylabel('Number of Weeks per Semester')
    st.pyplot(fig2)


# Display professor information in a table
st.subheader('Professor Information')

if not prof_df.empty:
    # st.write(f"Name of Professor: **{selected_prof}**")
    st.write(f"Name of Professor: **{selected_prof}**")
    st.write(f"Professor Type: **{prof_df['prof_type'].iloc[0]}**")
    info_table = prof_df[[ 'course_type', 'total_hrs_per_week', 'no_of_weeks_per_sem']].drop_duplicates()
    st.table(info_table)
else:
    st.write("No professor selected.")