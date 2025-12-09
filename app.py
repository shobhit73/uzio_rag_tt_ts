import streamlit as st
import os
from llama_index.core import VectorStoreIndex, StorageContext, Settings
from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.llms.google_genai import GoogleGenAI
from llama_index.embeddings.google_genai import GoogleGenAIEmbedding
import chromadb
from dotenv import load_dotenv

# Load API Key
load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# Configuration
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CHROMA_DB_DIR = os.path.join(BASE_DIR, "chroma_db")
COLLECTION_NAME = "uzio_docs"

# Debug Config
import sqlite3
print(f"DEBUG: SQLite Version: {sqlite3.sqlite_version}")
print(f"DEBUG: Base Directory: {BASE_DIR}")
print(f"DEBUG: Target Chroma DB Path: {CHROMA_DB_DIR}")

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
    /* Import Font */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    
    /* Apply font to text elements only, avoiding icons */
    html, body, .stMarkdown, .stButton, .stTextInput, .stChatInput {
        font-family: 'Inter', sans-serif !important;
    }

    /* Professional Text Styling - High Contrast */
    .stMarkdown p {
        font-size: 16px !important;
        color: #1A202C !important; /* Darker Black/Grey */
        line-height: 1.6;
    }
    
    /* Headings */
    h1, h2, h3 {
        color: #0077B6 !important;
        font-weight: 700 !important;
    }

    /* Chat Message Bubbles */
    .stChatMessage {
        border-radius: 12px;
        border: 1px solid #E2E8F0;
        padding: 1rem;
    }

    /* User Bubble */
    [data-testid="stChatMessage"]:nth-child(2n) {
        background-color: #EBF8FF;
        border-color: #BEE3F8;
    }
    
    /* Assistant Bubble */
    [data-testid="stChatMessage"]:nth-child(2n+1) {
        background-color: #FFFFFF;
        border-color: #E2E8F0;
    }

    /* Fix Expander Icon Glitch by not forcing font on everything */
    .streamlit-expanderHeader {
        font-family: 'Inter', sans-serif;
        color: #2D3748;
        font-weight: 600;
    }
    
    /* Button Styling */
    .stButton button {
        border-radius: 8px;
        background: linear-gradient(90deg, #00A3E0 0%, #0077B6 100%);
        color: white;
        border: none;
        font-weight: 600;
    }
    .stButton button:hover {
        transform: translateY(-1px);
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        color: white;
    }
    
    /* Link styling in markdown */
    .stMarkdown a {
        color: #3182CE !important;
        text-decoration: none;
    }

     /* Sidebar Logo Positioning */
    [data-testid="stSidebar"] img {
        margin-bottom: 20px;
        border-radius: 10px; 
    }
</style>
""", unsafe_allow_html=True)

@st.cache_resource
def load_index():
    print(f"DEBUG: Current Directory: {os.getcwd()}")
    print(f"DEBUG: Files in CWD: {os.listdir(os.getcwd())}")
    if os.path.exists(CHROMA_DB_DIR):
         print(f"DEBUG: {CHROMA_DB_DIR} contents: {os.listdir(CHROMA_DB_DIR)}")
    
    if not os.path.exists(CHROMA_DB_DIR):
        print(f"DEBUG: CHROMA_DB_DIR {CHROMA_DB_DIR} NOT FOUND at path!")
        return None
    
    # Setup Models
    try:
        Settings.embed_model = GoogleGenAIEmbedding(model_name="models/text-embedding-004", api_key=GOOGLE_API_KEY)
        Settings.llm = GoogleGenAI(model="models/gemini-flash-latest", api_key=GOOGLE_API_KEY)
    except Exception as e:
        return None

    try:
        db = chromadb.PersistentClient(path=CHROMA_DB_DIR)
        chroma_collection = db.get_or_create_collection(COLLECTION_NAME)
        vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
        storage_context = StorageContext.from_defaults(vector_store=vector_store)
        return VectorStoreIndex.from_vector_store(vector_store, storage_context=storage_context)
    except Exception as e:
        return None

# Sidebar
with st.sidebar:
    # UZIO Logo (Local Asset)
    if os.path.exists("assets/logo.png"):
        st.image("assets/logo.png", width=180)
    else:
        st.title("UZIO.ai")
    st.write("") # Spacer
    st.markdown("### **AI Support Assistant**")
    st.markdown("**Powered by Gemini Flash 1.5**")
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
                try:
                    # Debug print for Cloud logs
                    print(f"DEBUG: Querying LLM with model {Settings.llm.model}...")
                    response = chat_engine.chat(prompt)
                    st.markdown(response.response)
                    
                    # Show source nodes (especially images)
                    with st.expander("🔍 View Source Context (Text & Images)"):
                        if hasattr(response, 'source_nodes'):
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
                except Exception as e:
                    st.error(f"An error occurred: {str(e)}")
        
        if 'response' in locals() and response:
            st.session_state.messages.append({"role": "assistant", "content": response.response})
