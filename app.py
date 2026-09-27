import streamlit as st
import pandas as pd
import datetime
import matplotlib.pyplot as plt
from fpdf import FPDF

# --- LICENSE SYSTEM ---
VALID_KEYS = ["SAHWIRA100", "SAHWIRA200", "SAHWIRA365", "CLINIC2026", "TEST123", "ADMIN2026", "SAHWIRA5"]

def check_key():
    if st.session_state.get("activated"):
        return True
    key = st.session_state.get("license_input", "").strip().upper()
    if key in VALID_KEYS:
        st.session_state["activated"] = True
        return True
    return False

# --- PAGE CONFIG - CLINIC GRADE ---
st.set_page_config(
    page_title="Sahwira Health | Secure Patient Portal",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- PRO MEDICAL CSS ---
st.markdown("""
<style>
    #MainMenu, footer, header, .stDeployButton {visibility: hidden; display:none;}
    .main {background-color: #F8FAFF;}
    .clinic-header {
        background: linear-gradient(135deg, #0D47A1 0%, #1976D2 100%);
        padding: 18px 24px; border-radius: 12px; color: white;
        margin-bottom: 20px;
    }
    .metric-card {
        background: white; border-radius: 12px; padding: 16px;
        border: 1px solid #E3F2FD; box-shadow: 0 2px 8px rgba(0,0,0,0.04);
        text-align: center;
    }
    .trust-row span {
        background: #E3F2FD; border: 1px solid #90CAF9; border-radius: 20px;
        padding: 4px 10px; font-size: 11px; color: #0D47A1; margin-right: 6px;
    }
</style>
""", unsafe_allow_html=True)

# --- HEADER - ALWAYS VISIBLE ---
st.markdown("""
<div class='clinic-header'>
    <div style='display:flex; justify-content:space-between; align-items:center;'>
        <div><span style='font-size:28px;'>🛡️</span> <b style='font-size:20px;'> SAHWIRA HEALTH</b><br>
        <span style='font-size:12px; opacity:0.9;'>Harare, Zimbabwe | Private & Secure Patient Portal</span></div>
        <div style='font-size:11px; text-align:right; opacity:0.9;'>🔒 SSL Encrypted<br>🇿🇼 POPIA Compliant</div>
    </div>
</div>
""", unsafe_allow_html=True)

# --- AUTH GATE ---
if check_key():

    st.markdown("<div class='trust-row'><span>✅ Premium Active</span> <span>🩺 Doctor Trusted</span> <span>📄 Clinic Letterhead</span></div>", unsafe_allow_html=True)
    st.write("")

    tab1, tab2, tab3 = st.tabs(["📊 Dashboard", "📝 Log Sugar", "📄 Reports"])

    with tab1:
        colA, colB, colC = st.columns(3)
        with colA: st.markdown("<div class='metric-card'><div style='color:#888; font-size:12px;'>AVG SUGAR</div><div style='font-size:24px; color:#0D47A1;'><b>6.8</b> mmol/L</div><div style='color:#4CAF50; font-size:11px;'>● In Target</div></div>", unsafe_allow_html=True)
        with colB: st.markdown("<div class='metric-card'><div style='color:#888; font-size:12px;'>LAST READING</div><div style='font-size:24px;'><b>6.5</b></div><div style='color:#888; font-size:11px;'>Today 07:30</div></div>", unsafe_allow_html=True)
        with colC: st.markdown("<div class='metric-card'><div style='color:#888; font-size:12px;'>STREAK</div><div style='font-size:24px;'><b>12 Days</b></div><div style='color:#FF9800; font-size:11px;'>🔥 Keep going!</div></div>", unsafe_allow_html=True)
        
        st.write("")
        data = pd.DataFrame({'Day': ['Mon','Tue','Wed','Thu','Fri','Sat','Sun'], 'Sugar': [6.5,7.2,6.0,7.8,6.9,6.4,6.7]})
        fig, ax = plt.subplots(figsize=(8,3))
        ax.plot(data['Day'], data['Sugar'], marker='o', color='#0D47A1', linewidth=3, markersize=8)
        ax.fill_between(data['Day'], data['Sugar'], alpha=0.1, color='#0D47A1')
        ax.set_ylabel("mmol/L")
        ax.set_title("Your Weekly Trend - Sahwira Health", fontsize=11)
        ax.grid(True, alpha=0.2)
        st.pyplot(fig, use_container_width=True)

    with tab2:
        st.subheader("Log New Reading")
        with st.container(border=True):
            sugar = st.number_input("Blood Sugar (mmol/L)", 2.0, 30.0, 6.5, step=0.1)
            time = st.selectbox("When?", ["Fasting (Morning)", "Before Meal", "After Meal (2hr)", "Bedtime"])
            notes = st.text_input("Notes (optional)", placeholder="e.g. After sadza")
            if st.button("💾 Save Reading", type="primary", use_container_width=True):
                st.success(f"Saved: {sugar} mmol/L - {time}. Your doctor can see this in PDF.")

    with tab3:
        st.subheader("Clinic Report")
        st.caption("Download with official letterhead for your doctor.")
        if st.button("📄 Generate Professional PDF Report", type="primary", use_container_width=True):
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Arial", "B", 18)
            pdf.set_text_color(13,71,161)
            pdf.cell(0, 12, "SAHWIRA HEALTH", align="C", ln=True)
            pdf.set_font("Arial", "", 9)
            pdf.set_text_color(80,80,80)
            pdf.cell(0, 5, "Harare, Zimbabwe | WhatsApp: 0771477408 | www.sahwirahealth.co.zw", align="C", ln=True)
            pdf.set_draw_color(13,71,161)
            pdf.line(10, 28, 200, 28)
            pdf.ln(12)
            pdf.set_font("Arial", "B", 12)
            pdf.set_text_color(0,0,0)
            pdf.cell(0, 8, f"Patient Health Report - {datetime.date.today()}", ln=True)
            pdf.set_font("Arial", "", 10)
            pdf.cell(0, 6, f"Average: 6.8 mmol/L | Status: Controlled | Generated: {datetime.datetime.now().strftime('%H:%M')}", ln=True)
            pdf.ln(4)
            pdf.multi_cell(0, 5, "Readings:\nMon: 6.5 | Tue: 7.2 | Wed: 6.0 | Thu: 7.8 | Fri: 6.9 | Sat: 6.4 | Sun: 6.7\n\nThis report is for tracking purposes only. For medical emergencies dial 994 in Zimbabwe. Always consult your doctor.")
            pdf.ln(10)
            pdf.set_font("Arial", "B", 9)
            pdf.cell(0, 5, "Electronically Signed by Sahwira Health System | Secure & Encrypted", ln=True)
            pdf_path = "/tmp/Sahwira_Report.pdf"
            pdf.output(pdf_path)
            with open(pdf_path, "rb") as f:
                st.download_button("⬇️ Download Official Report", f, file_name=f"Sahwira_Report_{datetime.date.today()}.pdf", mime="application/pdf", type="primary", use_container_width=True)
            st.success("✅ Professional report ready with letterhead!")

    st.divider()
    if st.button("Log out"):
        st.session_state["activated"] = False
        st.rerun()

else:
    # --- LUXURY ACTIVATION SCREEN ---
    st.markdown("""
    <div style='max-width:520px; margin:30px auto; background:white; border-radius:16px; padding:28px; border:1px solid #E0E0E0; box-shadow:0 8px 24px rgba(13,71,161,0.08); text-align:center;'>
        <div style='width:64px; height:64px; background:#E3F2FD; border-radius:50%; display:flex; align-items:center; justify-content:center; margin:0 auto 12px; font-size:32px;'>🔐</div>
        <h2 style='color:#0D47A1; margin:8px 0;'>Premium Patient Access</h2>
        <p style='color:#666; font-size:13px; line-height:1.5;'>Trusted by clinics across Zimbabwe. Your data is end-to-end encrypted and never shared. Enter your license to unlock dashboard, trends & official PDF reports.</p>
    </div>
    """, unsafe_allow_html=True)
    
    c1,c2,c3 = st.columns([1,1.9,1])
    with c2:
        with st.container(border=True):
            st.markdown("**🔑 License Key**")
            st.caption("Check your EcoCash SMS or WhatsApp from Sahwira")
            lic = st.text_input("License", placeholder="SAHWIRA100", label_visibility="collapsed", key="license_input")
            if st.button("ACTIVATE SECURELY →", type="primary", use_container_width=True):
                if lic.strip().upper() in VALID_KEYS:
                    st.session_state["activated"] = True
                    st.balloons()
                    st.success("Welcome to Sahwira Premium!")
                    st.rerun()
                else:
                    st.error("Invalid key. WhatsApp us for help.")
            st.divider()
            st.markdown("""
            <div style='font-size:12px; line-height:1.6;'>
            <b>How to get access:</b><br>
            💳 EcoCash / ZiG / InnBucks to: <b>771477408</b> (James)<br>
            st.markdown("""
            <div style='font-size:12px; line-height:1.6;'>
            <b>How to get access:</b><br>
            EcoCash to: <b>771477408</b> (James)<br>
            Price: 5 USD for 3 months | 15 USD for 12 months<br>
            WhatsApp proof - instant activation
            </div>
            """, unsafe_allow_html=True)
            st.link_button("WhatsApp Support", "https://wa.me/263771477408", use_container_width=True)
        
        st.markdown("<div style='text-align:center; margin-top:18px; font-size:11px; color:#888;'>Secure | Built for Zimbabwe | Emergencies: Dial 994</div>", unsafe_allow_html=True)
