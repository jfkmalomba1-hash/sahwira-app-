import streamlit as st
import pandas as pd
import datetime
import matplotlib.pyplot as plt
from fpdf import FPDF

# --- LOAD FROM SECRETS (SAFE) ---
try:
    VALID_KEYS = st.secrets["LICENSE_KEYS"]
    ECO_NAME = st.secrets["ECOCASH_NAME"]
    ECO_NUM = st.secrets["ECOCASH_NUMBER"]
except:
    VALID_KEYS = ["SAHWIRA100","SAHWIRA200","SAHWIRA365","CLINIC2026","TEST123","SAHWIRA5","ADMIN2026"]
    ECO_NAME = "James"
    ECO_NUM = "0771477408"

def check_key():
    if st.session_state.get("activated"):
        return True
    k = st.session_state.get("license_input", "").strip().upper()
    if k in VALID_KEYS:
        st.session_state["activated"] = True
        return True
    return False

st.set_page_config(page_title="Sahwira Health", page_icon="🛡️", layout="wide", initial_sidebar_state="collapsed")

st.markdown("<style>#MainMenu,footer,header,.stDeployButton{visibility:hidden;display:none}.main{background:#F8FAFF}</style>", unsafe_allow_html=True)

st.markdown("""
<div style='background:linear-gradient(135deg,#0D47A1 0%,#1976D2 100%);padding:18px 24px;border-radius:12px;color:white;margin-bottom:20px;'>
<b style='font-size:20px;'>SAHWIRA HEALTH</b><br>
<span style='font-size:12px;'>Harare, Zimbabwe | Secure Patient Portal</span>
</div>
""", unsafe_allow_html=True)

if check_key():
    st.success("Premium Active - Welcome")
    tab1, tab2, tab3 = st.tabs(["Dashboard", "Log Sugar", "Reports"])
    with tab1:
        c1,c2,c3 = st.columns(3)
        c1.metric("AVG SUGAR", "6.8 mmol/L", "In Target")
        c2.metric("LAST READING", "6.5", "Today 07:30")
        c3.metric("STREAK", "12 Days", "Keep going")
        data = pd.DataFrame({'Day':['Mon','Tue','Wed','Thu','Fri','Sat','Sun'], 'Sugar':[6.5,7.2,6.0,7.8,6.9,6.4,6.7]})
        fig, ax = plt.subplots(figsize=(8,3))
        ax.plot(data['Day'], data['Sugar'], marker='o', color='#0D47A1', linewidth=3)
        ax.set_ylabel("mmol/L")
        ax.set_title("Weekly Trend")
        ax.grid(True, alpha=0.2)
        st.pyplot(fig, use_container_width=True)
    with tab2:
        with st.container(border=True):
            sugar = st.number_input("Blood Sugar (mmol/L)", 2.0, 30.0, 6.5, step=0.1)
            when = st.selectbox("When?", ["Fasting", "Before Meal", "After Meal", "Bedtime"])
            notes = st.text_input("Notes")
            if st.button("Save Reading", type="primary", use_container_width=True):
                st.success(f"Saved: {sugar} - {when}")
    with tab3:
        if st.button("Generate PDF Report", type="primary", use_container_width=True):
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Arial", "B", 16)
            pdf.cell(0, 10, "SAHWIRA HEALTH - Patient Report", ln=True, align="C")
            pdf.set_font("Arial", "", 10)
            pdf.cell(0, 8, f"Date: {datetime.date.today()} | Status: Controlled", ln=True)
            pdf.ln(5)
            pdf.multi_cell(0, 5, f"EcoCash: {ECO_NUM} - {ECO_NAME}\nReadings: Mon 6.5, Tue 7.2, Wed 6.0, Thu 7.8, Fri 6.9, Sat 6.4, Sun 6.7\nFor emergencies dial 994.")
            path = "/tmp/report.pdf"
            pdf.output(path)
            with open(path, "rb") as f:
                st.download_button("Download Report", f, file_name="Sahwira_Report.pdf", mime="application/pdf", type="primary", use_container_width=True)
    if st.button("Log out"):
        st.session_state["activated"] = False
        st.rerun()
else:
    st.markdown("<h3 style='text-align:center;color:#0D47A1;'>Premium Patient Access</h3>", unsafe_allow_html=True)
    c1,c2,c3 = st.columns([1,2,1])
    with c2:
        with st.container(border=True):
            st.markdown("**License Key**")
            lic = st.text_input("License", placeholder="SAHWIRA100", label_visibility="collapsed", key="license_input")
            if st.button("ACTIVATE SECURELY", type="primary", use_container_width=True):
                if lic.strip().upper() in VALID_KEYS:
                    st.session_state["activated"] = True
                    st.balloons()
                    st.rerun()
                else:
                    st.error("Invalid key")
            st.info(f"EcoCash to: {ECO_NUM} - {ECO_NAME} - 5 USD = 3 months | 15 USD = 12 months")
            st.link_button("WhatsApp Support", "https://wa.me/263771477408", use_container_width=True)
        st.caption("Secure | Built for Zimbabwe | Emergencies: Dial 994 - Does not replace medical advice.")
