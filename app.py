from dotenv import load_dotenv
load_dotenv()  # Load all the environment variables from .env

import streamlit as st
import os
from PIL import Image
import google.generativeai as genai

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Load Gemini pro vision model
model = genai.GenerativeModel('gemini-pro-vision')

def get_gemini_response(input, image, user_prompt):
    response = model.generate_content([input, image[0], user_prompt])
    return response.text

def input_image_details(uploaded_file):
    if uploaded_file is not None:
        # Read the file into bytes
        bytes_data = uploaded_file.getvalue()

        image_parts = [
            {
                "mime_type": uploaded_file.type,  # Get the mime type of the uploaded file
                "data": bytes_data
            }
        ]
        return image_parts
    else:
        raise FileNotFoundError("No file uploaded")

# Initialize our streamlit app
st.set_page_config(page_title="MultiLanguage Invoice Extractor", layout="wide")

# Add a sidebar with a small 3D box containing the message
st.sidebar.markdown(
    """
    <div style='
        background-color: #f0f8ff;
        border-radius: 10px;
        padding: 20px;
        margin-bottom: 20px;
        transform: perspective(1000px) rotateY(-20deg);
    '>
        <h3 style='color: #333333; font-size: 18px; margin-bottom: 10px;'>Upload any images</h3>
        <p style='color: #555555; font-size: 14px;'>You can upload not only invoice images but also all kinds of images. Then, write a prompt to extract information from the image.</p>
    </div>
    """,
    unsafe_allow_html=True
)

# Add header
st.markdown(
    """
    <div style='display: flex; align-items: center; justify-content: center; flex-direction: column;'>
        <h1 style='color: #f63366; text-align: center; font-size: 36px; margin-bottom: 20px;'>MultiLanguage Invoice Extractor</h1>
    </div>
    """,
    unsafe_allow_html=True
)

# Add text input with styling
input_prompt = st.text_area("Input Prompt:", height=100)

# Add file uploader with styling
uploaded_file = st.file_uploader("Choose an image of the invoice...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    st.sidebar.subheader("Uploaded Image:")
    st.sidebar.image(uploaded_file, caption="Uploaded Image.", use_column_width=True)

submit = st.button("Tell me about the invoice", key="submit")

# If submit button is clicked
if submit:
    if uploaded_file is None:
        st.error("Please upload an image of the invoice.")
    else:
        with st.spinner("Extracting information..."):
            input_data = input_prompt.strip()
            image_data = input_image_details(uploaded_file)
            response = get_gemini_response(input_data, image_data, input_prompt)
            st.success("Extraction completed!")

            # Add a catchy design to the result section
            st.markdown(
                """
                <div style='background-color: #f9f9f9; border-radius: 10px; padding: 20px; margin-top: 20px;'>
                    <h2 style='color: #333333; text-align: center; font-size: 24px; margin-bottom: 20px;'>The Response</h2>
                    <p style='color: #555555; font-size: 18px; line-height: 1.6;'>{}</p>
                </div>
                """.format(response),
                unsafe_allow_html=True
            )


# If like this app star respository





