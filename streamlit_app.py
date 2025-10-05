import streamlit as st
from tutor_cag.cli import build_graph
from tutor_cag.graph import Message

st.set_page_config(page_title="Tutor-CAG", page_icon="🎓", layout="centered")

st.title("Tutor-CAG: Data Science Tutor 🎓")

if "graph" not in st.session_state:
    st.session_state.graph = build_graph()
if "history" not in st.session_state:
    st.session_state.history = []  # list[dict(role, content)]

with st.sidebar:
    st.subheader("Session")
    if st.button("Reset conversation", use_container_width=True):
        st.session_state.history = []
        st.rerun()
    st.markdown("Examples:")
    st.caption("• Explain the bias-variance tradeoff\n• What is cross validation?\n• CLT intuition?")

# Render chat history
for msg in st.session_state.history:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if prompt := st.chat_input("Ask about data science..."):
    # Show user message
    st.session_state.history.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Build Message list and get response
    history_models = [Message(role=m["role"], content=m["content"]) for m in st.session_state.history]
    response = st.session_state.graph.run(history_models)

    assistant_text = response.content
    st.session_state.history.append({"role": "assistant", "content": assistant_text})
    with st.chat_message("assistant"):
        st.markdown(assistant_text)
