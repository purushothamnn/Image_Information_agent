import streamlit as st
import google.generativeai as genai
from PIL import Image
import os

# Configure Gemini API
def configure_gemini_api():
    """
    Configure the Gemini API with the API key.
    """
    # Prompt user to enter API key if not set
    GOOGLE_API_KEY = st.sidebar.text_input(
        "Enter your Google Gemini API Key", 
        type="password",
        help="You can get your API key from https://makersuite.google.com/app/apikey"
    )
    
    if not GOOGLE_API_KEY:
        st.sidebar.warning("Please enter your Gemini API Key")
        return None
    
    try:
        genai.configure(api_key=GOOGLE_API_KEY)
        # Verify API key by making a simple call
        models = [model.name for model in genai.list_models() 
                  if 'generateContent' in model.supported_generation_methods]
        
        if not models:
            st.sidebar.error("Invalid API Key or no compatible models found")
            return None
        
        st.sidebar.success("API Key validated successfully!")
        return genai
    except Exception as e:
        st.sidebar.error(f"Error configuring API: {e}")
        return None

# Function to generate image information
def generate_image_info(image):
    """
    Generate information about the uploaded image using Gemini.
    
    :param image: Uploaded image file
    :return: Generated text description
    """
    # Load the image
    img = Image.open(image)
    
    # Initialize the model
    try:
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        # Generate content
        response = model.generate_content(
            [
                "Analyze this image in detail. Provide comprehensive information including:",
                "1. A detailed description of the image contents",
                "2. Any notable objects, people, or scenes",
                "3. Potential context or setting",
                "4. Any interesting or unique aspects of the image",
                img
            ]
        )
        return response.text
    except Exception as e:
        st.error(f"An error occurred during image analysis: {e}")
        return "Could not generate image information."

# Streamlit app main function
def main():
    # Set page configuration
    st.set_page_config(
        page_title="Image Information Generator",
        page_icon=":camera:",
        layout="wide"
    )
    
    # Title and description
    st.title("🖼️ Image Information Generator")
    st.write("Upload an image and get detailed information using Gemini AI")
    
    # Gemini API setup
    gemini = configure_gemini_api()
    
    # Image upload
    uploaded_file = st.file_uploader(
        "Choose an image...", 
        type=["jpg", "jpeg", "png", "webp"],
        help="Upload an image to generate detailed information"
    )
    
    # Process uploaded image
    if uploaded_file is not None and gemini is not None:
        # Display the uploaded image
        col1, col2 = st.columns(2)
        
        with col1:
            st.image(uploaded_file, caption="Uploaded Image", use_column_width=True)
        
        with col2:
            # Generate and display image information
            with st.spinner('Generating image information...'):
                image_info = generate_image_info(uploaded_file)
                st.subheader("Image Analysis")
                st.write(image_info)

# Run the app
if __name__ == "__main__":
    main()