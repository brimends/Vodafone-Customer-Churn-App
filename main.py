import streamlit as st

st.set_page_config(page_title="Home", page_icon="", layout="wide")

st.title("My Customer Churn App")

from PIL import Image

Img = Image.open("voda pix.png")

st.image(Img, width=700)

tabl, tab2 = st.columns(2)

with tabl:
    st.subheader("Key Features")
    st.markdown(
        """
                - Data view
                - A prediction page
                - A dashboard for EDA and KPI monitoring
                
                """
    )

with tab2:
    st.subheader("Usage Instructions")
    st.markdown(
        """
                - Supply values for inputs
                - Hit the predict button
                - Your prediction will be displayed after a few minutes!
                
                """
    )
