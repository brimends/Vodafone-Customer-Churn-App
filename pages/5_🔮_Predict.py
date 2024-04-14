import streamlit as st
import joblib
import pandas as pd
import os
import datetime


st.set_page_config(
    page_title='Predict',
    page_icon='',
    layout='wide'
)


@st.cache_resource(show_spinner='Models Loading')
def load_gradient_pipeline():
    pipeline = joblib.load('./models/gradient_pipeline.joblib')
    return pipeline


@st.cache_resource(show_spinner='Models Loading')
def load_naives_pipeline():
    pipeline = joblib.load('./models/Naives_pipeline.joblib')
    return pipeline


def select_model():
    col1, col2 = st.columns(2)

    with col1:
        st.selectbox('Select a Model', options=[
                     'Gradient', 'Naives'], key='selected_model')
    with col2:
        pass

    if st.session_state['selected_model'] == 'gradient':
        pipeline = load_gradient_pipeline()
    else:
        pipeline = load_naives_pipeline()

    encoder = joblib.load('./models/encoder.joblib')

    return pipeline, encoder


if 'prediction' not in st.session_state:
    st.session_state['prediction'] = None

if 'probability' not in st.session_state:
    st.session_state['probability'] = None



def make_prediction(pipeline, encoder):
    gender= st.session_state['gender']
    seniorcitizen = st.session_state['seniorcitizen']
    partner = st.session_state['partner']
    dependents = st.session_state['dependents']
    tenure= st.session_state['tenure']
    phoneservice = st.session_state['phoneservice']
    multiplelines = st.session_state['multiplelines']
    internetservice = st.session_state['internetservice']
    onlinesecurity = st.session_state['onlinesecurity']
    onlinebackup = st.session_state['onlinebackup']
    deviceprotection = st.session_state['deviceprotection']
    techsupport = st.session_state['techsupport']
    streamingtv = st.session_state['streamingtv']
    streamingmovies = st.session_state['streamingmovies']
    contract = st.session_state['contract']
    paperlessbilling = st.session_state['paperlessbilling']
    paymentmethod = st.session_state['paymentmethod']
    monthlycharges = st.session_state['monthlycharges']
    totalcharges = st.session_state['totalcharges']






    columns = ['gender', 'seniorcitizen','partner','dependents','tenure','phoneservice','multiplelines','internetservice','onlinesecurity','onlinebackup','deviceprotection','techsupport','streamingtv','streamingmovies','contract','paperlessbilling','paymentmethod',
             'monthlycharges','totalcharges']

    data= [[ gender,seniorcitizen,partner,dependents,tenure,phoneservice,multiplelines,internetservice,onlinesecurity,onlinebackup,deviceprotection,techsupport,streamingtv,streamingmovies,contract,paperlessbilling,paymentmethod,
             monthlycharges,totalcharges]]

    # create a dataframe
    df = pd.DataFrame(data, columns=columns)

    df['Prediciton Time'] = datetime.date.today()
    df['Model Used'] = st.session_state['selected_model']

    df.to_csv('./data/history.csv', mode='a', header=not os.path.exists('./data/history.csv'), index=False)

    # Make prediction
    pred = pipeline.predict(df)
    pred = int(pred[0])
    prediction = encoder.inverse_transform([pred])

    # Get probabilities
    probability = pipeline.predict_proba(df)

    # Updating state
    st.session_state['prediction'] = prediction
    st.session_state['probability'] = probability

    return prediction, probability




def display_form():

    pipeline, encoder = select_model()

    with st.form('input-feature'):
        col1, col2, col3 = st.columns(3)

        with col1:
            st.write('### Personal Information')
            st.selectbox ('gender',['male', 'female'],key='gender')
            st.selectbox(' seniorcitizen:', ['yes', 'No'],key='seniorcitizen')
            st.selectbox(' partner:', ['yes', 'no'],key='partner')
            st.selectbox(' dependents:', ['yes', 'no'],key='dependents')

        with col2:
            st.write('### Services')
            st.selectbox(' phoneservice:', ['yes', 'no'],key='phoneservice')
            st.selectbox(' multiplelines:', ['yes', 'no', 'no_phone_service'],key='multiplelines')
            st.selectbox(' internetservice:', ['dsl', 'no', 'fiber_optic'],key='internetservice')
            st.selectbox(' onlinesecurity:', ['yes', 'no', 'no_internet_service'],key='onlinesecurity')
            st.selectbox(' onlinebackup:', ['yes', 'no', 'no_internet_service'],key='onlinebackup')
            st.selectbox(' deviceprotection:', ['yes', 'no', 'no_internet_service'],key='deviceprotection')
            st.selectbox(' techsupport:', ['yes', 'no', 'no_internet_service'],key='techsupport')
            st.selectbox(' streamingtv:', ['yes', 'no', 'no_internet_service'],key='streamingtv')
            st.selectbox(' streamingmovies:', ['yes', 'no', 'no_internet_service'],key='streamingmovies')

        
        
        
        
        
        
        with col3:
            st.write('### Contract/Billing')
            st.selectbox(' Customer has a contract:', ['month-to-month', 'one_year', 'two_year'],key='contract')
            st.selectbox(' Customer has a paperlessbilling:', ['yes', 'no'],key='paperlessbilling')
            st.selectbox('Paymentmethod:', ['bank_transfer_(automatic)', 'credit_card_(automatic)', 'electronic_check' ,'mailed_check'],key='paymentmethod')
            st.number_input('tenure  :', min_value=0, max_value=240, value=0,key='tenure')
            st.number_input('monthlycharges :', min_value=0, max_value=240, value=0,key='monthlycharges')
            st.number_input('totalcharges :', min_value=0, max_value=5000, value=0,key='totalcharges')

        st.form_submit_button('Make Prediction', on_click=make_prediction, kwargs=dict(
            pipeline=pipeline, encoder=encoder))


if __name__ == "__main__":
    st.title("Predicting Customer Churn")
    display_form()

    prediction = st.session_state['prediction']
    probability = st.session_state['probability']

    if not prediction:
        st.markdown("### Predictions will show here")
    elif prediction == "Yes":
        probability_of_yes = probability[0][1] * 100
        st.markdown(f"### The employee will leave the company with a probability of {round(probability_of_yes, 2)}%")
    else:
        probability_of_no = probability[0][0] * 100
        st.markdown(f"### Employee will not leave the company with a probability of  {round(probability_of_no, 2)}%")

     
st.write(st.session_state)