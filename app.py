import streamlit as st
from transformers import GPT2LMHeadModel, GPT2Tokenizer
import torch

# --- PAGE CONFIG ---
st.set_page_config(page_title="AI Text Architect", page_icon="✍️", layout="centered")

# --- LOAD MODEL (Cached for speed) ---
@st.cache_resource
def load_model():
    model_name = "gpt2"
    tokenizer = GPT2Tokenizer.from_pretrained(model_name)
    model = GPT2LMHeadModel.from_pretrained(model_name)
    return tokenizer, model

tokenizer, model = load_model()

# --- UI DESIGN ---
st.title("✍️ AI Paragraph Generator")
st.markdown("Build coherent paragraphs using a transformer-based GPT model.")

with st.sidebar:
    st.header("Settings")
    length = st.slider("Paragraph Length", 50, 300, 150)
    temp = st.slider("Creativity (Temperature)", 0.5, 1.2, 0.7)
    top_p = st.slider("Nucleus Sampling (Top-P)", 0.5, 1.0, 0.9)

# User Input
prompt = st.text_area("Enter your topic or starting sentence:", "The future of space exploration...")

if st.button("Generate Paragraph"):
    with st.spinner("AI is crafting your text..."):
        # Text Generation Logic
        input_ids = tokenizer.encode(prompt, return_tensors="pt")
        output = model.generate(
            input_ids,
            max_length=length,
            temperature=temp,
            top_p=top_p,
            no_repeat_ngram_size=3,
            do_sample=True
        )
        
        result = tokenizer.decode(output[0], skip_special_tokens=True)
        
        # Display Results
        st.subheader("Generated Text:")
        st.success(result)
        
        # Download Button (Mentors love this feature!)
        st.download_button("Download Text", result, file_name="generated_text.txt")
        