import streamlit as st
from PIL import Image, ImageOps
import requests
import io

# --- CONFIGURATION ---
# Replace 'YOUR_API_KEY' with the key you got from remove.bg
API_KEY = 'rFyj8cLX8FabQ1acaQ3ztraw'

st.set_page_config(page_title="AI Image Studio", layout="wide")

# --- UI DESIGN ---
st.title("✨ AI Image Magic Studio")
st.markdown("Remove backgrounds, add colors, and enhance your photos in one click.")

uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # Display Original
    col1, col2 = st.columns(2)
    input_image = Image.open(uploaded_file)
    col1.image(input_image, caption="Original Image", use_container_width=True)

    # --- TOOLS ---
    st.sidebar.header("Toolbox")
    task = st.sidebar.radio("Select Action:", ["Remove Background", "Enhance Quality"])
    bg_color = st.sidebar.color_picker("Pick a Background Color (if removing BG)", "#ffffff")

    if st.button("Process Image"):
        with st.spinner('Processing...'):
            if task == "Remove Background":
                # API Call to remove.bg
                response = requests.post(
                    'https://api.remove.bg/v1.0/removebg',
                    files={'image_file': uploaded_file.getvalue()},
                    data={'size': 'auto', 'bg_color': bg_color},
                    headers={'X-Api-Key': API_KEY},
                )
                
                if response.status_code == requests.codes.ok:
                    processed_img = Image.open(io.BytesIO(response.content))
                    col2.image(processed_img, caption="Processed Image", use_container_width=True)
                    
                    # Download Button
                    btn = st.download_button(
                        label="Download High-Res Image",
                        data=response.content,
                        file_name="ai_studio_result.png",
                        mime="image/png"
                    )
                else:
                    st.error("Error: Check your API Key or connection.")

            elif task == "Enhance Quality":
                # Simple AI-based enhancement (Auto-contrast & Sharpness)
                enhanced = ImageOps.autocontrast(input_image)
                col2.image(enhanced, caption="Enhanced Image", use_container_width=True)
                
                # Buffer to save image
                buf = io.BytesIO()
                enhanced.save(buf, format="PNG")
                st.download_button(label="Download Enhanced", data=buf.getvalue(), file_name="enhanced.png")
