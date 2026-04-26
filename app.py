import streamlit as st
import pandas as pd
import numpy as np
from dotenv import load_dotenv
load_dotenv()
from agents import crawler_agent, search_agent
from functions import run

st.set_page_config(page_title="Contact Automation", page_icon="⚡", layout="wide")  # moved up + wide

st.title("Contact Automation")
prompt = st.text_input("Market Query", value="Youth travel sports programs in Cleveland Ohio")

col1, col2 = st.columns(2)
runs = col1.slider("Runs", 1, 10, 5)
target = col2.slider("Target Contacts", 1, 10, 5)

submit = st.button("Run")

if submit:
    if not prompt:
        st.warning("Enter a query first.")
    else:
        with st.spinner("Running..."):
            collected = []
            attempts = 0
            while len(collected) < target and attempts < runs:
                result = run(prompt)
                collected += result
                attempts += 1

        df = pd.DataFrame(collected)
        
        # simple stats row
        c1, c2, c3 = st.columns(3)
        c1.metric("Contacts Found", len(collected))
        c2.metric("Runs Completed", attempts)
        c3.metric("Target Hit", "✅" if len(collected) >= target else "❌")

        st.dataframe(df, use_container_width=True)
