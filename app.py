# pylint: disable=invalid-name
"""
This module demonstrates the usage of the Gemini API in Vertex AI within a Streamlit application.
"""

import os
from google import genai
from google.genai.types import GenerateContentConfig, Part
import streamlit as st
import pandas as pd
from io import StringIO
from PIL import Image

API_KEY = os.environ.get("VERTEX_AI_API_KEY")
PROJECT_ID = os.environ.get("GCP_PROJECT")
LOCATION = os.environ.get("GCP_REGION")

if PROJECT_ID and not LOCATION:
    LOCATION = "europe-west1"

@st.cache_resource
def load_client() -> genai.Client:
    """Load Google Gen AI Client."""
    return genai.Client(
        vertexai=True, project=PROJECT_ID, location=LOCATION, api_key=API_KEY
    )


def get_model_name(name: str | None) -> str:
    """Get the formatted model name."""
    if not name:
        return "Gemini"
    return MODELS.get(name, "Gemini")

st.header(":fire: :pizza: Lunch-a-niser", divider="rainbow")
client = load_client()
st.markdown("""Welcome to the Lunch-a-niser! This app is designed to 'analyse' your lunch and provide you with a description of what you're eating, along with an estimated calorie content. Make better choices and know what you're putting into your mouth!""")

uploaded_file = st.file_uploader("Choose a file", type=["png","jpg","jpeg"], accept_multiple_files=False, label_visibility="visible")
if 'image' not in st.session_state:
    st.session_state.image = None

if uploaded_file is not None:  # Check if a file was uploaded
    try:
        st.session_state.image = Image.open(uploaded_file)
        # Process the file contents here
        st.write("File uploaded and read successfully.")
        st.image(uploaded_file, width=400, caption="Preview of Uploaded Image", use_container_width=True)
    except Exception as e:
        st.error(f"An error occurred: {e}")
else:
    st.info("Please upload a file.")


content = [
    "Please analyse the following picture ", 
    st.session_state.image,
    "\n",
    "Add a short summary description of the picture",
    "Also add each individual item you recognise in the picture, and estimate a rough number of calories",
    "For each individual item, add the results into a table",
    "The columns for the table would be 'Item', 'Description', 'Estimated Calories'",
    "Add a final total for estimated calories as a range"
]
config = GenerateContentConfig(temperature=0.8, max_output_tokens=8192)

tab1, tab2 = st.tabs(["Response", "Prompt"])
image_analysis = st.button(
    "Analyse Food!", key="image_analysis"
)
gemini_pro = "gemini-2.0-flash-001"
#gemini_pro = "Gemini 2.0 Flash"
with tab1:
    if image_analysis and uploaded_file and content:
        with st.spinner(
            f"Generating a description of the Image ..."
        ):
            response = client.models.generate_content(
                model=gemini_pro,
                contents=content,
                config=config,
            ).text
            st.markdown(response)

with tab2:
    st.write("Prompt used:")
    st.code(content, language="markdown")
