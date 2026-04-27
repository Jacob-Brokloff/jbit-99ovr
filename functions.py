import json
import re
from agents import crawler_agent, search_agent
from email_validator import validate_email, EmailNotValidError
import streamlit as st


def parse_json(text: str):
    # Strip markdown code fences if present
    text = re.sub(r"```json|```", "", text).strip()
    try:
        return json.loads(text)
    except Exception:
        return []

def verify_email(email: str, check_deliverability: bool = True) -> dict:
    try:
        valid = validate_email(email, check_deliverability=check_deliverability)
        return {
            "email": email,
            "normalized": valid.normalized,
            "valid": True,
            "reason": None
        }
    except EmailNotValidError as e:
        return {
            "email": email,
            "normalized": None,
            "valid": False,
            "reason": str(e)
        }

        
def run(market: str):
    try:
        search_raw = search_agent.run(f"{market} contacts").content
        print("SEARCH:", search_raw)
        urls = parse_json(search_raw)
    except Exception as e:
        print(f"Search failed: {e}")
        return []

    if not urls:
        return []

    crawl_raw = crawler_agent.run(f"Extract contacts from: {json.dumps(urls)}").content
    print("CRAWL:", crawl_raw)
    contacts = parse_json(crawl_raw)

    verified = []
    for contact in contacts:
        email = contact.get("email")
        if not email:
            continue
        result = verify_email(email)
        if result["valid"]:
            contact["email"] = result["normalized"]  # use cleaned version
            verified.append(contact)
        else:
            print(f"Rejected {email}: {result['reason']}")

    return verified


def require_auth():
    if st.session_state.get("authenticated"):
        return
    USERS = st.secrets["users"]
    if st.session_state.get("attempts", 0) >= 5:
        st.error("Too many attempts.")
        st.stop()
    st.title("🔒 Login")
    username = st.text_input("Username")
    pwd = st.text_input("Password", type="password")
    if st.button("Login"):
        if USERS.get(username) == pwd and pwd:
            st.session_state.authenticated = True
            st.session_state.username = username
            st.rerun()
        else:
            st.session_state.attempts = st.session_state.get("attempts", 0) + 1
            st.error(f"Incorrect credentials ({5 - st.session_state.attempts} attempts left)")
    st.stop()
