# import streamlit as st
#
# st.set_page_config(page_title="Merged Streamlit App", layout="wide")
#
# st.title("Welcome to the Merged Streamlit App")
#
# st.write("Use the sidebar to navigate between different applications.")
#
# # Import functions from both Streamlit apps if they're modular
# from app1 import app as app1_function
# from app2 import app as app2_function
#
# st.sidebar.title("Navigation")
# page = st.sidebar.radio("Go to", ["App 1", "App 2"])
#
# if page == "App 1":
#     app1_function()
# elif page == "App 2":
#     app2_function()

import streamlit as st
import os
from PIL import Image
import numpy as np
import pickle
import tensorflow
from tensorflow import keras
from tensorflow.keras.preprocessing import image
from tensorflow.keras.layers import GlobalMaxPooling2D
from tensorflow.keras.applications.resnet50 import ResNet50, preprocess_input
from sklearn.neighbors import NearestNeighbors
from numpy.linalg import norm
import google.generativeai as genai

# Configure Google Gemini API
genai.configure(api_key="AIzaSyAIbaU3vaR2mDaO2we4p7qjbKoDaRlwTg8")

generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 40,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

model_gemini = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config=generation_config,
)

# Load precomputed features
feature_list = np.array(pickle.load(open('embeddings.pkl', 'rb')))
filenames = pickle.load(open('filenames.pkl', 'rb'))

# Load ResNet50 Model
model = ResNet50(weights='imagenet', include_top=False, input_shape=(224, 224, 3))
model.trainable = False
model = tensorflow.keras.Sequential([
    model,
    GlobalMaxPooling2D()
])

# Streamlit UI
st.set_page_config(page_title="Fashion Recommender & Stylist", page_icon="👗", layout="wide")

st.markdown("""
    <div style='text-align: center;'>
        <h1 style='color: #ff4081;'>👗 AI-Powered Fashion Stylist & Recommender 👗</h1>
    </div>
""", unsafe_allow_html=True)

st.sidebar.header("User Preferences")
occasion = st.sidebar.selectbox("Select Occasion", ["Casual", "Formal", "Party", "Workout", "Business Casual"])
color_preference = st.sidebar.color_picker("Pick Your Preferred Color")
style_preference = st.sidebar.selectbox("Choose Your Style", ["Modern", "Vintage", "Streetwear", "Boho", "Minimalist"])

# Upload Image
uploaded_file = st.file_uploader("Choose an image")

def save_uploaded_file(uploaded_file):
    try:
        with open(os.path.join('uploads', uploaded_file.name), 'wb') as f:
            f.write(uploaded_file.getbuffer())
        return 1
    except:
        return 0

def feature_extraction(img_path, model):
    img = image.load_img(img_path, target_size=(224, 224))
    img_array = image.img_to_array(img)
    expanded_img_array = np.expand_dims(img_array, axis=0)
    preprocessed_img = preprocess_input(expanded_img_array)
    result = model.predict(preprocessed_img).flatten()
    normalized_result = result / norm(result)
    return normalized_result

def recommend(features, feature_list):
    neighbors = NearestNeighbors(n_neighbors=5, algorithm='brute', metric='euclidean')
    neighbors.fit(feature_list)
    distances, indices = neighbors.kneighbors([features])
    return indices

if uploaded_file is not None:
    if save_uploaded_file(uploaded_file):
        display_image = Image.open(uploaded_file)
        st.image(display_image, caption="Uploaded Image")
        features = feature_extraction(os.path.join("uploads", uploaded_file.name), model)
        indices = recommend(features, feature_list)

        st.subheader("🛍️ Recommended Outfits")
        col1, col2, col3, col4, col5 = st.columns(5)
        with col1:
            st.image(filenames[indices[0][0]])
        with col2:
            st.image(filenames[indices[0][1]])
        with col3:
            st.image(filenames[indices[0][2]])
        with col4:
            st.image(filenames[indices[0][3]])
        with col5:
            st.image(filenames[indices[0][4]])
    else:
        st.error("Error uploading file. Please try again.")

# Chatbot Section
st.subheader("💬 Fashion Stylist Chatbot")
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

chat_container = st.container()

with chat_container:
    for message in st.session_state.chat_history:
        role_class = "user" if message["role"] == "user" else "bot"
        st.markdown(f"**{role_class.capitalize()}**: {message['content']}")

user_input = st.chat_input("Ask me anything about fashion!")
if user_input:
    st.session_state.chat_history.append({"role": "user", "content": user_input})
    bot_response = model_gemini.generate_content(["You are a fashion stylist. Provide fashion advice.", f"{user_input}"]).text.strip()
    st.session_state.chat_history.append({"role": "assistant", "content": bot_response})
    st.markdown(f"**Bot**: {bot_response}")

st.caption("Created by FashionAI Team")
