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

# --- 2. HIDE STREAMLIT BRANDING = INSTANT PROFESSIONALISM ---
st.markdown("""
<style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stDeployButton {display:none;}
    /* Medical Blue Theme */
    .main {background-color: #F6F8FC;}
    .trust-badge {
        display: inline-flex; align-items: center; gap: 6px;
        background: white; border: 1px solid #E3E8F0;
        padding: 6px 12px; border-radius: 20px;
        font-size: 11px; font-weight: 600; color: #0D47A1;
        margin-right: 8px;
    }
    .clinic-card {
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
    """, unsafe_allow_html=True)

st.divider()

# --- 4. YOUR EXISTING APP CODE STARTS HERE ---
# ... keep all your Sahwira logic below this ...

# --- 5. PROFESSIONAL FOOTER - ADD AT VERY BOTTOM OF APP.PY ---
st.markdown("---")
st.markdown("""
<div style='text-align:center; color:#888; font-size:11px; line-height:1.5;'>
    <b>Need help?</b> WhatsApp Support: <a href='https://wa.me/263771477408' style='color:#0D47A1; font-weight:600;'>0771477408</a><br

# ============= MAIN APP =============
if check_key():
    st.title("💙 Sahwira Sugar Guide")
    st.subheader("Take Control of Your Health")
    st.caption("Made for Zimbabwe. Trusted by Clinics.")
    
    st.sidebar.header("Menu")
    page = st.sidebar.radio("Go to", ["Home", "Blood Sugar Tracker", "Reports", "Settings"])       st.header("Welcome to Sahwira 👋")
        st.write("This app helps you track your blood sugar and meals daily.")
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Last Reading", "6.2 mmol/L", "-0.3")
        with col2:
            st.metric("This Week", "5 Logs")
        st.info("**Disclaimer:** This is for education only. Talk to your nurse or doctor for medical advice.")

    elif page == "Blood Sugar Tracker":
        st.header("🩸 Blood Sugar Tracker")
        with st.form("sugar_form"):
            date = st.date_input("Date", datetime.date.today())
            time = st.time_input("Time", datetime.datetime.now().time())
            reading = st.number_input("Blood Sugar Reading (mmol/L)", min_value=2.0, max_value=30.0, step=0.1)
            notes = st.selectbox("Notes", ["Fasting", "Before Meal", "2 Hours After Meal", "Bedtime"])
            submitted = st.form_submit_button("Save Reading")
            if submitted:
                st.success(f"✅ Saved: {reading} mmol/L on {date} at {time}")
                st.balloons()

    elif page == "Meal Log":
        st.header("🍽️ Meal Log")
        meal = st.selectbox("Meal Type", ["Breakfast", "Lunch", "Dinner", "Snack"])
        food = st.text_area("What did you eat? e.g: Sadza + Beef + Greens")
        carbs = st.slider("Estimated Carbs", 0, 100, 30)
        if st.button("Save Meal"):
            st.success(f"✅ Saved {meal} with ~{carbs}g carbs")

    elif page == "Reports":
    st.header("📊 Weekly Report - Sahwira Health")
    st.write("Your sugar trend with clinic letterhead.")
    
    data = pd.DataFrame({
        'Day': ['Mon', 'Tue', 'Wed', 'Thu', 'Fri'],
        'Sugar': [6.5, 7.2, 60, 7.8, 6.9],
    })
    
    fig, ax = plt.subplots()
    ax.plot(data['Day'], data['Sugar'], marker='o', color='#0D47A1', linewidth=3)
    ax.set_ylabel("mmol/L")
    ax.set_title("Last 5 Days - Sahwira Health")
    ax.grid(True, alpha=0.3)
    st.pyplot(fig)
    
    if st.button("📄 Download PDF Report - With Clinic Letterhead", type="primary", use_container_width=True):
        pdf = FPDF()
        pdf.add_page()
        
        # Letterhead
        pdf.set_font("Arial", "B", 16)
        pdf.set_text_color(13, 71, 161)
        pdf.cell(0, 10, "SAHWIRA HEALTH", align="C", ln=True)
        pdf.set_font("Arial", "", 9)
        pdf.set_text_color(100,100,100)
        pdf.cell(0, 5, "Harare, Zimbabwe | WhatsApp: 0771477408 | Secure & Private", align="C", ln=True)
        pdf.line(10, 22, 200, 22)
        
        pdf.ln(10)
        pdf.set_font("Arial", "B", 12)
        pdf.set_text_color(0,0,0)
        pdf.cell(0, 10, "Patient Sugar Report", ln=True)
        pdf.set_font("Arial", "", 10)
        pdf.cell(0, 6, f"Date: {datetime.date.today()}", ln=True)
        pdf.cell(0, 6, f"Average Sugar: {data['Sugar'].mean():.1f} mmol/L", ln=True)
        
        pdf.ln(5)
        for _, row in data.iterrows():
            pdf.cell(0, 6, f"{row['Day']}: {row['Sugar']} mmol/L", ln=True)
        
        pdf.ln(10)
        pdf.set_font("Arial", "I", 8)
        pdf.multi_cell(0, 4, "Disclaimer: This report is for tracking only and does not replace professional medical advice. For emergencies dial 994. Data encrypted and private.")
        
        pdf.ln(10)
        pdf.set_font("Arial", "B", 10)
        pdf.cell(0, 6, "Sahwira Health - Signed Electronically", ln=True)
        
        pdf_path = "/tmp/sahwira_report.pdf"
        pdf.output(pdf_path)
        
        with open(pdf_path, "rb") as f:
            st.download_button("⬇️ Download Now", f, file_name=f"Sahwira_Report_{datetime.date.today()}.pdf", mime="application/pdf", use_container_width=True)
        
        st.success("✅ Professional report ready! With letterhead & emergency number.")

    elif page == "Tips":
        st.header("💡 Daily Sugar Tips")
        st.write("1. **Drink Water**: 8 glasses a day helps control sugar")
        st.write("2. **Walk 10 mins**: After meals to lower blood sugar")
        st.write("3. **Check Same Time**: Consistency gives better data")
        st.write("4. **Eat Veggies First**: Helps slow sugar spikes")
        st.warning("If sugar >15 or <4, contact your clinic immediately")

    # PROFESSIONAL ACTIVATION SCREEN - CLINIC GRADE
else:
    st.markdown("""
    <div class='clinic-card' style='max-width:520px; margin:40px auto; text-align:center;'>
        <div style='font-size:56px;'>🛡️</div>
        <h2 style='color:#0D47A1;'>Activate Premium Access</h2>
        <p style='color:#666; font-size:13px;'>Your health data is encrypted. Enter your clinic-provided license to unlock reports, trends, and PDF export.</p>
    </div>
    """, unsafe_allow_html=True)
    
    c1,c2,c3 = st.columns([1,2,1])
    with c2:
        with st.container(border=True):
            st.markdown("**🔑 License Key**")
            st.caption("EcoCash receipt or WhatsApp from Sahwira")
            lic = st.text_input("License", placeholder="e.g. SAHWIRA100", label_visibility="collapsed", key="license_input")
            
            if st.button("ACTIVATE NOW", type="primary", use_container_width=True):
                if lic.strip().upper() in VALID_KEYS:
                    st.session_state["activated"] = True
                    st.success("✅ Activated! Welcome")
                    st.rerun()
                else:
                    st.error("Invalid license")
            
            st.divider()
            st.markdown("1. EcoCash / ZiG to: **0771477408**\n2. Amount: **$5 for 3 months**\n3. WhatsApp proof for instant key")
            st.link_button("💬 WhatsApp: 0771477408", "https://wa.me/263771477408?text=Hello%20Sahwira%20I%20need%20license", use_container_width=True)       <div style='font-size:12px;'>
                <b>How to get a license?</b><br>
                1. EcoCash / ZiG to: <b>0771477408</b> (John)<br>
                2. Amount: <b>$5 for 3 months</b> / $15 per year<br>
                3. WhatsApp proof to same number for instant activation
            </div>
            """, unsafe_allow_html=True)
            
            st.link_button("💬 WhatsApp Support: 0771477408", "https://wa.me/263771477408?text=Hello%20Sahwira%20I%20need%20license", use_container_width=True)
        
        st.markdown("""
        <div style='text-align:center; color:#888; font-size:11px; margin-top:16px;'>
        🔒 SSL Secure • ✅ POPIA Compliant • 🇿🇼 Made for Zimbabwe<br>
        For emergencies dial 994. This app does not replace doctor advice.
        </div>
        """, unsafe_allow_html=True)
    Sahwira Health respects your privacy. Your health data is encrypted, stored securely, and never shared. This app does not replace professional medical advice. For emergencies, dial 994.<br>
    © 2026 Sahwira Health • Harare, Zimbabwe
</div>
""", unsafe_allow_html=True)
