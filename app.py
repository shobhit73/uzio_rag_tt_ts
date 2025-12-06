import streamlit as st
import os
from llama_index.core import VectorStoreIndex, StorageContext, Settings
from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.llms.google_genai import GoogleGenerativeAI
from llama_index.embeddings.google_genai import GoogleGenerativeAIEmbedding
import chromadb
from dotenv import load_dotenv

# Load API Key
load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# Configuration
CHROMA_DB_DIR = "chroma_db"
COLLECTION_NAME = "uzio_docs"

# Page Config
st.set_page_config(
    page_title="UZIO AI Assistant",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for Professional Look
st.markdown("""
<style>
    /* Global Font & Theme */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    
    html, body, [class*="st-"] {
        font-family: 'Inter', sans-serif;
    }

    /* Professional Text Styling */
    .stMarkdown, p, div {
        font-size: 15px !important;
        color: #2D3748;
    }

    h1, h2, h3 {
        color: #00A3E0; /* Cyan/Blue from Logo */
        font-weight: 700;
        background: -webkit-linear-gradient(45deg, #00A3E0, #1A365D);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    /* Chat Message Bubbles */
    .stChatMessage {
        border-radius: 12px;
        margin-bottom: 10px;
        border: 1px solid #E2E8F0;
    }

    [data-testid="stChatMessage"]:nth-child(2n+1) {
        background-color: #F8FAFC; 
    }

    [data-testid="stChatMessage"]:nth-child(2n) {
        background-color: #E0F2F1; /* Very light cyan tint */
        border-color: #B2DFDB;
    }
    
    /* Button Styling - Gradient Theme */
    .stButton button {
        width: 100%;
        border-radius: 8px;
        height: 3em;
        background: linear-gradient(90deg, #00A3E0 0%, #0077B6 100%); /* Cyan to Blue Gradient */
        color: white;
        font-weight: 600;
        border: none;
        transition: transform 0.1s ease;
    }
    .stButton button:hover {
        transform: scale(1.02);
        color: white;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    
    /* Secondary Button */
    button[kind="secondary"] {
        background: transparent !important;
        border: 1px solid #CBD5E0 !important;
        color: #718096 !important;
        box-shadow: none !important;
    }

    /* Sidebar Logo Positioning */
    [data-testid="stSidebar"] img {
        margin-bottom: 20px;
        border-radius: 10px; /* Slight rounding if square */
    }
    
</style>
""", unsafe_allow_html=True)

@st.cache_resource
def load_index():
    if not os.path.exists(CHROMA_DB_DIR):
        return None
    
    # Setup Models
    Settings.embed_model = GoogleGenerativeAIEmbedding(model_name="models/text-embedding-004", api_key=GOOGLE_API_KEY)
    Settings.llm = GoogleGenerativeAI(model="models/gemini-2.0-flash-001", api_key=GOOGLE_API_KEY)

    db = chromadb.PersistentClient(path=CHROMA_DB_DIR)
    chroma_collection = db.get_or_create_collection(COLLECTION_NAME)
    vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
    storage_context = StorageContext.from_defaults(vector_store=vector_store)
    
    return VectorStoreIndex.from_vector_store(vector_store, storage_context=storage_context)

# Sidebar
with st.sidebar:
    # UZIO Logo (Local Asset)
    if os.path.exists("assets/logo.png"):
        st.image("assets/logo.png", width=180)
    else:
        st.title("UZIO.ai")
    st.write("") # Spacer
    st.markdown("### **AI Support Assistant**")
    st.markdown("**Powered by Gemini 2.0 Flash**")
    st.markdown("---")
    st.markdown("Use this assistant to quickly find answers about UZIO Scheduling and Time Tracking modules.")
    
    st.markdown("### 🛠️ Actions")
    if st.button("🗑️ Clear Conversation", type="secondary"):
        st.session_state.messages = []
        st.rerun()
    
    st.markdown("---")
    st.markdown("### 📊 Capabilities")
    st.info("""
    - **Time Tracking**: Overtime, Breaks, Geofencing
    - **Scheduling**: Shifts, Swaps, Offers
    - **Multi-modal**: Understands charts & screenshots
    """)

# Main Content
if "messages" not in st.session_state:
    st.session_state.messages = []

index = load_index()

if not index:
    st.error("⚠️ **System Not Ready**: Index not found. Please run the data processing scripts.")
else:
    chat_engine = index.as_chat_engine(
        chat_mode="context", 
        system_prompt=(
            "You are an expert UZIO Software Consultant. "
            "Your goal is to provide clear, step-by-step answers based strictly on the provided documentation. "
            "If the context includes image descriptions (screenshots/charts), use them to explain where to click or what the UI looks like. "
            "Be professional, concise, and friendly."
        )
    )

    # Welcome Screen (if no messages)
    if not st.session_state.messages:
        st.markdown("<div style='text-align: center; margin-top: 50px;'><h1>👋 Welcome to UZIO AI Support</h1></div>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center; color: #718096; font-size: 1.1em;'>I can help you navigate Scheduling and Time Tracking settings. What would you like to know?</p>", unsafe_allow_html=True)
        st.write("")
        st.write("")
        
        col1, col2, col3 = st.columns(3)
        
        # Helper Button Logic
        def add_msg(text):
            st.session_state.messages.append({"role": "user", "content": text})
            
        with col1:
            if st.button("👥 How to add employees?", key="btn1"):
                add_msg("How do I add employees to Time Tracking?")
                st.rerun()
        with col2:
            if st.button("⏱️ Explain Overtime Rules", key="btn2"):
                add_msg("How do I configure overtime rules (Daily/Weekly)?")
                st.rerun()
        with col3:
            if st.button("📍 What is Geofencing?", key="btn3"):
                add_msg("How does Geofencing work and how do I set it up?")
                st.rerun()

    # Chat Interface
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("Ask about Scheduling, Time Tracking, or Reports..."):
        # Add user message
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Generate response
        with st.chat_message("assistant"):
            with st.spinner("Analyzing UZIO documentation..."):
                response = chat_engine.chat(prompt)
                st.markdown(response.response)
                
                # Show source nodes (especially images)
                with st.expander("🔍 View Source Context (Text & Images)"):
                    for node in response.source_nodes:
                        st.markdown(f"**Score:** {node.score:.2f}")
                        # Clean up text for display
                        text_content = node.node.get_text().replace("Image Path:", "").strip()
                        st.markdown(f"> {text_content[:300]}...")
                        
                        # Check for Image
                        if "image_path" in node.node.metadata:
                            img_path = node.node.metadata["image_path"]
                            if os.path.exists(img_path):
                                st.image(img_path, caption="Relevant Screenshot/Chart", width=400)
                                
        st.session_state.messages.append({"role": "assistant", "content": response.response})
