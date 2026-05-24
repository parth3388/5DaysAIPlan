import streamlit as st
from transformers import BlipProcessor, BlipForConditionalGeneration, BlipForQuestionAnswering
from PIL import Image
import torch

# -------------------------------
# Page Configuration & Styling
# -------------------------------
st.set_page_config(
    page_title="Vision AI Pro",
    page_icon="👁️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for a more premium look
st.markdown("""
    <style>
    .main {
        background-color: #f8f9fa;
        font-family: 'Inter', sans-serif;
    }
    .stButton>button {
        border-radius: 20px;
        background-color: #4CAF50;
        color: white;
        font-weight: bold;
    }
    .stTextInput>div>div>input {
        border-radius: 10px;
    }
    /* Simple card style helper */
    .css-1d391kg {
        background-color: #ffffff;
        border-radius: 15px;
        padding: 20px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    </style>
""", unsafe_allow_html=True)

# -------------------------------
# Sidebar Info
# -------------------------------
with st.sidebar:
    st.image("https://huggingface.co/front/assets/huggingface_logo-noborder.svg", width=50)
    st.title("About Vision AI")
    st.info(
        "Upload any image and let our AI analyze it! "
        "Built using the powerful Salesforce BLIP model from Hugging Face, "
        "this tool allows you to extract captions and ask direct questions about your images."
    )
    st.divider()
    st.caption("Powered by Transformers & Streamlit")

# -------------------------------
# Load Models (cached for speed)
# -------------------------------
@st.cache_resource(show_spinner=False)
def load_models():
    # Captioning Model
    processor_cap = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
    model_cap = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")
    
    # VQA Model
    processor_vqa = BlipProcessor.from_pretrained("Salesforce/blip-vqa-base")
    model_vqa = BlipForQuestionAnswering.from_pretrained("Salesforce/blip-vqa-base")
    
    return processor_cap, model_cap, processor_vqa, model_vqa

with st.spinner("Loading Vision Models... Please wait (this may take a moment)."):
    try:
        processor_cap, model_cap, processor_vqa, model_vqa = load_models()
    except Exception as e:
        st.error(f"Error loading models: {e}")
        st.stop()

# -------------------------------
# Main UI
# -------------------------------
st.title("✨ Vision AI Studio - Image Intelligence")
st.markdown("Unlock the hidden details of your images through AI-powered captioning and visual QA.")
st.divider()

col1, col2 = st.columns([1, 1.2], gap="large")

with col1:
    st.subheader("1. Upload Image")
    uploaded_file = st.file_uploader("Drop an image here", type=["png", "jpg", "jpeg"], help="Supported formats: PNG, JPG, JPEG")
    
    if uploaded_file is not None:
        try:
            image = Image.open(uploaded_file).convert("RGB")
            st.image(image, caption="Current Image", use_container_width=True)
            
            # Reset chat history if it's a new file (basic check)
            if "last_file" not in st.session_state or st.session_state.last_file != uploaded_file.name:
                st.session_state.chat_history = []
                st.session_state.last_file = uploaded_file.name
                
        except Exception as e:
            st.error("Failed to load image. Please try another one.")
            image = None
    else:
        st.info("Awaiting image upload...")
        image = None

with col2:
    if image is not None:
        st.subheader("2. AI Analysis")
        
        # Analyze Button
        if st.button("🔍 Generate Comprehensive Caption", use_container_width=True):
            with st.spinner("Analyzing image..."):
                try:
                    inputs = processor_cap(image, return_tensors="pt")
                    out = model_cap.generate(**inputs, max_new_tokens=50)
                    caption = processor_cap.decode(out[0], skip_special_tokens=True)
                    st.success("**Caption:** " + caption)
                except Exception as e:
                    st.error("Error generating caption.")
        
        st.divider()
        st.subheader("3. Ask Questions")
        
        if "chat_history" not in st.session_state:
            st.session_state.chat_history = []
        
        question = st.text_input("What would you like to know about this image?", placeholder="E.g. What color is the car?")
        
        if question:
            with st.spinner("Thinking..."):
                try:
                    inputs_q = processor_vqa(image, question, return_tensors="pt")
                    out_q = model_vqa.generate(**inputs_q, max_new_tokens=50)
                    answer = processor_vqa.decode(out_q[0], skip_special_tokens=True)
                    
                    # Prepend to history so latest is on top
                    st.session_state.chat_history.insert(0, {"q": question, "a": answer})
                except Exception as e:
                    st.error("Error answering question.")
        
        # Display chat history
        if st.session_state.chat_history:
            st.markdown("### Conversation History")
            for chat in st.session_state.chat_history:
                with st.chat_message("user"):
                    st.write(chat["q"])
                with st.chat_message("assistant"):
                    st.write(chat["a"])
    else:
        st.empty()

# -------------------------------
# Footer
# -------------------------------
st.markdown("<br><br><br>", unsafe_allow_html=True)
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: gray; font-size: 0.8em;'>"
    "Vision AI Studio | Built for seamless image understanding.</div>", 
    unsafe_allow_html=True
)