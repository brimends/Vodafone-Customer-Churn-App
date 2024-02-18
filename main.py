


import streamlit as st
st.set_page_config(
    page_title='Home',
    page_icon= '',
    layout= 'wide'
)

st.title('My Customer Churn App')

from PIL import Image
Img = Image.open('voda pix.png')

st.image(
    Img,

    width=700


)








