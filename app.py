import streamlit as st
from retriever import Retriever
from openai import OpenAI

# Initialize OpenAI client
openai = OpenAI(api_key="Your_API_KEY")

# Page configuration
st.set_page_config(
    page_title="DocBot — Capillary Docs Chatbot",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Sidebar
with st.sidebar:
    st.title("🤖 DocBot")
    st.markdown(
        """
        Welcome to **Capillary Documentation Chatbot**!
        
        - Ask anything about CapillaryTech docs.
        - The bot retrieves relevant sections and generates a professional answer.
        - Powered by Streamlit.
        """
    )
    st.markdown("---")
    st.caption("Developed by Your Name")

# Load retriever
@st.cache_resource
def load_retriever():
    return Retriever("docs_content.json")  # Your JSON documentation path

retriever = load_retriever()

# Main page title
st.markdown(
    "<h1 style='text-align: center; color: #4B8BBE;'>🤖 DocBot — Capillary Docs Chatbot</h1>",
    unsafe_allow_html=True
)
st.markdown(
    "<p style='text-align: center; color: #306998;'>Ask me anything about CapillaryTech documentation!</p>",
    unsafe_allow_html=True
)

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages with simple spacing
for msg in st.session_state.messages:
    with st.container():
        if msg["role"] == "user":
            st.markdown(f"**You:** {msg['content']}")
        else:
            st.markdown(f"**DocBot:** {msg['content']}")

# Input box
if query := st.chat_input("Type your question about Capillary Docs..."):
    st.session_state.messages.append({"role": "user", "content": query})

    # Display user message instantly
    with st.container():
        st.markdown(f"**You:** {query}")

    # Retrieve relevant docs
    results = retriever.get_best_response(query, top_k=3)

    if not results:
        # If no relevant data is found, skip GPT entirely
        answer = "❌ Sorry, I couldn't find anything relevant in the documentation."
    else:
        # Prepare context for GPT
        context = "\n\n".join([f"Title: {r['title']}\nText: {r['text']}" for r in results])
        prompt = f"""
You are an expert assistant for CapillaryTech documentation.
A user asked: "{query}"
Using the following documentation context, generate a **clear, concise, and professional answer** in natural language.
Context:
{context}
Answer:
"""
        # Generate answer using GPT
        response = openai.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.2
        )
        answer = response.choices[0].message.content

    # Display bot answer
    with st.container():
        st.markdown(f"**DocBot:** {answer}")

    # Save bot message
    st.session_state.messages.append({"role": "assistant", "content": answer})
