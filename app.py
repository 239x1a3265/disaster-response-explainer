import streamlit as st

from rag.loader import load_documents
from rag.retriever import retrieve_relevant_docs
from rag.gemini import call_gemini

# ----------------------------
# PAGE CONFIG
# ----------------------------
st.set_page_config(
    page_title="Disaster Response & Relief Explainer Bot",
    page_icon="🌪️",
    layout="centered"
)

# ----------------------------
# SIDEBAR
# ----------------------------
with st.sidebar:
    st.header("ℹ️ About This Bot")
    st.write(
        """
This AI assistant explains **disaster response and relief processes**.

**What it does:**
- Explains evacuation procedures
- Describes relief camp operations
- Explains disaster response stages
- Shares general safety guidelines

**What it does NOT do:**
- ❌ Issue emergency alerts
- ❌ Give real-time instructions
- ❌ Coordinate rescue
"""
    )

    st.markdown("---")
    st.caption("⚠️ For emergencies, contact official services.")

# ----------------------------
# MAIN HEADER
# ----------------------------
st.markdown(
    "<h1 style='text-align: center;'>🌪️ Disaster Response & Relief Explainer</h1>",
    unsafe_allow_html=True
)

st.markdown(
    "<p style='text-align: center; color: gray;'>"
    "Public information assistant for disaster preparedness & awareness"
    "</p>",
    unsafe_allow_html=True
)

# ----------------------------
# DISCLAIMER BOX
# ----------------------------
st.warning(
    "⚠️ **Disclaimer:** This system provides general informational explanations only. "
    "It does NOT issue alerts, provide real-time instructions, or replace emergency services."
)

# ----------------------------
# LOAD DOCUMENTS
# ----------------------------
documents = load_documents()

# ----------------------------
# EMERGENCY SAFETY FILTER
# ----------------------------
EMERGENCY_KEYWORDS = [
    "help", "urgent", "rescue", "trapped",
    "emergency", "call", "save me", "danger",
    "stuck", "need help"
]

def is_emergency_query(text):
    text = text.lower()
    return any(word in text for word in EMERGENCY_KEYWORDS)

# ----------------------------
# RESPONSE GENERATOR
# ----------------------------
def generate_response(question):
    retrieved_docs = retrieve_relevant_docs(question, documents)

    if not retrieved_docs:
        return "I do not have information on this topic."

    context = "\n\n".join(retrieved_docs)
    return call_gemini(context, question)

# ----------------------------
# USER INPUT (CHAT STYLE)
# ----------------------------
st.markdown("### 💬 Ask a Question")

user_question = st.text_input(
    "Example: Explain evacuation procedures",
    placeholder="Type your question here..."
)

# ----------------------------
# HANDLE RESPONSE
# ----------------------------
if user_question:
    if is_emergency_query(user_question):
        st.error(
            "🚨 I can only explain general disaster procedures.\n\n"
            "Please contact **local emergency services immediately**."
        )
    else:
        with st.spinner("🔍 Generating explanation..."):
            answer = generate_response(user_question)

        st.markdown("### ✅ Explanation")
        st.info(answer)

# ----------------------------
# FOOTER
# ----------------------------
st.markdown("---")
st.caption(
    "Built using Streamlit, Gemini AI, and Retrieval-Augmented Generation (RAG)"
)
st.markdown("""
<style>

/* =============================
   GLOBAL BACKGROUND & FONT
============================= */
.stApp {
    background: radial-gradient(circle at top, #1e0033 0%, #0b0014 60%, #000000 100%);
    font-family: "Inter", "Segoe UI", sans-serif;
}

/* =============================
   MAIN CONTENT WIDTH
============================= */
.block-container {
    max-width: 900px;
    padding-top: 2rem;
}

/* =============================
   MAIN TITLE
============================= */
h1 {
    font-size: 2.6rem;
    font-weight: 800;
    color: #e9d5ff;
    letter-spacing: -0.5px;
}

/* =============================
   SUBTITLE / PARAGRAPHS
============================= */
p {
    color: #c4b5fd;
    font-size: 1rem;
}

/* =============================
   SIDEBAR (BLACK + PURPLE)
============================= */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #000000, #1e0033);
    padding-top: 1.2rem;
}

section[data-testid="stSidebar"] h1,
section[data-testid="stSidebar"] h2,
section[data-testid="stSidebar"] h3,
section[data-testid="stSidebar"] p,
section[data-testid="stSidebar"] li {
    color: #ede9fe !important;
}

/* =============================
   DISCLAIMER CARD
============================= */
div[data-testid="stAlert"] {
    background: linear-gradient(135deg, #2a003f, #1a002b);
    border-left: 6px solid #a855f7;
    border-radius: 16px;
    padding: 1rem;
    font-size: 0.95rem;
    color: #f5d0fe;
}

/* =============================
   INPUT BOX
============================= */
input {
    border-radius: 14px !important;
    padding: 14px !important;
    font-size: 1rem !important;
    color: #f5d0fe !important;
    background-color: #0f001a !important;
    border: 1px solid #9333ea !important;
    box-shadow: 0 0 18px rgba(168,85,247,0.35) !important;
}

/* =============================
   INPUT PLACEHOLDER
============================= */
input::placeholder {
    color: #a78bfa !important;
}

/* =============================
   BOT RESPONSE CARD
============================= */
div[data-testid="stInfo"] {
    background: linear-gradient(135deg, #14001f, #0b0014);
    border-left: 6px solid #a855f7;
    border-radius: 18px;
    padding: 22px;
    font-size: 1.05rem;
    color: #f5d0fe;
    box-shadow: 0 14px 40px rgba(168,85,247,0.45);
    animation: fadeUp 0.4s ease-in-out;
}

/* =============================
   ERROR MESSAGE
============================= */
div[data-testid="stError"] {
    background-color: #3b0764;
    border-radius: 16px;
    color: #fdf4ff;
}

/* =============================
   SPINNER TEXT
============================= */
div[data-testid="stSpinner"] {
    color: #c084fc;
    font-weight: 600;
}

/* =============================
   FOOTER
============================= */
footer {
    visibility: hidden;
}

.footer-text {
    text-align: center;
    font-size: 0.85rem;
    color: #a78bfa;
    margin-top: 40px;
}

/* =============================
   ANIMATION
============================= */
@keyframes fadeUp {
    from {
        opacity: 0;
        transform: translateY(10px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

</style>
""", unsafe_allow_html=True)

