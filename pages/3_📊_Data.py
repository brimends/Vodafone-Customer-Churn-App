import streamlit as st
import pyodbc
import pandas as pd
import requests


st.set_page_config(
    page_title='View Data',
    page_icon= '',
    layout= 'wide'
)

st.title('Proprietory Data From Vodafone')

@st.cache_resource(show_spinner='connecting to Database...')
def first_connection():
    connection= pyodbc.connect(
        "DRIVER={SQL Server};SERVER="
        + st.secrets["SERVER"]
        + ";DATABASE="
        + st.secrets["DATABASE"]
        + ";UID="
        + st.secrets["UID"]
        + ";PWD="
        + st.secrets["PWD"]
    )


    return connection

conn = first_connection()

@st.cache_data()
def query_connection(query):
    with conn.cursor() as cur:
        cur.execute(query)
        rows= cur.fetchall()

        df =  pd.DataFrame. from_records(data=rows, columns=[  column[0] for column in cur.description])

    return df

@st.cache_data()
def select_all_features():
    query = "SELECT * FROM LP2_Telco_churn_first_3000"
    df = query_connection(query)
    return df

def select_all_features():
    query = "SELECT * FROM LP2_Telco_churn_first_3000"
    df = query_connection(query)
    return df


if __name__ == "__main__":

    col1, col2 = st.columns(2)

    with col1:

     st.selectbox("Select the type of features", options= ["All features", "Numeric features","Categorical features"], key= "selected_columns"
                  )
     
     with col2:
        pass
     
    if st.session_state['selected_columns'] == "All features": 
        data= select_all_features()
        st.dataframe(data)

    st.write(st.session_state)