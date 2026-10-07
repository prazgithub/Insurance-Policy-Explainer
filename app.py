import sys
sys.path.append("src")          # so we can import our files from src/

import streamlit as st

from qa import answer

st.set_page_config(page_title="Insurance Policy Explainer", page_icon="🛡️")

st.title("🛡️ Insurance Policy Explainer")
st.caption("Ask questions about the policy documents. This is an explainer, not insurance advice.")

# Sidebar options
st.sidebar.header("Options")
simple = st.sidebar.checkbox("Explain in extra simple language", value=False)

# Main question box
question = st.text_input(
    "Your question",
    placeholder="e.g. What is the waiting period for pre-existing diseases?",
)

if st.button("Ask") and question.strip():
    q = question
    if simple:
        q = question + " (Explain like I am 12 years old, with a short everyday example.)"

    with st.spinner("Searching the policy..."):
        text, chunks = answer(q)

    st.subheader("Answer")
    st.write(text)

    with st.expander("Sources"):
        for c in chunks:
            st.markdown(f"**Page {c['page']}**, `{c['source']}`")
            st.write(c["text"])
            st.divider()