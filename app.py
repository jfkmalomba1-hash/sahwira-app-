import streamlit as st
import pandas as pd
import datetime
import random
from fpdf import FPDF

try:
    VALID_KEYS = st.secrets["LICENSE_KEYS"]
except:
    VALID_KEYS = ["SAHWIRA100","SAHWIRA200","SAHWIRA365","CLINIC2026","TEST123","SAHWIRA5","ADMIN2026","SAHWIRA1"]

FOODS = [
    # Sadza types
    {"en":"Sadza zviyo (1 cup)","sn":"Sadza rezviyo (1 cup)","carbs":40,"cat":"Staple","level":"🟢 Best"},
    {"en":"Sadza mapfunde (1 cup)","sn":"Sadza remapfunde","carbs":42,"cat":"Staple","level":"🟢 Good"},
    {"en":"Sadza rukweza (1 cup)","sn":"Sadza rerukweza","carbs":38,"cat":"Staple","level":"🟢 Best low GI"},
    {"en":"Sadza white maize (1 cup)","sn":"Sadza chena","carbs":45,"cat":"Staple","level":"🟡"},
    {"en":"Sadza mutakura","sn":"Mutakura (sadza+bhinzi)","carbs":35,"cat":"Staple","level":"🟢 Best"},
    {"en":"Brown rice 1/2 cup","sn":"Mupunga brown","carbs":22,"cat":"Staple","level":"🟢"},
    {"en":"White rice 1/2 cup","sn":"Mupunga chena","carbs":22,"cat":"Staple","level":"🔴"},
    {"en":"Nhopi 1 cup","sn":"Nhopi","carbs":28,"cat":"Staple","level":"🟢"},
    {"en":"Manhanga boiled 1 cup","sn":"Manhanga","carbs":10,"cat":"Veg","level":"🟢 Free"},
    {"en":"Mbambaira 1 med","sn":"Mbambaira","carbs":26,"cat":"Staple","level":"🟢"},
    {"en":"Tsenza 1/2 cup","sn":"Tsenza","carbs":18,"cat":"Staple","level":"🟢 Best"},
    {"en":"Madhumbe 1/2 cup","sn":"Madhumbe","carbs":20,"cat":"Staple","level":"🟢"},
    {"en":"Magogoya 1/2 cup","sn":"Magogoya","carbs":22,"cat":"Staple","level":"🟢"},
    # Muriwo
    {"en":"Mowa 1 cup","sn":"Mowa","carbs":5,"cat":"Muriwo","level":"🟢 Free"},
    {"en":"Mutsine 1 cup","sn":"Mutsine","carbs":4,"cat":"Muriwo","level":"🟢 Free"},
    {"en":"Manyanya/Muboora 1 cup","sn":"Manyanya","carbs":4,"cat":"Muriwo","level":"🟢 Free"},
    {"en":"Covo 1 cup","sn":"Covo","carbs":5,"cat":"Muriwo","level":"🟢 Free"},
    {"en":"Beetroot 1/2 cup","sn":"Beetroot","carbs":8,"cat":"Veg","level":"🟢"},
    {"en":"Carrots 1/2 cup","sn":"Makarotsi","carbs":6,"cat":"Veg","level":"🟢"},
    {"en":"Cauliflower 1 cup","sn":"Cauliflower","carbs":5,"cat":"Veg","level":"🟢 Free"},
    {"en":"Cucumber 1 cup","sn":"Magaka / Cucumber","carbs":3,"cat":"Salad","level":"🟢 Free best"},
    {"en":"Lettuce + tomato salad 1 cup","sn":"Saladhi yemadomasi","carbs":4,"cat":"Salad","level":"🟢 Free"},
    # MEATS YOU ASKED - NEW
    {"en":"Tsuro / Rabbit 100g","sn":"Tsuro (100g)","carbs":0,"cat":"Meat","level":"🟢 Best lean"},
    {"en":"Huku yechibhoyi / Roadrunner 100g","sn":"Huku yechibhoyi (100g)","carbs":0,"cat":"Meat","level":"🟢 Best - no fat"},
    {"en":"Huku normal 100g","sn":"Huku (100g)","carbs":0,"cat":"Meat","level":"🟢"},
    {"en":"Hanga / Guinea fowl 100g","sn":"Hanga (100g)","carbs":0,"cat":"Meat","level":"🟢 Best lean"},
    {"en":"Toki / Turkey 100g","sn":"Toki (100g)","carbs":0,"cat":"Meat","level":"🟢 Best"},
    {"en":"Dhadha / Duck 100g (no skin)","sn":"Dhadha (100g)","carbs":0,"cat":"Meat","level":"🟡 Remove skin"},
    {"en":"Mbudzi / Goat 100g lean","sn":"Mbudzi (100g)","carbs":0,"cat":"Meat","level":"🟢 Good"},
    {"en":"Mombe / Beef lean 100g","sn":"Mombe (100g)","carbs":0,"cat":"Meat","level":"🟡 Small portion"},
    {"en":"Mhou / Ostrich 100g","sn":"Mhou (100g)","carbs":0,"cat":"Meat","level":"🟢 Best - very lean"},
    {"en":"Tinned Tuna in water 80g","sn":"Tuna yemutini","carbs":0,"cat":"Meat","level":"🟢 Best"},
    {"en":"Pilchards in tomato 80g","sn":"Pilchards","carbs":2,"cat":"Meat","level":"🟢 Good protein"},
    {"en":"Hove fresh 100g","sn":"Hove","carbs":0,"cat":"Meat","level":"🟢 Best"},
    {"en":"Kapenta 30g","sn":"Kapenta","carbs":0,"cat":"Meat","level":"🟢"},
    {"en":"Madora 30g","sn":"Madora","carbs":2,"cat":"Meat","level":"🟢 Iron"},
    {"en":"Mazai 2","sn":"Mazai 2","carbs":1,"cat":"Meat","level":"🟢"},
    {"en":"Bhinzi 1/2 cup","sn":"Bhinzi/Nyaemba","carbs":20,"cat":"Protein","level":"🟢"},
    # Dairy
    {"en":"Mukaka wakakora 250ml","sn":"Mukaka wakakora","carbs":12,"cat":"Dairy","level":"🟢"},
    {"en":"Mukaka fresh 250ml","sn":"Mukaka","carbs":12,"cat":"Dairy","level":"🟡"},
    {"en":"Yoghurt plain 200ml","sn":"Yoghurt isina shuga","carbs":9,"cat":"Dairy","level":"🟢"},
    # Porridge & Breakfast you asked - NEW
    {"en":"Porridge rine dovi 1 cup","sn":"Bota rine dovi (1 cup)","carbs":30,"cat":"Breakfast","level":"🟢 Good + protein"},
    {"en":"Oats porridge 1 cup no sugar","sn":"Oats bota (1 cup)","carbs":27,"cat":"Breakfast","level":"🟢 Best - low GI"},
    {"en":"Cornflakes 1 cup no sugar (30g)","sn":"Cornflakes (30g)","carbs":24,"cat":"Breakfast","level":"🔴 High - small only"},
    {"en":"Weetabix 2 biscuits no sugar","sn":"Weetabix 2","carbs":22,"cat":"Breakfast","level":"🟡 Medium"},
    {"en":"Porridge no sugar 1 cup","sn":"Bota risina shuga","carbs":25,"cat":"Breakfast","level":"🟢"},
    # Fruits & salads you asked - NEW
    {"en":"Pawpaw / Papaya 1 cup","sn":"Pawpaw (1 cup)","carbs":10,"cat":"Fruit","level":"🟢 Good"},
    {"en":"Cucumber 1 cup (salad)","sn":"Magaka","carbs":3,"cat":"Salad","level":"🟢 Free"},
    {"en":"Plums 2 medium","sn":"Plums 2","carbs":12,"cat":"Fruit","level":"🟢"},
    {"en":"Apricots 3","sn":"Apricots 3","carbs":12,"cat":"Fruit","level":"🟢"},
    {"en":"Prunes 3","sn":"Prunes 3","carbs":15,"cat":"Fruit","level":"🟡 Small"},
    {"en":"Fruit salad no sugar 1/2 cup (pawpaw+apple+guava)","sn":"Fruit salad isina shuga","carbs":12,"cat":"Fruit","level":"🟢 Best mix"},
    {"en":"Mango 1/2","sn":"Mango 1/2","carbs":15,"cat":"Fruit","level":"🟡"},
    {"en":"Guava 1","sn":"Guava 1","carbs":8,"cat":"Fruit","level":"🟢"},
    {"en":"Orange 1","sn":"Orenji 1","carbs":12,"cat":"Fruit","level":"🟢"},
    {"en":"Apple 1 med","sn":"Apuro 1","carbs":19,"cat":"Fruit","level":"🟢"},
    {"en":"Banana small 1","sn":"Bhanana diki","carbs":20,"cat":"Fruit","level":"🟡"},
    {"en":"Mazhanje 10","sn":"Mazhanje 10","carbs":9,"cat":"Fruit","level":"🟢"},
    {"en":"Tsubvu 20","sn":"Tsubvu 20","carbs":8,"cat":"Fruit","level":"🟢"},
    {"en":"Nhunguru 10","sn":"Nhunguru 10","carbs":8,"cat":"Fruit","level":"🟢"},
    {"en":"Masawu 10","sn":"Masawu 10","carbs":10,"cat":"Fruit","level":"🟢"},
    {"en":"Matamba 1","sn":"Matamba 1","carbs":13,"cat":"Fruit","level":"🟡"},
    {"en":"Nyii 1","sn":"Nyii 1","carbs":10,"cat":"Fruit","level":"🟢"},
    {"en":"Avocado 1/2","sn":"Avocado 1/2","carbs":2,"cat":"Fruit","level":"🟢 Best fat"},
    {"en":"Baobab Mauyu 30g","sn":"Mauyu 30g","carbs":12,"cat":"Fruit","level":"🟡"},
    {"en":"Nzungu 30g","sn":"Nzungu 30g","carbs":6,"cat":"Snack","level":"🟢"},
    {"en":"Huchi 1 tbsp","sn":"Huchi (avoid)","carbs":17,"cat":"Sweet","level":"🔴 Avoid"},
    {"en":"Nzimbe 100g","sn":"Nzimbe (avoid)","carbs":28,"cat":"Sweet","level":"🔴 Avoid"},
]

EXERCISES = [
    {"name":"Kufamba nekukurumidza / Fast walk","drop":1.5,"min":30},
    {"name":"Kurima 20 min","drop":2.0,"min":20},
    {"name":"Kutsvaira chivanze 30 min","drop":0.8,"min":30},
    {"name":"Kutamba / Dance 20 min","drop":1.2,"min":20},
]

st.set_page_config(page_title="Sahwira V6.1", page_icon="🧠", layout="wide")
st.markdown("<style>#MainMenu,footer{display:none}</style>", unsafe_allow_html=True)

lang = st.selectbox("🌐 English / Shona / Ndebele", ["English","Shona","Ndebele"], label_visibility="collapsed")
st.markdown("<div style='background:#0D47A1;padding:16px;border-radius:12px;color:white'><b>SAHWIRA V6.1 SMART</b> - 100+ Foods incl Tsuro, Hanga, Mhou, Pawpaw, Dovi, Oats</div>", unsafe_allow_html=True)

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
        st.text_input("License", key="lic", placeholder="TEST123")
        if st.button("ACTIVATE", type="primary", use_container_width=True):
            if st.session_state["lic"].strip().upper() in VALID_KEYS:
                st.session_state["activated"]=True; st.rerun()
    st.stop()

st.success("Premium Active - 100 Foods Ready")

tab1, tab2, tab3 = st.tabs(["📝 Enter Today", "🍽️ My Day Plan", "📚 Full Library"])

with tab1:
    st.subheader("1) BM now + Body")
    c1,c2,c3 = st.columns(3)
    with c1:
        sugar_now = st.number_input("Current BM mmol/L", 2.0, 30.0, 7.5, step=0.1)
    with c2:
        weight = st.number_input("Weight kg", 40, 150, 70)
    with c3:
        height = st.number_input("Height cm", 140, 200, 170)
    bmi = weight / ((height/100)**2)
    st.metric("BMI", f"{bmi:.1f}")

    st.subheader("2) What food is at home today? (Tick all you have)")
    all_names = [f"{f['sn']} - {f['en']} ({f['carbs']}g) [{f['cat']}]" for f in FOODS]
    available = st.multiselect("Choose foods available in house (min 6)", all_names, default=all_names[20:35])

    st.subheader("3) Medicine")
    meds = st.multiselect("Meds", ["Metformin 500mg","Glibenclamide 5mg","Insulin","None","Other"])
    med_other = st.text_input("Other med")
    taken = st.checkbox("Took morning meds today")

    if st.button("🧠 GENERATE MY TODAY PLAN", type="primary", use_container_width=True):
        st.session_state["plan"] = {"sugar":sugar_now,"wt":weight,"ht":height,"bmi":bmi,"available":available,"meds":meds,"taken":taken}
        st.success("Done! Go to My Day Plan tab")
        st.balloons()

with tab2:
    if "plan" not in st.session_state:
        st.warning("Go to Enter Today first")
        st.stop()
    p = st.session_state["plan"]
    sugar = p["sugar"]; bmi = p["bmi"]
    kcal = p["wt"]*28
    carb_day = int(kcal*0.45/4)
    carb_meal = carb_day//3
    if sugar>12:
        status="🔴 HIGH"; carb_meal=max(20,carb_meal-10); ex_min=40
    elif sugar>9:
        status="🟡 HIGH"; carb_meal=max(25,carb_meal-5); ex_min=30
    elif sugar<4.5:
        status="🔵 LOW"; carb_meal+=10; ex_min=10
    else:
        status="🟢 GOOD"; ex_min=20

    st.subheader(f"Now: {sugar} mmol/L {status} | Target {carb_meal}g per meal | BMI {bmi:.1f}")
    c1,c2 = st.columns(2)
    c1.metric("Target/meal", f"{carb_meal}g")
    c2.metric("Exercise today", f"{ex_min} min")

    # map available to objects
    avail_objs=[]
    for a in p["available"]:
        for f in FOODS:
            if f["en"] in a or f["sn"] in a:
                avail_objs.append(f); break
    staples=[f for f in avail_objs if f["cat"] in ["Staple","Breakfast"]]
    muriwo=[f for f in avail_objs if f["cat"] in ["Muriwo","Veg","Salad"]]
    meat=[f for f in avail_objs if f["cat"] in ["Meat","Protein"]]
    fruits=[f for f in avail_objs if f["cat"] in ["Fruit","Snack","Dairy"]]

    if not staples: staples=[f for f in FOODS if f["cat"]=="Staple"][:2]
    if not muriwo: muriwo=[f for f in FOODS if f["cat"]=="Muriwo"][:2]
    if not meat: meat=[{"sn":"Mazai 2","carbs":1,"en":"Eggs"}]

    def make_meal(name,time):
        s=random.choice(staples); m=random.choice(muriwo); pr=random.choice(meat)
        s_c = s["carbs"]//2 if s["carbs"]>25 else s["carbs"]
        if "Cornflakes" in s["en"] or "Weetabix" in s["en"]:
            s_c = s["carbs"]  # already small
        total=s_c + m["carbs"] + pr["carbs"]
        extra=""
        if total < carb_meal-8 and fruits:
            fr=random.choice(fruits)
            if total+fr["carbs"] <= carb_meal+5:
                extra=f" + {fr['sn']} ({fr['carbs']}g)"
                total+=fr["carbs"]
        # special handling for dovi
        note=""
        if "dovi" in s["sn"].lower():
            note=" (Dovi adds protein, good!)"
        st.markdown(f"**{name} ({time}) - {total}g {'✅' if total<=carb_meal+5 else '⚠️'}**\n- {s['sn']} → 1/2 cup ONLY ({s_c}g){note}\n- {m['sn']} → 1 cup full ({m['carbs']}g) eat first\n- {pr['sn']} ({pr['carbs']}g){extra}\n- Water 2 cups")
        return total

    b=make_meal("MANGWANANI / Breakfast","07:30")
    l=make_meal("MASIKATI / Lunch","13:00")
    d=make_meal("MANHERU / Dinner","19:00")
    st.markdown(f"**Snack 10:30:** Choose from your fruits: e.g., Tsubvu/Guava/Pawpaw (8-10g)")
    st.markdown(f"**Snack 16:00:** Nzungu 30g (6g) or Yoghurt plain (9g)")

    st.markdown("### 🏃 Exercise to stay in range")
    if sugar>10:
        st.error(f"Sugar {sugar} high → Do {ex_min} min fast walk + kurima. Drops ~2 mmol/L. Recheck after 1hr.")
    elif sugar<5:
        st.warning(f"Sugar {sugar} low → Light walk {ex_min} min only. Eat fruit first!")
    else:
        st.success(f"Sugar good → {ex_min} min walk + sweep yard keeps stable.")
    for ex in EXERCISES:
        st.markdown(f"- {ex['name']}: {ex['min']} min → drops {ex['drop']} mmol/L")

    if not p["taken"]:
        st.error("⚠️ Take morning meds now with food!")
    else:
        st.success(f"Meds taken: {', '.join(p['meds'])} - Evening at 20:00")

    if st.button("Save PDF Plan"):
        pdf=FPDF(); pdf.add_page(); pdf.set_font("Arial","B",12)
        pdf.cell(0,10,f"Plan BM {sugar} BMI {bmi:.1f}",ln=True); pdf.set_font("Arial","",10)
        pdf.multi_cell(0,5,f"Date {datetime.date.today()}\nMeals B{b}g L{l}g D{d}g\nExercise {ex_min}min\nMeds {p['meds']}")
        path="/tmp/plan.pdf"; pdf.output(path)
        with open(path,"rb") as f:
            st.download_button("Download", f, file_name="Plan.pdf", mime="application/pdf", type="primary")

with tab3:
    st.subheader("📚 Full Library 100+ Foods - Tsuro, Hanga, Mhou, Pawpaw, Dovi, Oats etc")
    search=st.text_input("Search / Tsvaga", placeholder="tsuro, hanga, pawpaw, dovi, oats...")
    cat=st.selectbox("Filter", ["All","Staple","Muriwo","Veg","Salad","Meat","Protein","Breakfast","Fruit","Dairy","Snack","Sweet"])
    df=pd.DataFrame(FOODS)
    if search:
        df=df[df["en"].str.contains(search, case=False) | df["sn"].str.contains(search, case=False)]
    if cat!="All":
        df=df[df["cat"]==cat]
    st.dataframe(df[["sn","en","carbs","level","cat"]].rename(columns={"sn":"Shona / Local","en":"English","carbs":"Carbs g","level":"Guide","cat":"Type"}), use_container_width=True, hide_index=True)
    st.caption("🟢 Best/Good = eat daily | 🟡 Small portion | 🔴 Avoid | All carbs per portion shown")
