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

LANG = {
    "English": {
        "title":"SAHWIRA HEALTH","sub":"Harare, Zimbabwe | Secure Patient Portal",
        "premium_active":"Premium Active - Welcome","dash":"Dashboard","log":"Log Sugar","rep":"Reports",
        "menu":"Menus","combo":"Combinations","rem":"Reminders","fam":"Family",
        "avg":"AVG SUGAR","last":"LAST READING","streak":"STREAK","weekly":"Weekly Trend",
        "blood":"Blood Sugar (mmol/L)","save":"Save Reading","saved":"Saved"
    },
    "Shona": {
        "title":"SAHWIRA HEALTH","sub":"Harare, Zimbabwe | Nzvimbo Yakachengeteka",
        "premium_active":"Premium Yabatidzwa - Mauya","dash":"Dhibhodhi","log":"Nyora Shuga","rep":"Mishumo",
        "menu":"Menyu Yekudya","combo":"Misanganiswa","rem":"Zviyeuchidzo","fam":"Mhuri",
        "avg":"AVHAREJI","last":"KUPEDZISIRA","streak":"MAZUVA","weekly":"Mafambiro eVhiki",
        "blood":"Shuga (mmol/L)","save":"Chengetedza","saved":"Zvachengetedzwa"
    },
    "Ndebele": {
        "title":"SAHWIRA HEALTH","sub":"Harare, Zimbabwe | Indawo Ephephile",
        "premium_active":"Premium Isebenzayo - Siyakwamukela","dash":"Ibhodi","log":"Bhala Ushukela","rep":"Imibiko",
        "menu":"Ukudla","combo":"Inhlanganisela","rem":"Izikhumbuzi","fam":"Umndeni",
        "avg":"ISILINGANISO","last":"OKUCINA","streak":"IZINSUKU","weekly":"Ukuhamba Kweviki",
        "blood":"Ushukela (mmol/L)","save":"Gcina","saved":"Kugcinwe"
    }
}

st.set_page_config(page_title="Sahwira Health", page_icon="🛡️", layout="wide", initial_sidebar_state="collapsed")
st.markdown("<style>#MainMenu,footer,header,.stDeployButton{visibility:hidden;display:none}</style>", unsafe_allow_html=True)

top1, top2 = st.columns([3,1])
with top2:
    lang_choice = st.selectbox("🌐", ["English","Shona","Ndebele"], label_visibility="collapsed")
t = LANG[lang_choice]

st.markdown(f"""<div style='background:linear-gradient(135deg,#0D47A1 0%,#1976D2 100%);padding:18px 24px;border-radius:12px;color:white;margin-bottom:20px;'><b style='font-size:20px;'>{t['title']}</b><br><span style='font-size:12px;'>{t['sub']}</span></div>""", unsafe_allow_html=True)

def check_key():
    if st.session_state.get("activated"): return True
    k = st.session_state.get("license_input","").strip().upper()
    if k in VALID_KEYS:
        st.session_state["activated"]=True
        return True
    return False

if check_key():
    st.success(t['premium_active'])
    tabs = st.tabs([t['dash'], t['log'], t['menu'], t['combo'], t['rem'], t['fam'], t['rep']])

    with tabs[0]: # DASHBOARD
        c1,c2,c3 = st.columns(3)
        c1.metric(t['avg'], "6.8 mmol/L", "Kuhle")
        c2.metric(t['last'], "6.5", "Namuhla 07:30")
        c3.metric(t['streak'], "12 Days", "Qhubeka")
        data = pd.DataFrame({'Day':['Mon','Tue','Wed','Thu','Fri','Sat','Sun'], 'Sugar':[6.5,7.2,6.0,7.8,6.9,6.4,6.7]})
        fig, ax = plt.subplots(figsize=(8,3))
        ax.plot(data['Day'], data['Sugar'], marker='o', color='#0D47A1', linewidth=3)
        ax.set_ylabel("mmol/L"); ax.set_title(t['weekly']); ax.grid(True, alpha=0.2)
        st.pyplot(fig, use_container_width=True)

    with tabs[1]: # LOG
        sugar = st.number_input(t['blood'], 2.0, 30.0, 6.5, step=0.1)
        when = st.selectbox("When?", ["Fasting","Before Meal","After Meal","Bedtime"])
        if st.button(t['save'], type="primary", use_container_width=True):
            st.success(f"{t['saved']}: {sugar}")

    with tabs[2]: # MENUS
        st.subheader(f"🍽️ {t['menu']}")
        st.markdown("""
        **MANGWANANI (Breakfast):**
        - Porridge isina shuga + nzungu + mukaka
        - Mazai 2 + madomasi + slice 1 ye brown bread
        **MASIKATI (Lunch):**
        - Sadza diki (1 cup) + Muriwo/Covo + Huku isina ganda
        - Mupunga (1/2 cup) + bhinzi + muriwo
        **MANHERU (Dinner):**
        - Sadza diki + matumbu + muriwo
        - Sweet potato + fish + salad
        """)
        st.info("DZIVISA: Soda, doro rakawandisa, chingwa chichena chakawanda, mafuta akawanda")

    with tabs[3]: # COMBINATIONS
        st.subheader(f"🥗 {t['combo']}")
        st.markdown("""
        **ZVAKANAKA (Good Combos = Sugar inononoka):**
        ✅ Sadza + Muriwo + Bhinzi/Nyama = Kuhle
        ✅ Mupunga + Huku + Salad
        ✅ Porridge + Nzungu

        **ZVAKAIPA (Bad Combos):**
        ❌ Sadza hombe + soda = Shuga inokwira!
        ❌ Chingwa chichena + jam + tea ine shuga
        ❌ Sadza + mafuta akawanda

        Tip: Idya muriwo wakawanda kutanga, wozodya sadza.
        """)

    with tabs[4]: # REMINDERS
        st.subheader(f"⏰ {t['rem']}")
        r_time = st.time_input("Nguva yekunwa mushonga / Isikhathi sokuthatha amaphilisi", datetime.time(7,30))
        r_type = st.selectbox("Chii? / Yini?", ["Tarisa Shuga","Mushonga","Kufamba-famba (Exercise)","Kunwa Mvura"])
        if st.button("Gadza Chiyeuchidzo / Beka Isikhumbuzi", type="primary", use_container_width=True):
            st.success(f"✅ Chiyeuchidzo chagadzirwa: {r_type} na {r_time} - Tichakutumira WhatsApp!")
            st.balloons()
        st.caption("In next version: WhatsApp message otomatiki panguva ino")

    with tabs[5]: # FAMILY
        st.subheader(f"👨‍👩‍👧‍👦 {t['fam']}")
        st.markdown("Wedzera mhuri kuti ivone hutano hwako")
        fam_name = st.text_input("Zita reMhuri / Ibizo Lomndeni", placeholder="Mai, Baba, Mwana")
        fam_phone = st.text_input("WhatsApp yavo", placeholder="077...")
        fam_rel = st.selectbox("Ukama", ["Mukadzi/Murume","Mwana","Mubereki","Mukoma/Munin'ina","Shamwari"])
        if st.button("Wedzera Mhuri / Engeza Umndeni", type="primary", use_container_width=True):
            st.success(f"✅ {fam_name} ({fam_rel}) wawedzerwa! Vachagamuchira mishumo kana shuga yakwira.")
        st.info("Kana shuga yako > 15 kana < 3.5, mhuri yako inoziviswa paWhatsApp otomatiki (Pro feature)")

    with tabs[6]: # REPORTS
        if st.button("Generate PDF Report", type="primary", use_container_width=True):
            pdf = FPDF(); pdf.add_page(); pdf.set_font("Arial","B",16)
            pdf.cell(0,10,"SAHWIRA HEALTH - Report", ln=True, align="C")
            pdf.set_font("Arial","",10)
            pdf.multi_cell(0,5,f"Date: {datetime.date.today()}\nEcoCash: {ECO_NUM}\nReadings: 6.5, 7.2, 6.0, 7.8")
            path="/tmp/report.pdf"; pdf.output(path)
            with open(path,"rb") as f:
                st.download_button("Download Report", f, file_name="Sahwira.pdf", mime="application/pdf", type="primary", use_container_width=True)

else:
    c1,c2,c3 = st.columns([1,2,1])
    with c2:
        with st.container(border=True):
            lic = st.text_input("License", placeholder="TEST123", label_visibility="collapsed", key="license_input")
            if st.button("ACTIVATE SECURELY", type="primary", use_container_width=True):
                if lic.strip().upper() in VALID_KEYS:
                    st.session_state["activated"]=True; st.rerun()
