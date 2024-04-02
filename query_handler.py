from PIL import Image
import streamlit as st
import requests

def send_image_to_flask(file):
    # url = 'http://localhost:5000/predict'  #Flask app's URL.
    url = ' https://cf77-108-20-133-165.ngrok-free.app'  #Flask app's URL.

    files = {'file': (file.name, file, 'multipart/form-data')}
    response = requests.post(url, files=files)
    if response.status_code == 200:
        return response.json()
    else:
        return {'error': 'Failed to get prediction from the server', 'status_code': response.status_code}

st.title("Image Upload for Prediction")

uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])
if uploaded_file is not None:
    # Display the uploaded image
    try:
        image = Image.open(uploaded_file)
        st.image(image, caption='Uploaded Image.', use_column_width=True)
    except IOError:
        st.error("Failed to read the image file. Please make sure it is an image.")
    
    if st.button('Predict'):
        result = send_image_to_flask(uploaded_file)
        if 'error' not in result:
            st.write(result)
        else:
            st.error(result.get('error'))
