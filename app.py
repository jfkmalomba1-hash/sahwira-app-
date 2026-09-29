import streamlit as st
import pandas as pd
import datetime
import matplotlib.pyplot as plt
from fpdf import FPDF

try:
    VALID_KEYS = st.secrets["LICENSE_KEYS"]
    ECO_NAME = st.secrets["ECOCASH_NAME"]
    ECO_NUM = st.secrets["ECOCASH_NUMBER"]
except:
    VALID_KEYS = ["SAHWIRA100","SAHWIRA200","SAHWIRA365","CLINIC2026","TEST123","SAHWIRA5","ADMIN2026"]
    ECO_NAME = "James"
    ECO_NUM = "0771477408"

# --- TRANSLATIONS ---
LANG = {
    "English": {
        "title": "SAHWIRA HEALTH", "sub": "Harare, Zimbabwe | Secure Patient Portal",
        "premium_active": "Premium Active - Welcome", "premium_title": "Premium Patient Access",
        "dash": "Dashboard", "log": "Log Sugar", "rep": "Reports",
        "avg": "AVG SUGAR", "last": "LAST READING", "streak": "STREAK",
        "in_target": "In Target", "today": "Today 07:30", "keep": "Keep going",
        "weekly": "Weekly Trend", "blood": "Blood Sugar (mmol/L)", "when": "When?",
        "notes": "Notes", "save": "Save Reading", "saved": "Saved",
        "pdf_btn": "Generate PDF Report", "download": "Download Report",
        "license": "License Key", "activate": "ACTIVATE SECURELY", "invalid": "Invalid key",
        "pay": "EcoCash to: {num} - {name} - 5 USD = 3 months | 15 USD = 12 months",
        "support": "WhatsApp Support", "logout": "Log out"
    },
    "Shona": {
        "title": "SAHWIRA HEALTH", "sub": "Harare, Zimbabwe | Nzvimbo Yakachengeteka",
        "premium_active": "Premium Yabatidzwa - Mauya", "premium_title": "Kupinda Kwevarwere Premium",
        "dash": "Dhibhodhi", "log": "Nyora Shuga", "rep": "Mishumo",
        "avg": "AVHAREJI YESHUGA", "last": "KUYEDZA KWEKUPEDZISIRA", "streak": "MAZUVA AKATEVEDZANA",
        "in_target": "Zvakanaka", "today": "Nhasi 07:30", "keep": "Ramba wakadaro",
        "weekly": "Mafambiro eVhiki", "blood": "Shuga muRopa (mmol/L)", "when": "Rini?",
        "notes": "Manotsi", "save": "Chengetedza", "saved": "Zvachengetedzwa",
        "pdf_btn": "Gadzira Mushumo wePDF", "download": "Dhawunirodha Mushumo",
        "license": "Kiyi yeLayisensi", "activate": "BATIDZA ZVAKACHENGETEKA", "invalid": "Kiyi isiriyo",
        "pay": "EcoCash ku: {num} - {name} - 5 USD = mwedzi 3 | 15 USD = mwedzi 12",
        "support": "Batsiro paWhatsApp", "logout": "Buda"
    },
    "Ndebele": {
        "title": "SAHWIRA HEALTH", "sub": "Harare, Zimbabwe | Indawo Ephephile Yesigulane",
        "premium_active": "Premium Isebenzayo - Siyakwamukela", "premium_title": "Ukungena Kwezigulane Premium",
        "dash": "Ibhodi", "log": "Bhala Ushukela", "rep": "Imibiko",
        "avg": "ISILINGANISO SIKASHUKELA", "last": "UKUHLOLWA KOKUCINA", "streak": "IZINSUKU EZILANDELANAYO",
        "in_target": "Kuhle", "today": "Namuhla 07:30", "keep": "Qhubeka",
        "weekly": "Ukuhamba Kweviki", "blood": "Ushukela Egazini (mmol/L)", "when": "Nini?",
        "notes": "Amanothi", "save": "Gcina", "saved": "Kugcinwe",
        "pdf_btn": "Yenza Umbiko wePDF", "download": "Landa Umbiko",
        "license": "Ukhiye weLayisensi", "activate": "VULA NGOKUPHEPHILE", "invalid": "Ukhiye ongalunganga",
        "pay": "EcoCash ku: {num} - {name} - 5 USD = izinyanga 3 | 15 USD = izinyanga 12",
        "support": "Usizo kuWhatsApp", "logout": "Phuma"
    }
}

st.set_page_config(page_title="Sahwira Health", page_icon="🛡️", layout="wide", initial_sidebar_state="collapsed")
st.markdown("<style>#MainMenu,footer,header,.stDeployButton{visibility:hidden;display:none}</style>", unsafe_allow_html=True)

# Language selector - top right
top1, top2 = st.columns([3,1])
with top2:
    lang_choice = st.selectbox("🌐", ["English","Shona","Ndebele"], label_visibility="collapsed")
t = LANG[lang_choice]

st.markdown(f"""
<div style='background:linear-gradient(135deg,#0D47A1 0%,#1976D2 100%);padding:18px 24px;border-radius:12px;color:white;margin-bottom:20px;'>
<b style='font-size:20px;'>{t['title']}</b><br>
<span style='font-size:12px;'>{t['sub']}</span>
</div>
""", unsafe_allow_html=True)

def check_key():
    if st.session_state.get("activated"): return True
    k = st.session_state.get("license_input","").strip().upper()
    if k in VALID_KEYS:
        st.session_state["activated"]=True
        return True
    return False

if check_key():
    st.success(t['premium_active'])
    tab1, tab2, tab3 = st.tabs([t['dash'], t['log'], t['rep']])
    with tab1:
        c1,c2,c3 = st.columns(3)
        c1.metric(t['avg'], "6.8 mmol/L", t['in_target'])
        c2.metric(t['last'], "6.5", t['today'])
        c3.metric(t['streak'], "12 Days", t['keep'])
        data = pd.DataFrame({'Day':['Mon','Tue','Wed','Thu','Fri','Sat','Sun'], 'Sugar':[6.5,7.2,6.0,7.8,6.9,6.4,6.7]})
        fig, ax = plt.subplots(figsize=(8,3))
        ax.plot(data['Day'], data['Sugar'], marker='o', color='#0D47A1', linewidth=3)
        ax.set_ylabel("mmol/L")
        ax.set_title(t['weekly'])
        ax.grid(True, alpha=0.2)
        st.pyplot(fig, use_container_width=True)
    with tab2:
        with st.container(border=True):
            sugar = st.number_input(t['blood'], 2.0, 30.0, 6.5, step=0.1)
            when = st.selectbox(t['when'], ["Fasting", "Before Meal", "After Meal", "Bedtime"])
            notes = st.text_input(t['notes'])
            if st.button(t['save'], type="primary", use_container_width=True):
                st.success(f"{t['saved']}: {sugar} - {when}")
    with tab3:
        if st.button(t['pdf_btn'], type="primary", use_container_width=True):
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Arial","B",16)
            pdf.cell(0,10,f"SAHWIRA HEALTH - {t['rep']} ({lang_choice})", ln=True, align="C")
            pdf.set_font("Arial","",10)
            pdf.cell(0,8,f"Date: {datetime.date.today()} | Language: {lang_choice}", ln=True)
            pdf.ln(5)
            pdf.multi_cell(0,5,f"EcoCash: {ECO_NUM} - {ECO_NAME}\nReadings: 6.5, 7.2, 6.0, 7.8, 6.9, 6.4, 6.7\nEmergencies: 994")
            path="/tmp/report.pdf"
            pdf.output(path)
            with open(path,"rb") as f:
                st.download_button(t['download'], f, file_name=f"Sahwira_{lang_choice}.pdf", mime="application/pdf", type="primary", use_container_width=True)
    if st.button(t['logout']):
        st.session_state["activated"]=False
        st.rerun()
else:
    st.markdown(f"<h3 style='text-align:center;color:#0D47A1;'>{t['premium_title']}</h3>", unsafe_allow_html=True)
    c1,c2,c3 = st.columns([1,2,1])
    with c2:
        with st.container(border=True):
            st.markdown(f"**{t['license']}**")
            lic = st.text_input("License", placeholder="SAHWIRA100", label_visibility="collapsed", key="license_input")
            if st.button(t['activate'], type="primary", use_container_width=True):
                if lic.strip().upper() in VALID_KEYS:
                    st.session_state["activated"]=True
                    st.balloons()
                    st.rerun()
                else:
                    st.error(t['invalid'])
            st.info(t['pay'].format(num=ECO_NUM, name=ECO_NAME))
            st.link_button(t['support'], "https://wa.me/263771477408", use_container_width=True)
        st.caption("Secure | Harare | Emergencies: 994")
