# --------------------------- INSTRUCTION TO INSTALL LIBRARIES------------------------------------------#








# --------------------------- INSTRUCTION TO RUN THE APPLICATION-----------------------------------------#






# --------------------------- IMPORTS --------------------------------------------------------------------#
from llm_output import handle_input
from application import prediction
import streamlit as st 



# -------------------------- SPLASH PAGE------------------------------------------------------------------#

# -------------------------- Page Logo -------------------------------------------------------------------#
st.set_page_config(layout="wide")
st.image('healthy-veg-gard_background.jpg', caption='Veg Garden')

# Sidebar
image_input = st.sidebar.file_uploader("Choose a image file")
if image_input is not None:
    if st.sidebar.button('Submit'):
        #Pass the image file to application.py and save the return as 
        
        #Get prediction
        species, disease = prediction(image_input)
        # Get explanation from LLM
        answer = handle_input(species, disease)


        


        st.write(answer)


