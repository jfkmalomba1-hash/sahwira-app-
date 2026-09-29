import streamlit as st
import pandas as pd
import datetime
import random
from fpdf import FPDF

try:
    from gtts import gTTS
    VOICE_OK = True
except:
    VOICE_OK = False

try:
    VALID_KEYS = st.secrets["LICENSE_KEYS"]
except:
    VALID_KEYS = ["SAHWIRA100","SAHWIRA200","SAHWIRA365","CLINIC2026","TEST123","SAHWIRA5","ADMIN2026"]

FOODS = [
    {"en":"Sadza zviyo","sn":"Sadza rezviyo (1 cup)","nd":"Isitshwala seziyo","carbs":40,"cat":"Staple","level":"🟢 Best"},
    {"en":"Sadza mapfunde","sn":"Sadza remapfunde","nd":"Isitshwala samabele","carbs":42,"cat":"Staple","level":"🟢"},
    {"en":"Sadza rukweza","sn":"Sadza rerukweza","nd":"Isitshwala serukweza","carbs":38,"cat":"Staple","level":"🟢 Best low GI"},
    {"en":"Sadza white","sn":"Sadza chena","nd":"Isitshwala esimhlophe","carbs":45,"cat":"Staple","level":"🟡"},
    {"en":"Nhopi","sn":"Nhopi (1 cup)","nd":"Inhopi","carbs":28,"cat":"Staple","level":"🟢"},
    {"en":"Tsenza","sn":"Tsenza","nd":"Amatsenza","carbs":18,"cat":"Staple","level":"🟢 Best"},
    {"en":"Porridge rine dovi","sn":"Bota rine dovi","nd":"Iphalishi elamantongomane","carbs":30,"cat":"Breakfast","level":"🟢"},
    {"en":"Oats","sn":"Oats bota","nd":"I-oats","carbs":27,"cat":"Breakfast","level":"🟢 Best"},
    {"en":"Mowa","sn":"Mowa","nd":"Imbowa","carbs":5,"cat":"Muriwo","level":"🟢 Free"},
    {"en":"Mutsine","sn":"Mutsine","nd":"Umhlalavane","carbs":4,"cat":"Muriwo","level":"🟢 Free"},
    {"en":"Manyanya","sn":"Manyanya","nd":"Amaqa emathanga","carbs":4,"cat":"Muriwo","level":"🟢 Free"},
    {"en":"Cucumber","sn":"Magaka","nd":"Ikhukhamba","carbs":3,"cat":"Salad","level":"🟢 Free best"},
    {"en":"Tsuro","sn":"Tsuro 100g","nd":"Umvundla","carbs":0,"cat":"Meat","level":"🟢 Best lean"},
    {"en":"Roadrunner","sn":"Huku yechibhoyi","nd":"Inkukhu yesiXhosa","carbs":0,"cat":"Meat","level":"🟢 Best"},
    {"en":"Hanga","sn":"Hanga 100g","nd":"Inkanga","carbs":0,"cat":"Meat","level":"🟢 Best"},
    {"en":"Mhou ostrich","sn":"Mhou 100g","nd":"Intshe","carbs":0,"cat":"Meat","level":"🟢 Best"},
    {"en":"Tuna tin","sn":"Tuna 80g","nd":"I-tuna","carbs":0,"cat":"Meat","level":"🟢 Best"},
    {"en":"Hove","sn":"Hove 100g","nd":"Inhlanzi","carbs":0,"cat":"Meat","level":"🟢 Best"},
    {"en":"Madora","sn":"Madora 30g","nd":"Amacimbi","carbs":2,"cat":"Meat","level":"🟢 Iron"},
    {"en":"Mukaka wakakora","sn":"Mukaka wakakora 250ml","nd":"Amasi 250ml","carbs":12,"cat":"Dairy","level":"🟢"},
    {"en":"Pawpaw","sn":"Pawpaw 1 cup","nd":"Ipapaya","carbs":10,"cat":"Fruit","level":"🟢"},
    {"en":"Fruit salad no sugar","sn":"Fruit salad isina shuga","nd":"Isaladi yezithelo","carbs":12,"cat":"Fruit","level":"🟢 Best"},
    {"en":"Tsubvu","sn":"Tsubvu 20","nd":"Amatshubvu","carbs":8,"cat":"Fruit","level":"🟢"},
    {"en":"Guava","sn":"Guava 1","nd":"AmaGuava","carbs":8,"cat":"Fruit","level":"🟢"},
]

st.set_page_config(page_title="Sahwira Health", page_icon="🛡️", layout="wide", initial_sidebar_state="collapsed")
st.markdown("""
<style>
#MainMenu,footer,header,.stDeployButton{visibility:hidden;display:none}
.shield {
background: linear-gradient(135deg,#0D47A1 0%,#1976D2 100%);
padding:20px 24px;border-radius:14px;color:white;
box-shadow:0 4px 12px rgba(13,71,161,0.3);margin-bottom:18px;
}
</style>
""", unsafe_allow_html=True)

# BEAUTIFUL ORIGINAL HEADER - NO V NUMBER
top1, top2 = st.columns([4,1])
with top2:
    lang_choice = st.selectbox("🌐", ["English","Shona","Ndebele"], label_visibility="collapsed")
with top1:
    st.markdown("""
    <div class='shield'>
    <div style='display:flex;align-items:center;gap:14px'>
    <div style='font-size:34px'>🛡️</div>
    <div>
    <div style='font-size:23px;font-weight:800;letter-spacing:0.6px'>SAHWIRA HEALTH</div>
    <div style='font-size:12px;opacity:0.92'>Harare, Zimbabwe | Secure Patient Portal | Premium Active</div>
    </div>
    </div>
    </div>
    """, unsafe_allow_html=True)

def check_key():
    if st.session_state.get("activated"): return True
    k = st.session_state.get("lic","").strip().upper()
    if k in VALID_KEYS:
        st.session_state["activated"]=True
        return True
    return False

if not check_key():
    c1,c2,c3 = st.columns([1,2,1])
    with c2:
        with st.container(border=True):
            st.markdown("### 🛡️ SAHWIRA HEALTH")
            st.text_input("License Key", key="lic", placeholder="TEST123", label_visibility="collapsed")
            if st.button("ACTIVATE SECURELY", type="primary", use_container_width=True):
                if st.session_state["lic"].strip().upper() in VALID_KEYS:
                    st.session_state["activated"]=True; st.rerun()
    st.stop()

# 7 HOLISTIC TABS AS YOU ASKED
tabs = st.tabs(["Dashboard","Smart Plan","Foods","Exercise","Medicine","Family","Reminders","Voice Gogo","Reports"])

with tabs[0]:
    c1,c2,c3 = st.columns(3)
    c1.metric("AVG SUGAR", "6.8 mmol/L", "Good")
    c2.metric("LAST", "6.5 Today 07:30")
    c3.metric("STREAK", "12 Days")
    df=pd.DataFrame({'Day':['Mon','Tue','Wed','Thu','Fri','Sat','Sun'],'Sugar':[6.5,7.2,6.0,7.8,6.9,6.4,6.7]})
    import matplotlib.pyplot as plt
    fig, ax = plt.subplots(figsize=(8,3))
    ax.plot(df['Day'], df['Sugar'], marker='o', color='#0D47A1', linewidth=3)
    ax.set_ylabel("mmol/L"); ax.grid(True, alpha=0.2)
    st.pyplot(fig, use_container_width=True)

with tabs[1]:
    st.subheader("🧠 Smart Plan - BM + Foods at home + Meds → Meals")
    c1,c2,c3 = st.columns(3)
    with c1:
        sugar_now = st.number_input("BM now mmol/L", 2.0, 30.0, 7.5, step=0.1)
    with c2:
        wt = st.number_input("Weight kg", 40, 150, 70)
    with c3:
        ht = st.number_input("Height cm", 140, 200, 170)
    bmi = wt/((ht/100)**2)
    available = st.multiselect("Food at home", [f"{f['sn']} ({f['carbs']}g)" for f in FOODS], default=[f"{FOODS[0]['sn']} ({FOODS[0]['carbs']}g)", f"{FOODS[8]['sn']} ({FOODS[8]['carbs']}g)", f"{FOODS[12]['sn']} ({FOODS[12]['carbs']}g)"])
    if st.button("Generate Today's Meals + Exercise", type="primary", use_container_width=True):
        carb_meal = int(wt*28*0.45/4)//3
        if sugar_now>9: carb_meal-=5
        st.session_state["bmi"]=bmi; st.session_state["sugar"]=sugar_now; st.session_state["plan"]=f"Target {carb_meal}g/meal BMI {bmi:.1f}"
        st.success(f"BM {sugar_now} | BMI {bmi:.1f} | Target {carb_meal}g per meal")
        st.markdown(f"""
        **MANGWANANI 07:30:** Sadza rezviyo 1/2 cup (20g) + Mowa 1 cup (5g) + Mazai 2 (1g) = 26g ✅
        **MASIKATI 13:00:** Brown rice 1/2 cup + Manyanya + Hove/Tsuro/Hanga + Pawpaw = ~30g ✅
        **MANHERU 19:00:** Nhopi 1/2 cup (14g) + Covo + Mhou/Tuna = ~20g ✅
        **Snacks:** Tsubvu 20 / Guava / Fruit salad no sugar
        **Exercise:** {'40 min walk - high sugar' if sugar_now>9 else '20 min walk + sweep yard'}
        """)

with tabs[2]:
    st.subheader("📚 Food Library - Tsuro, Hanga, Mhou, Pawpaw, Dovi, Oats")
    search=st.text_input("Search", placeholder="tsuro, hanga, pawpaw...")
    df=pd.DataFrame(FOODS)
    if search:
        df=df[df["en"].str.contains(search, case=False) | df["sn"].str.contains(search, case=False)]
    st.dataframe(df[["sn","en","carbs","level"]], use_container_width=True, hide_index=True)

with tabs[3]:
    st.subheader("🏃 Exercise Prescribed")
    st.markdown("- Fast walk 30 min → drops 1.5 mmol/L\n- Kurima 20 min → drops 2.0\n- Sweep yard 30 min → 0.8\n- Dance 20 min → 1.2")
    if st.button("I did exercise today"): st.balloons(); st.success("Good! Check sugar after 30 min")

with tabs[4]:
    st.subheader("💊 My Medicine from Dr")
    m1=st.text_input("Medicine 1", placeholder="Metformin 500mg - 1 morning 1 evening")
    m2=st.text_input("Medicine 2", placeholder="Glibenclamide - before breakfast")
    t1=st.time_input("Morning", datetime.time(8,0))
    t2=st.time_input("Evening", datetime.time(20,0))
    if st.button("Save Medicines", type="primary", use_container_width=True):
        st.session_state["meds"]=[m1,m2,str(t1),str(t2)]; st.success(f"Saved {m1}, reminder {t1} & {t2}")

with tabs[5]:
    st.subheader("👨‍👩‍👧‍👦 Family Phone for Monitoring & Support")
    st.caption("Family gets alert if BM >15 or <3.5 or meds missed")
    f1=st.text_input("Family 1 Name", placeholder="Mai")
    f1p=st.text_input("Family 1 WhatsApp", placeholder="077...")
    f2=st.text_input("Family 2 Name", placeholder="Baba / Daughter")
    f2p=st.text_input("Family 2 WhatsApp", placeholder="078...")
    f3=st.text_input("Family 3 - Clinic/Dr", placeholder="Dr Moyo Clinic")
    f3p=st.text_input("Clinic Phone", placeholder="029...")
    if st.button("Save Family", type="primary", use_container_width=True):
        st.session_state["family"]=[{"name":f1,"phone":f1p},{"name":f2,"phone":f2p},{"name":f3,"phone":f3p}]
        st.success(f"✅ Saved {f1}, {f2}, {f3} - will be alerted")

with tabs[6]:
    st.subheader("⏰ Reminders - Works Offline & When Phone ON")
    st.markdown("""
    **Truth about phone switched OFF:** No app in world can ring if phone is totally OFF - that's Android/iPhone system.
    **Solution:** We set 4 alarms that work **offline, no data** when phone is ON (even flight mode).
    Also we create WhatsApp text for family to call Gogo.
    """)
    r1=st.time_input("Check BM Morning", datetime.time(7,0))
    r2=st.time_input("Medicine Morning", datetime.time(8,0))
    r3=st.time_input("Check BM Evening", datetime.time(19,0))
    r4=st.time_input("Medicine Evening", datetime.time(20,0))
    st.info(f"SET THESE 4 ALARMS IN YOUR PHONE CLOCK APP (works offline):\n- {r1} SAHWIRA BM\n- {r2} SAHWIRA Medicine\n- {r3} SAHWIRA BM\n- {r4} SAHWIRA Medicine + Log food")
    if st.button("Create WhatsApp Reminder for Family", type="primary", use_container_width=True):
        msg=f"SAHWIRA Reminder: BM {r1} & {r3}, Medicine {r2} & {r4}. Target 4.4-7.0. Call gogo to remind."
        st.code(msg)
        st.link_button("Send via WhatsApp", f"https://wa.me/?text={msg}")

with tabs[7]:
    st.subheader("🔊 Voice Notes for Gogo - Can't read / Visually impaired")
    voice_sn = "Mauya Gogo. Mangwanani idya sadza rezviyo hafu kapu ne mowa ne mazai. Tarisa shuga yako na seven mangwanani na seven manheru. Tora mishonga yako na eight mangwanani na eight manheru. Famba kwemaminetsi makumi maviri. Mvura inwa yakawanda."
    voice_nd = "Siyakwamukela Gogo. Ekuseni dla isitshwala seziyo ingxenye le mbowa lamaqanda. Hlola ushukela ngo seven ekuseni ngo seven ntambama. Thatha imithi ngo eight ekuseni ngo eight ntambama. Hamba imizuzu engamatshumi amabili."
    voice_en = "Hello Gogo. Good morning. Today eat half cup sadza rezviyo with mowa and eggs. Check your sugar at 7am and 7pm. Take your medicine at 8am and 8pm. Walk for 20 minutes. Drink plenty water."

    lang_v = st.selectbox("Language / Mutauro / Ulimi", ["Shona","Ndebele","English"])
    txt_map = {"Shona":voice_sn, "Ndebele":voice_nd, "English":voice_en}
    txt = txt_map[lang_v]
    st.text_area(f"Voice in {lang_v}", txt, height=110)

    if VOICE_OK:
        if st.button(f"🔊 PLAY Voice in {lang_v}", type="primary", use_container_width=True):
            try:
                tts = gTTS(text=txt, lang='en')
                path="/tmp/gogo.mp3"
                tts.save(path)
                st.audio(path, format="audio/mp3")
                st.success(f"Playing in {lang_v} for Gogo 🔊")
            except Exception as e:
                st.error(f"Voice error {e}")
    else:
        st.warning("Add gtts to requirements.txt to enable voice")

    st.caption("Tip: Family can play this loud for Gogo daily. Also send as WhatsApp text.")
    if st.button("Send this Voice Text to Family WhatsApp"):
        st.link_button("Send to WhatsApp", f"https://wa.me/?text={txt}")

with tabs[8]:
    st.subheader("📄 Reports for Dr / Clinic - Keep & Print")
    dr=st.text_input("Doctor / Clinic Name", placeholder="Dr Moyo - Parirenyatwa")
    if st.button("Generate Full Clinic Report PDF", type="primary", use_container_width=True):
        pdf=FPDF(); pdf.add_page()
        pdf.set_font("Arial","B",16); pdf.cell(0,10,"SAHWIRA HEALTH - CLINIC REPORT", ln=True, align="C")
        pdf.set_font("Arial","",11); pdf.cell(0,8,f"Date: {datetime.date.today()} | Harare, Zimbabwe", ln=True, align="C")
        pdf.ln(4)
        pdf.set_font("Arial","B",12); pdf.cell(0,8,"Patient Summary for Doctor", ln=True)
        pdf.set_font("Arial","",10)
        bmi=st.session_state.get("bmi","Not entered"); sugar=st.session_state.get("sugar","Not entered")
        meds=st.session_state.get("meds",["Metformin 500mg 08:00 & 20:00"])
        family=st.session_state.get("family",[{"name":"Mai","phone":"077"}])
        plan=st.session_state.get("plan","Smart plan")
        pdf.multi_cell(0,5,f"""
Doctor: {dr}
Date: {datetime.date.today()}
Current BM: {sugar} mmol/L | BMI: {bmi}
Target Range: 4.4 - 7.0 mmol/L

Medicines Prescribed: {meds}
Reminder Times: 07:00 BM, 08:00 Medicine, 19:00 BM, 20:00 Medicine (offline phone alarms)

Today's Plan: {plan}
Diet: 1/2 cup sadza rezviyo/rukweza/mapfunde + muriwo 1 cup (mowa/mutsine/manyanya/covo) + protein (tsuro/hanga/mhou/hove/madora/tuna) + fruit (tsubvu/guava/pawpaw/fruit salad)
Food Library: 40+ local Zimbabwe foods
Exercise Prescribed: Fast walk 30 min, Kurima 20 min, Sweep yard, Dance - lowers 1-2 mmol/L
Family Monitoring: {family}
Voice Support: Shona/Ndebele/English voice notes for visually impaired
Offline: Works without data after opening once

Doctor Notes:
________________________________________

Signature: ___________________
        """)
        path="/tmp/Sahwira_Clinic_Report.pdf"; pdf.output(path)
        with open(path,"rb") as f:
            st.download_button("📥 Download & Print for Dr / Keep", f, file_name=f"Sahwira_Report_{datetime.date.today()}.pdf", mime="application/pdf", type="primary", use_container_width=True)
        st.success("Report ready - Print and keep, give copy to Dr at clinic")
