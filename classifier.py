
import cv2
import numpy as np
import tensorflow as tf


# Path to model
MODEL_PATH = './plant_village_new_model_Inception_multi_tasks.h5'  # update model
IMAGE_SIZE = 256  # Update this if your model uses a different input size


# Directly defining label mappings
plant_labels_sorted = [
    'Apple', 
    'Blueberry', 
    'Cherry', 
    'Corn', 
    'Grape', 
    'Orange', 
    'Peach', 
    'Pepper,_bell', 
    'Potato', 
    'Raspberry', 
    'Soybean', 
    'Squash', 
    'Strawberry', 
    'Tomato']

disease_labels_sorted = [
    'Apple_scab', 
    'Bacterial_spot', 
    'Black_rot', 
    'Cedar_apple_rust', 
    'Cercospora_leaf_spot Gray_leaf_spot', 
    'Common_rust', 
    'Early_blight', 
    'Esca_(Black_Measles)', 
    'Haunglongbing_(Citrus_greening)', 
    'Late_blight', 
    'Leaf_Mold', 
    'Leaf_blight_(Isariopsis_Leaf_Spot)', 
    'Leaf_scorch', 
    'Northern_Leaf_Blight', 
    'Powdery_mildew', 
    'Septoria_leaf_spot', 
    'Spider_mites Two-spotted_spider_mite', 
    'Target_Spot', 
    'Tomato_Yellow_Leaf_Curl_Virus', 
    'Tomato_mosaic_virus',
     'healthy']

# Convert sorted lists to index-based mappings
plant_labels = {i: label for i, label in enumerate(plant_labels_sorted)}
disease_labels = {i: label for i, label in enumerate(disease_labels_sorted)}

# Preprocess the image
def preprocess_image(image_file, fig_size=256):
    # Read the file's bytes
    file_bytes = np.asarray(bytearray(image_file.read()), dtype=np.uint8)
    # Decode the bytes into an image
    img_array = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
    # Resize the image
    img_array_resized = cv2.resize(img_array, (fig_size, fig_size))
    # Add a batch dimension
    img_array_reshaped = np.expand_dims(img_array_resized, axis=0)
    
    return img_array_reshaped


def load_model():
    return tf.keras.models.load_model(MODEL_PATH)

def predict(preprocessed_image):
    # Load the pre-trained model
    model = load_model()
    # Predict using the pre-trained model
    predictions = model.predict(preprocessed_image)
    # Get indices of the highest probability labels
    species_index, disease_index = np.argmax(predictions[0]), np.argmax(predictions[1])
    # Map the indices to actual names using the mappings
    species = plant_labels[species_index]
    disease = disease_labels[disease_index]
    return species, disease


def prediction(image_input):
    # Preprocess your image
    preprocessed_image = preprocess_image(image_input, IMAGE_SIZE)
    # Get predictions
    species, disease = predict(preprocessed_image)
    
    return species, disease

# image_input = './apple2.jpg' 
# species, disease = prediction(image_input)
# print(f"Predicted species: {species}, Predicted disease: {disease}")

