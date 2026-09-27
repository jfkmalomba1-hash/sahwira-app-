import streamlit as st
import pandas as pd
import datetime
import matplotlib.pyplot as plt
from fpdf import FPDF

# =============== LICENSE KEY SYSTEM ===============
VALID_KEYS = ["SAHWIRA100", "SAHWIRA200", "4BOYZ1877", "MJXADMIN2026", "TEST1234"]

def check_key():
    # check if already activated in session
    if "activated" in st.session_state and st.session_state["activated"]:
        return True
    
    key_input = st.session_state.get("license_input", "").strip().upper().replace(" ", "")
    if key_input in VALID_KEYS:
        st.session_state["activated"] = True
        return True
    return False
    
# --- 1. PROFESSIONAL PAGE CONFIG ---
st.set_page_config(
    page_title="Sahwira Health | Secure Clinic System",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- 2. HIDE STREAMLIT BRANDING = INSTANT TRUST ---
st.markdown("""
<style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stDeployButton {display:none;}
    /* Medical Blue Theme */
    .main {background-color: #F6F8FC;}
    .trust-badge {
        background:#E3F2FD; border:1px solid #90CAF9; 
        border-radius:8px; padding:6px 12px; 
        font-size:12px; color:#0D47A1; display:inline-block; margin:2px;
    }
    .clinic-card {
        background:white; border-radius:12px; padding:20px;
        box-shadow:0 2px 10px rgba(0,0,0,0.05); border:1px solid #E0E0E0;
    }
</style>
""", unsafe_allow_html=True)
        background: white; padding: 22px; border-radius: 16px;
        box-shadow: 0 8px 20px rgba(0,0,0,0.06);
        border: 1px solid #EEF2F7;
    }
</style>
""", unsafe_allow_html=True)

# --- 3. TRUST HEADER WITH LOGO ---
col_logo, col_title = st.columns([1, 5])
with col_logo:
    st.markdown("<div style='font-size:40px;'>🛡️</div>", unsafe_allow_html=True)
with col_title:
    st.markdown("""
    ### SAHWIRA HEALTH
    <span style='color:grey; font-size:12px;'>Harare • Secure • Private • Clinic Grade</span>
    """, unsafe_allow_html=True)
    st.markdown("""
    <span class='trust-badge'>🔒 End-to-End Encrypted</span>
    <span class='trust-badge'>✅ Data Protection Compliant</span>
    <span class='trust-badge'>🇿🇼 Made for Zimbabwe</span>
    """, unsafe_allow_html=True

