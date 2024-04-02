# --------------------------- INSTRUCTION TO INSTALL LIBRARIES------------------------------------------#








# --------------------------- INSTRUCTION TO RUN THE APPLICATION-----------------------------------------#






# --------------------------- IMPORTS --------------------------------------------------------------------#
import streamlit as st 


from dotenv import load_dotenv
import os
import openai

# ---------------------------  --------------------------------------------------------------------#

def prediction(image_input):
    
    # Placeholder return for now. Replace with aayush's code
    species = "tomato"
    disease = "Leaf fungus"
    
    return species, disease



# Retrieve API keys from environment variables. Keep separate file .env in the same directory as this file and add teh keys there. 
def load_api_key():
    load_dotenv()
    return os.getenv("OPENAI_API_KEY")

def ask_question(api_key, question, instructions):
    # Format the question with instructions.
    formatted_question = f"{instructions}\nQuestion: {question}"
    
    # Use the OpenAI API for Query and Response
    openai.api_key = api_key
    response = openai.Completion.create(
        engine="gpt-3.5-turbo-instruct",  
        prompt=formatted_question,
        temperature=0.5,
        max_tokens=350,  
        top_p=1.0,
        frequency_penalty=0.0,
        presence_penalty=0.0
    )

    # Extracting text response from the OpenAI response object
    answer = response.choices[0].text.strip()
    
    return answer

def handle_input(species, disease):
    instructions = '''You are getting an input that states the plant species and predicted disease for that plant. 
    Based on your general knowledge about the plant and the predicted disease, please write your response in 3 portions:
    1. First paragraph gives a general summary of your findings. It should start with "Thank you for uploading the image, based on the prediction from our model, your plant (insert name based on input) shows (disease based on input)."
    2. Second portion is the suggested home remedies.
    3. Third portion is the suggested pesticide treatment.
    Also, add a disclaimer that you are basing this information on LLM data.
    Write the output as strings that can be passed for output on a UI using Python libraries.'''
    openai_api_key = load_api_key()
    input_text = f"Plant is {species} and the disease is {disease}"
    response = ask_question(openai_api_key, input_text, instructions)
    return response



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


