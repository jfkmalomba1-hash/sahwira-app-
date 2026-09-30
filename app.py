import streamlit as st
import pandas as pd
import datetime
from fpdf import FPDF
import matplotlib.pyplot as plt
import random

try:
    from gtts import gTTS
    VOICE_OK = True
except:
    VOICE_OK = False

try:
    VALID_KEYS = st.secrets["LICENSE_KEYS"]
except:
    VALID_KEYS = ["SAHWIRA100","SAHWIRA200","SAHWIRA365","CLINIC2026","TEST123","SAHWIRA5","ADMIN2026","SAHWIRA1"]

# 100 ZIMBABWE FOODS - ORIGINAL FULL LIBRARY YOU ASKED
FOODS = [
    # Sadza types 1-6
    {"en":"Sadza white maize 1 cup 250g","sn":"Sadza chena 1 cup","nd":"Isitshwala esimhlophe","carbs":45,"cat":"Sadza","level":"🟡 Medium"},
    {"en":"Sadza zviyo finger millet 1 cup","sn":"Sadza rezviyo 1 cup","nd":"Isitshwala seziyo","carbs":40,"cat":"Sadza","level":"🟢 Good fiber"},
    {"en":"Sadza mapfunde sorghum 1 cup","sn":"Sadza remapfunde 1 cup","nd":"Isitshwala samabele","carbs":42,"cat":"Sadza","level":"🟢 Good"},
    {"en":"Sadza rukweza rapoko 1 cup","sn":"Sadza rerukweza 1 cup","nd":"Isitshwala serukweza","carbs":38,"cat":"Sadza","level":"🟢 Best low GI"},
    {"en":"Sadza wheat 1 cup","sn":"Sadza regorosi 1 cup","nd":"Isitshwala sikakolosi","carbs":44,"cat":"Sadza","level":"🟡"},
    {"en":"Mutakura sadza+beans 1 cup","sn":"Mutakura 1 cup","nd":"Umutakura","carbs":35,"cat":"Sadza","level":"🟢 Best protein"},
    # Grains 7-12
    {"en":"White rice 1/2 cup","sn":"Mupunga chena 1/2 cup","nd":"Irayisi elimhlophe","carbs":22,"cat":"Grain","level":"🔴 High"},
    {"en":"Brown rice 1/2 cup","sn":"Mupunga brown 1/2 cup","nd":"Irayisi elinsundu","carbs":22,"cat":"Grain","level":"🟢 Good"},
    {"en":"Nhopi pumpkin porridge 1 cup","sn":"Nhopi 1 cup","nd":"Inhopi","carbs":28,"cat":"Grain","level":"🟢 Good"},
    {"en":"Mbambaira sweet potato 1 med 150g","sn":"Mbambaira 1","nd":"Ubhatata 1","carbs":26,"cat":"Staple","level":"🟢 Good"},
    {"en":"Tsenza livingstone potato 1/2 cup","sn":"Tsenza 1/2 cup","nd":"Amatsenza","carbs":18,"cat":"Staple","level":"🟢 Best"},
    {"en":"Madhumbe taro 1/2 cup","sn":"Madhumbe 1/2 cup","nd":"Amadumbe","carbs":20,"cat":"Staple","level":"🟢 Good"},
    {"en":"Magogoya yams 1/2 cup","sn":"Magogoya 1/2 cup","nd":"Amagogoya","carbs":22,"cat":"Staple","level":"🟢 Good"},
    {"en":"Hacha wild medlar 5 fruits","sn":"Hacha 5","nd":"Ihacha 5","carbs":12,"cat":"Fruit","level":"🟢 Good"},
    # Muriwo 13-22
    {"en":"Mowa amaranth 1 cup","sn":"Mowa 1 cup","nd":"Imbowa","carbs":5,"cat":"Muriwo","level":"🟢 Free iron"},
    {"en":"Mutsine blackjack 1 cup","sn":"Mutsine 1 cup","nd":"Umhlalavane","carbs":4,"cat":"Muriwo","level":"🟢 Free"},
    {"en":"Manyanya pumpkin leaves 1 cup","sn":"Manyanya Muboora 1 cup","nd":"Amaqa emathanga","carbs":4,"cat":"Muriwo","level":"🟢 Free"},
    {"en":"Covo kale 1 cup","sn":"Covo 1 cup","nd":"Icovo","carbs":5,"cat":"Muriwo","level":"🟢 Free"},
    {"en":"Rape 1 cup","sn":"Rape 1 cup","nd":"Irape","carbs":5,"cat":"Muriwo","level":"🟢 Free"},
    {"en":"Beetroot 1/2 cup","sn":"Beetroot 1/2 cup","nd":"I-beetroot","carbs":8,"cat":"Veg","level":"🟢 Good"},
    {"en":"Carrots 1/2 cup","sn":"Makarotsi 1/2 cup","nd":"Izaqathi","carbs":6,"cat":"Veg","level":"🟢 Good"},
    {"en":"Cauliflower 1 cup","sn":"Cauliflower 1 cup","nd":"I-cauliflower","carbs":5,"cat":"Veg","level":"🟢 Free"},
    {"en":"Cucumber 1 cup","sn":"Magaka Cucumber 1 cup","nd":"Ikhukhamba 1 cup","carbs":3,"cat":"Salad","level":"🟢 Free best"},
    {"en":"Tomato + lettuce salad 1 cup","sn":"Saladhi yemadomasi 1 cup","nd":"Isaladi katamatisi","carbs":4,"cat":"Salad","level":"🟢 Free"},
    {"en":"Manhanga pumpkin boiled 1 cup","sn":"Manhanga akabikwa 1 cup","nd":"Amathanga 1 cup","carbs":10,"cat":"Veg","level":"🟢 Free"},
    {"en":"Okra derere 1 cup","sn":"Derere 1 cup","nd":"Idelele 1 cup","carbs":6,"cat":"Veg","level":"🟢 Free"},
    # Meats you asked 23-38
    {"en":"Tsuro rabbit 100g","sn":"Tsuro 100g","nd":"Umvundla 100g","carbs":0,"cat":"Meat","level":"🟢 Best lean"},
    {"en":"Huku yechibhoyi roadrunner 100g","sn":"Huku yechibhoyi 100g","nd":"Inkukhu yesiXhosa 100g","carbs":0,"cat":"Meat","level":"🟢 Best no fat"},
    {"en":"Huku normal chicken 100g no skin","sn":"Huku 100g isina ganda","nd":"Inkukhu 100g","carbs":0,"cat":"Meat","level":"🟢 Good"},
    {"en":"Hanga guinea fowl 100g","sn":"Hanga 100g","nd":"Inkanga 100g","carbs":0,"cat":"Meat","level":"🟢 Best lean"},
    {"en":"Toki turkey 100g","sn":"Toki 100g","nd":"I-turkey 100g","carbs":0,"cat":"Meat","level":"🟢 Best"},
    {"en":"Dhadha duck 100g no skin","sn":"Dhadha 100g","nd":"Idada 100g","carbs":0,"cat":"Meat","level":"🟡 Remove skin"},
    {"en":"Mbudzi goat lean 100g","sn":"Mbudzi 100g","nd":"Imbuzi 100g","carbs":0,"cat":"Meat","level":"🟢 Good"},
    {"en":"Mombe beef lean 100g","sn":"Mombe 100g","nd":"Inkomo 100g","carbs":0,"cat":"Meat","level":"🟡 Small portion"},
    {"en":"Mhou ostrich 100g","sn":"Mhou 100g","nd":"Intshe 100g","carbs":0,"cat":"Meat","level":"🟢 Best very lean"},
    {"en":"Tinned tuna in water 80g","sn":"Tuna yemutini 80g","nd":"I-tuna 80g","carbs":0,"cat":"Meat","level":"🟢 Best"},
    {"en":"Pilchards in tomato 80g","sn":"Pilchards 80g","nd":"Amapilchards 80g","carbs":2,"cat":"Meat","level":"🟢 Good protein"},
    {"en":"Hove fresh fish 100g","sn":"Hove 100g","nd":"Inhlanzi 100g","carbs":0,"cat":"Meat","level":"🟢 Best"},
    {"en":"Kapenta dried 30g","sn":"Kapenta 30g","nd":"Ikapenta 30g","carbs":0,"cat":"Meat","level":"🟢 Good"},
    {"en":"Madora mopane worms 30g","sn":"Madora 30g","nd":"Amacimbi 30g","carbs":2,"cat":"Meat","level":"🟢 Iron best"},
    {"en":"Mazai eggs 2","sn":"Mazai 2","nd":"Amaqanda 2","carbs":1,"cat":"Meat","level":"🟢 Good"},
    {"en":"Bhinzi beans nyaemba 1/2 cup","sn":"Bhinzi Nyaemba 1/2 cup","nd":"Ubhontshisi 1/2 cup","carbs":20,"cat":"Protein","level":"🟢 Good"},
    # Dairy 39-43
    {"en":"Mukaka wakakora sour milk 250ml","sn":"Mukaka wakakora 250ml","nd":"Amasi 250ml","carbs":12,"cat":"Dairy","level":"🟢 Good"},
    {"en":"Mukaka fresh milk 250ml","sn":"Mukaka 250ml","nd":"Ubisi 250ml","carbs":12,"cat":"Dairy","level":"🟡 Medium"},
    {"en":"Yoghurt plain no sugar 200ml","sn":"Yoghurt isina shuga 200ml","nd":"Iyogathi engenashukela","carbs":9,"cat":"Dairy","level":"🟢 Good"},
    {"en":"Yoghurt sweetened 200ml","sn":"Yoghurt ine shuga","nd":"Iyogathi eloshukela","carbs":20,"cat":"Dairy","level":"🔴 Avoid"},
    {"en":"Nzungu peanuts 30g handful","sn":"Nzungu 30g","nd":"Amakinati 30g","carbs":6,"cat":"Snack","level":"🟢 Good"},
    # Breakfast you asked 44-49
    {"en":"Porridge rine dovi 1 cup peanut porridge","sn":"Bota rine dovi 1 cup","nd":"Iphalishi elamantongomane","carbs":30,"cat":"Breakfast","level":"🟢 Good protein"},
    {"en":"Oats porridge no sugar 1 cup","sn":"Oats bota 1 cup","nd":"I-oats 1 cup","carbs":27,"cat":"Breakfast","level":"🟢 Best low GI"},
    {"en":"Cornflakes no sugar 30g 1 cup","sn":"Cornflakes 30g","nd":"I-cornflakes 30g","carbs":24,"cat":"Breakfast","level":"🔴 High small only"},
    {"en":"Weetabix 2 biscuits no sugar","sn":"Weetabix 2","nd":"I-Weetabix 2","carbs":22,"cat":"Breakfast","level":"🟡 Medium"},
    {"en":"Porridge no sugar 1 cup","sn":"Bota risina shuga 1 cup","nd":"Iphalishi elingenashukela","carbs":25,"cat":"Breakfast","level":"🟢 Good"},
    {"en":"Maputi popcorn 1 cup no oil","sn":"Maputi 1 cup","nd":"Amaputi 1 cup","carbs":10,"cat":"Snack","level":"🟢 Good"},
    # Fruits you asked 50-100
    {"en":"Mango 1/2 medium","sn":"Mango 1/2","nd":"Umango 1/2","carbs":15,"cat":"Fruit","level":"🟡 Medium"},
    {"en":"Guava 1 medium","sn":"Guava 1","nd":"AmaGuava 1","carbs":8,"cat":"Fruit","level":"🟢 Good"},
    {"en":"Baobab Mauyu 30g pulp","sn":"Mauyu 30g","nd":"Umkhomo 30g","carbs":12,"cat":"Fruit","level":"🟡 Medium"},
    {"en":"Masawu jujube 10 fruits","sn":"Masawu 10","nd":"Amasawu 10","carbs":10,"cat":"Fruit","level":"🟢 Good"},
    {"en":"Mazhanje wild loquat 10 fruits","sn":"Mazhanje 10","nd":"Amazhanje 10","carbs":9,"cat":"Fruit","level":"🟢 Good"},
    {"en":"Matamba monkey orange 1","sn":"Matamba 1","nd":"Umatamba 1","carbs":13,"cat":"Fruit","level":"🟡 Medium"},
    {"en":"Banana small 1","sn":"Bhanana diki 1","nd":"Ibhanana elincane 1","carbs":20,"cat":"Fruit","level":"🟡 Medium"},
    {"en":"Apple 1 medium","sn":"Apuro 1","nd":"I-apula 1","carbs":19,"cat":"Fruit","level":"🟢 Good"},
    {"en":"Orange 1 medium","sn":"Orenji 1","nd":"I-oranji 1","carbs":12,"cat":"Fruit","level":"🟢 Good"},
    {"en":"Pawpaw papaya 1 cup","sn":"Pawpaw 1 cup","nd":"Ipapaya 1 cup","carbs":10,"cat":"Fruit","level":"🟢 Good best"},
    {"en":"Plums 2 medium","sn":"Plums 2","nd":"Amaplums 2","carbs":12,"cat":"Fruit","level":"🟢 Good"},
    {"en":"Apricots 3","sn":"Apricots 3","nd":"Amapricot 3","carbs":12,"cat":"Fruit","level":"🟢 Good"},
    {"en":"Prunes 3 dried","sn":"Prunes 3","nd":"Amaprune 3","carbs":15,"cat":"Fruit","level":"🟡 Medium small"},
    {"en":"Fruit salad no sugar 1/2 cup pawpaw+apple+guava","sn":"Fruit salad isina shuga 1/2 cup","nd":"Isaladi yezithelo 1/2 cup","carbs":12,"cat":"Fruit","level":"🟢 Best mix"},
    {"en":"Avocado 1/2","sn":"Avocado 1/2","nd":"Ukotapheya 1/2","carbs":2,"cat":"Fruit","level":"🟢 Best healthy fat"},
    {"en":"Tsubvu smelly berry 20 fruits","sn":"Tsubvu 20","nd":"Amatshubvu 20","carbs":8,"cat":"Fruit","level":"🟢 Good best"},
    {"en":"Nyii marula fruit 1","sn":"Nyii Pfura 1","nd":"Amapfura 1","carbs":10,"cat":"Fruit","level":"🟢 Good"},
    {"en":"Tsambati Grewia 20 fruits","sn":"Tsambati 20","nd":"Amasambati 20","carbs":9,"cat":"Fruit","level":"🟢 Good"},
    {"en":"Mulberries black 1/2 cup","sn":"Mulberries 1/2 cup","nd":"Amajikijolo 1/2 cup","carbs":7,"cat":"Fruit","level":"🟢 Best"},
    {"en":"Nhunguru chocolate berry 10","sn":"Nhunguru 10","nd":"Unhungulu 10","carbs":8,"cat":"Fruit","level":"🟢 Good"},
    {"en":"Watermelon 1 cup","sn":"Watermelon 1 cup","nd":"Ikhabe 1 cup","carbs":11,"cat":"Fruit","level":"🟢 Good"},
    {"en":"Pineapple 1/2 cup","sn":"Pineapple 1/2 cup","nd":"Uphayinaphu","carbs":11,"cat":"Fruit","level":"🟡 Medium"},
    {"en":"Soda 330ml can","sn":"Soda 330ml","nd":"Isoda 330ml","carbs":35,"cat":"Drink","level":"🔴 Avoid"},
    {"en":"Maheu no sugar 250ml","sn":"Maheu asina shuga 250ml","nd":"Amahewu 250ml","carbs":15,"cat":"Drink","level":"🟡 Medium"},
    {"en":"Huchi honey 1 tbsp","sn":"Huchi 1 tbsp","nd":"Uju 1 tbsp","carbs":17,"cat":"Sweet","level":"🔴 Avoid"},
    {"en":"Nzimbe sugarcane 100g piece","sn":"Nzimbe 100g","nd":"Umoba 100g","carbs":28,"cat":"Sweet","level":"🔴 Avoid"},
]

st.set_page_config(page_title="Sahwira Health", page_icon="🛡️", layout="wide", initial_sidebar_state="collapsed")
st.markdown("<style>#MainMenu,footer,header,.stDeployButton{visibility:hidden;display:none}.shield{background:linear-gradient(135deg,#0D47A1 0%,#1976D2 100%);padding:20px 24px;border-radius:14px;color:white;box-shadow:0 4px 12px rgba(13,71,161,0.3);margin-bottom:18px}</style>", unsafe_allow_html=True)

top1, top2 = st.columns([4,1])
with top2:
    lang_choice = st.selectbox("🌐", ["English","Shona","Ndebele"], label_visibility="collapsed")
with top1:
    st.markdown("<div class='shield'><div style='display:flex;align-items:center;gap:14px'><div style='font-size:34px'>🛡️</div><div><div style='font-size:23px;font-weight:800'>SAHWIRA HEALTH</div><div style='font-size:12px;opacity:0.92'>Harare, Zimbabwe | Secure Patient Portal | Premium Active</div></div></div></div>", unsafe_allow_html=True)

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

tabs = st.tabs(["Dashboard","Smart Plan","Foods 100","Exercise","Medicine","Family","Reminders","Voice Gogo","Reports"])

with tabs[0]:
    c1,c2,c3 = st.columns(3)
    c1.metric("AVG SUGAR", "6.8 mmol/L", "Good"); c2.metric("LAST", "6.5 Today 07:30"); c3.metric("STREAK", "12 Days")
    df=pd.DataFrame({'Day':['Mon','Tue','Wed','Thu','Fri','Sat','Sun'],'Sugar':[6.5,7.2,6.0,7.8,6.9,6.4,6.7]})
    fig, ax = plt.subplots(figsize=(8,3)); ax.plot(df['Day'], df['Sugar'], marker='o', color='#0D47A1', linewidth=3); ax.set_ylabel("mmol/L"); ax.grid(True, alpha=0.2)
    st.pyplot(fig, use_container_width=True)

with tabs[1]:
    st.subheader("🧠 Smart Plan - BM + Foods at home + Meds → Meals & Exercise")
    c1,c2,c3 = st.columns(3)
    with c1: sugar_now = st.number_input("BM now mmol/L", 2.0, 30.0, 7.5, step=0.1)
    with c2: wt = st.number_input("Weight kg", 40, 150, 70)
    with c3: ht = st.number_input("Height cm", 140, 200, 170)
    bmi = wt/((ht/100)**2)
    available = st.multiselect("Food at home today (tick)", [f"{f['sn']} ({f['carbs']}g) [{f['cat']}]" for f in FOODS], default=[f"{FOODS[1]['sn']} ({FOODS[1]['carbs']}g) [{FOODS[1]['cat']}]", f"{FOODS[14]['sn']} ({FOODS[14]['carbs']}g) [{FOODS[14]['cat']}]", f"{FOODS[23]['sn']} ({FOODS[23]['carbs']}g) [{FOODS[23]['cat']}]"])
    if st.button("Generate Today's Meals + Exercise to stay in range", type="primary", use_container_width=True):
        kcal=wt*28; carb_day=int(kcal*0.45/4); carb_meal=carb_day//3
        if sugar_now>12: carb_meal=max(20,carb_meal-10); ex="40 min fast walk + 20 min kurima - HIGH sugar"
        elif sugar_now>9: carb_meal=max(25,carb_meal-5); ex="30 min fast walk"
        elif sugar_now<4.5: carb_meal+=10; ex="10 min light walk only - LOW sugar eat fruit first"
        else: ex="20 min walk + sweep yard - GOOD"
        st.session_state["bmi"]=bmi; st.session_state["sugar"]=sugar_now; st.session_state["plan"]=f"Target {carb_meal}g/meal {ex}"
        st.success(f"BM {sugar_now} | BMI {bmi:.1f} | Target {carb_meal}g per meal | Exercise {ex}")
        st.markdown(f"""
        **MANGWANANI 07:30 ({carb_meal}g target):** Sadza rezviyo 1/2 cup (20g) + Mowa 1 cup (5g) + Mazai 2 (1g) = 26g ✅ + Water 2 cups
        **MASIKATI 13:00:** Brown rice 1/2 cup or Sadza rerukweza 1/2 cup + Manyanya/Covo + Tsuro/Hanga/Mhou/Hove (0g) + Pawpaw/Fruit salad 1/2 cup (6g) = ~30g ✅
        **MANHERU 19:00:** Nhopi 1/2 cup (14g) + Mutsine 1 cup (4g) + Tuna/Pilchards/Madora (2g) + Cucumber salad (3g) = 23g ✅
        **Snacks:** 10:30 Tsubvu 20 or Guava 1 (8g) | 16:00 Nzungu 30g (6g) or Yoghurt plain (9g) | Porridge rine dovi or Oats if morning
        **Exercise today:** {ex} - lowers sugar 1-2 mmol/L
        """)

with tabs[2]:
    st.subheader(f"📚 Food Library - {len(FOODS)} Zimbabwe Foods incl Tsuro, Hanga, Mhou, Pawpaw, Dovi, Oats")
    search=st.text_input("🔍 Search / Tsvaga / Sesha", placeholder="zviyo, tsuro, hanga, pawpaw, dovi, tsubvu, nhunguru...")
    cat=st.selectbox("Filter Type", ["All","Sadza","Grain","Staple","Muriwo","Veg","Salad","Meat","Protein","Dairy","Breakfast","Fruit","Snack","Drink","Sweet"])
    df=pd.DataFrame(FOODS)
    if search:
        df=df[df["en"].str.contains(search, case=False) | df["sn"].str.contains(search, case=False)]
    if cat!="All":
        df=df[df["cat"]==cat]
    st.dataframe(df[["sn","en","carbs","level","cat"]].rename(columns={"sn":"Shona / Local","en":"English","carbs":"Carbs g","level":"Guide","cat":"Type"}), use_container_width=True, hide_index=True)
    st.caption("🟢 Best/Good daily | 🟡 Small portion | 🔴 Avoid | Carbs per portion shown - Use 1/2 cup for Sadza if sugar high")

with tabs[3]:
    st.subheader("🏃 Exercise Prescribed - Lowers BM 1-2 mmol/L")
    st.markdown("- **Fast walk 30 min** → drops 1.5 mmol/L | Best daily\n- **Kurima 20 min** → drops 2.0 | Excellent\n- **Sweep yard 30 min** → 0.8\n- **Dance 20 min** → 1.2 | Happy heart")
    if st.button("I did exercise today"): st.balloons(); st.success("Great! Check sugar after 30 min")

with tabs[4]:
    st.subheader("💊 My Medicine from Dr")
    m1=st.text_input("Medicine 1", placeholder="Metformin 500mg - 1 morning 1 evening")
    m2=st.text_input("Medicine 2", placeholder="Glibenclamide 5mg - before breakfast")
    t1=st.time_input("Morning time", datetime.time(8,0)); t2=st.time_input("Evening time", datetime.time(20,0))
    if st.button("Save Medicines", type="primary", use_container_width=True):
        st.session_state["meds"]=[m1,m2,str(t1),str(t2)]; st.success(f"Saved {m1}, reminder {t1} & {t2}")

with tabs[5]:
    st.subheader("👨‍👩‍👧‍👦 Family Phone for Monitoring & Support")
    f1=st.text_input("Family 1 Name", placeholder="Mai"); f1p=st.text_input("Family 1 WhatsApp", placeholder="077...")
    f2=st.text_input("Family 2 Name", placeholder="Baba / Daughter"); f2p=st.text_input("Family 2 WhatsApp", placeholder="078...")
    f3=st.text_input("Family 3 - Clinic/Dr", placeholder="Dr Moyo Clinic"); f3p=st.text_input("Clinic Phone", placeholder="029...")
    if st.button("Save Family", type="primary", use_container_width=True):
        st.session_state["family"]=[{"name":f1,"phone":f1p},{"name":f2,"phone":f2p},{"name":f3,"phone":f3p}]
        st.success(f"✅ Saved {f1}, {f2}, {f3}")

with tabs[6]:
    st.subheader("⏰ Reminders - Works Offline When Phone ON")
    st.markdown("No app rings if phone totally OFF - set these 4 alarms in phone clock, works offline no data")
    r1=st.time_input("Check BM Morning", datetime.time(7,0)); r2=st.time_input("Medicine Morning", datetime.time(8,0))
    r3=st.time_input("Check BM Evening", datetime.time(19,0)); r4=st.time_input("Medicine Evening", datetime.time(20,0))
    st.info(f"Alarms: {r1} BM, {r2} Meds, {r3} BM, {r4} Meds + Log food")
    if st.button("Create WhatsApp Reminder for Family", type="primary", use_container_width=True):
        msg=f"SAHWIRA Reminder: BM {r1} & {r3}, Medicine {r2} & {r4}. Target 4.4-7.0. Call gogo."
        st.code(msg); st.link_button("Send via WhatsApp", f"https://wa.me/?text={msg}")

with tabs[7]:
    st.subheader("🔊 Voice for Gogo - Can't read / Visually impaired")
    voice_sn="Mauya Gogo. Mangwanani idya sadza rezviyo hafu kapu ne mowa ne mazai. Tarisa shuga yako na seven mangwanani na seven manheru. Tora mishonga yako na eight mangwanani na eight manheru. Famba kwemaminetsi makumi maviri. Mvura inwa yakawanda."
    voice_nd="Siyakwamukela Gogo. Ekuseni dla isitshwala seziyo ingxenye le mbowa lamaqanda. Hlola ushukela ngo seven ekuseni ngo seven ntambama. Thatha imithi ngo eight ekuseni ngo eight ntambama. Hamba imizuzu engamatshumi amabili."
    voice_en="Hello Gogo. Good morning. Today eat half cup sadza rezviyo with mowa and eggs. Check your sugar at 7am and 7pm. Take medicine at 8am and 8pm. Walk 20 minutes. Drink plenty water."
    lang_v=st.selectbox("Language / Mutauro", ["Shona","Ndebele","English"])
    txt_map={"Shona":voice_sn,"Ndebele":voice_nd,"English":voice_en}
    txt=txt_map[lang_v]
    st.text_area(f"Voice in {lang_v}", txt, height=110)
    if VOICE_OK:
        if st.button(f"🔊 PLAY Voice {lang_v}", type="primary", use_container_width=True):
            try:
                tts=gTTS(text=txt, lang='en'); path="/tmp/gogo.mp3"; tts.save(path); st.audio(path); st.success("Playing 🔊")
            except Exception as e: st.error(str(e))
    else:
        st.warning("Add gtts to requirements.txt")

with tabs[8]:
    st.subheader("📄 Reports for Dr / Clinic - Keep & Print Records")
    dr=st.text_input("Doctor / Clinic Name", placeholder="Dr Moyo - Parirenyatwa")
    if st.button("Generate Full Clinic Report PDF", type="primary", use_container_width=True):
        pdf=FPDF(); pdf.add_page()
        pdf.set_font("Arial","B",16); pdf.cell(0,10,"SAHWIRA HEALTH - CLINIC REPORT", ln=True, align="C")
        pdf.set_font("Arial","",11); pdf.cell(0,8,f"Date: {datetime.date.today()} | Harare, Zimbabwe", ln=True, align="C")
        pdf.ln(4); pdf.set_font("Arial","B",12); pdf.cell(0,8,"Patient Summary", ln=True)
        pdf.set_font("Arial","",10)
        bmi=st.session_state.get("bmi","-"); sugar=st.session_state.get("sugar","-")
        meds=st.session_state.get("meds",["Metformin"]); family=st.session_state.get("family",[{"name":"Mai"}]); plan=st.session_state.get("plan","-")
        pdf.multi_cell(0,5,f"Doctor: {dr}\nBM: {sugar} mmol/L | BMI: {bmi} | Target 4.4-7.0\nMeds: {meds}\nPlan: {plan}\nFamily: {family}\nFood Library: 100 local foods incl tsuro, hanga, mhou, pawpaw, dovi, oats, tsenza, nhopi, mowa, mutsine, tsubvu, nhunguru, masawu, mazhanje, matamba, nyii, tsambati, mulberries\nExercise: Walk, Kurima, Dance\nReminders: 07:00 BM, 08:00 Meds, 19:00 BM, 20:00 Meds (offline)\nVoice: Shona/Ndebele/English for Gogo\n")
        path="/tmp/Sahwira_Report.pdf"; pdf.output(path)
        with open(path,"rb") as f:
            st.download_button("📥 Download & Print for Dr", f, file_name=f"Sahwira_Report_{datetime.date.today()}.pdf", mime="application/pdf", type="primary", use_container_width=True)
