import streamlit as st 
import pandas  as pd 
import numpy as np 
import plotly.express as px  # pip install plotly-express 
from datetime import datetime, timedelta


try: 
    st.set_page_config(
            page_title="Freshers' Analytics",
            page_icon=':bar_chart:',
            layout="wide",
            initial_sidebar_state="expanded"
        )

    # import sidebar
    # sidebar.execute_sidebar()

        #year = st.text_input('Enter current year')
    st.markdown ("# :green[Newly Admitted Students Analytics]")

    
        
    with st.sidebar: 
            
        try:
            st.header(":red[Menu]")
            uploded_data = st.file_uploader("Upload your file", type={"csv", "txt"})
        
            if uploded_data is not None:
                df = pd.read_csv(uploded_data)
                    #st.write(df)
        except:
            st.warning("Use the upload channel in the menu to upload a csv file")
        
        options =  ["Age", "Blood Group","College", "Degree", "Denomination", "Gender","Genotype", "Kin Relationship","Current Level", "Religion"]
        select_options = st.multiselect(
            "Select two items for one or two items to perform analytics",
            options,
            #["Degree", "Gender"],
            max_selections=2 
            ) 
        chart_type = st.selectbox('Choose another chat view program', ['Bar', 'Table']) 


        #sidebar = { "backgroundColor": "#FFFFFF", "contrast": 1.2 }
        df['Degree'] = df['Degree'].str.upper()
        df['Degree'] = df['Degree'].str.replace('\W', '', regex=True) # Removing punctuations
        df['State'] = df['State'].str.upper()
        df['Department'] = df['Department'].str.upper()
        df['Program'] = df["Program"].str.rstrip() #Remove space at the end of a sentence



    left_col, right_col = st.columns(2)
    with left_col:
        rows, columns = df.shape
        total_admitted_students = rows
        st.markdown(f"### Total number of admitted students: :red[{total_admitted_students}]")

        program_size = df.groupby(['Department'])['Department'].count().reset_index(name='count')
        rows, columns = program_size.shape
        total_program = rows
        st.markdown(f"### Total number of Departments with admitted students: :red[  {total_program}]")
        
    with right_col:
        program_size = df.groupby(['State'])['State'].count().reset_index(name='count')
        rows, columns = program_size.shape
        total_state = rows
        st.markdown(f"### Total number of states with admitted students: :red[  {total_state}]")

        program_size = df.groupby(['Program'])['Program'].count().reset_index(name='count')
        rows, columns = program_size.shape
        total_program = rows
        st.markdown(f"### Total number of Programs with admitted students: :red[  {total_program}]")

    st.markdown(" --- ")



    if len(select_options) ==1:
            x1 = select_options[0]
            Title = st.write(f"Distribution of {select_options[0]}")
            stat = df.groupby([x1])[x1].count().reset_index(name='Counts')
            fig = px.pie(stat, values='Counts', names= x1, title=' College Distribution')  
            st.plotly_chart(fig, use_container_width=True)
        

    elif len(select_options) == 2: 
        x1 = select_options[0]
        x2 = select_options[1]
        
        Title = st.write(f"{select_options[0]} Vs {select_options[1]}")
        select_= df.groupby([ x1,x2])[x2].count().reset_index(name='Values')
        fig = px.bar(select_, x= x1, y="Values", color= x2, title= Title)
        st.plotly_chart(fig, use_container_width=True)
    else:
        select_= df.groupby([ 'Degree','Gender'])['Gender'].count().reset_index(name='Values')
        fig = px.bar(select_, x= 'Degree', y="Values", color= 'Gender', title= 'Degree Vs Gender')
        st.plotly_chart(fig, use_container_width=True)
            

    st.markdown("---")

    col1, col2 = st.columns(2)
    with col1:
        df['Department'] = df['Department'].str.upper() # Converting all values to Upper cases 
        stat = df.groupby(['Department'])['Department'].count().reset_index(name='Counts')
        styled_df = stat.style.highlight_max(axis=0, color='yellow')
        st.dataframe(styled_df)
    with col2:
        df['Program'] = df['Program'].str.upper() # Converting all values to Upper cases 
        stat = df.groupby(['Program'])['Program'].count().reset_index(name='Counts')
        styled_df = stat.style.highlight_max(axis=0, color='yellow')
        st.dataframe(styled_df)
        #st.write(stat)


    st.markdown("---")


    df['State'] = df['State'].str.upper() # Converting all values to Upper cases 
    stat = df.groupby(['State'])['State'].count().reset_index(name='Counts')

    if chart_type == 'Bar':
        fig = px.bar(stat, x ='Counts', y ='State', title='State Distribution')   
        st.plotly_chart(fig, use_container_width=True)

    elif chart_type == 'Table':  
        styled_df = stat.style.highlight_max(axis=0, color='yellow')
        st.dataframe(styled_df)

    st.markdown(" --- ") 

    df['dob'] = pd.to_datetime(df['Date of Birth'])  
    now = pd.Timestamp('now') 
    df['Age'] = (((now - df['dob']).dt.days))/365.25
    #age = df['Age']#.astype('<m8[Y]')
    age = df["Age"].astype(float).round().astype(int)

    
    stat1 = df.groupby(['Age'])['Age'].count().reset_index(name='Counts')
    fig = px.bar(stat1, x ='Counts', y ='Age', title='Age Distribution')   
    st.plotly_chart(fig, use_container_width=True)
    #st.write(age)
except:
    st.warning(':red[Upload your data to continue the analytics]', icon="⚠️")
