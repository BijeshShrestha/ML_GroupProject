# --------------------------- INSTRUCTION TO INSTALL LIBRARIES------------------------------------------#








# --------------------------- INSTRUCTION TO RUN THE APPLICATION-----------------------------------------#






# --------------------------- IMPORTS --------------------------------------------------------------------#
from llm_output import handle_input
# from application import *


import streamlit as st 
# from pillow import Image






# -------------------------- SPLASH PAGE------------------------------------------------------------------#

# -------------------------- Page Logo -------------------------------------------------------------------#
st.set_page_config(layout="wide")

st.image('healthy-veg-gard_background.jpg', caption='Veg Garden')

# Sidebar
uploaded_file = st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
    if st.sidebar.button('Submit'):
        
        st.write("test")


