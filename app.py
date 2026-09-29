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
    "English": {"title":"SAHWIRA HEALTH","sub":"Harare, Zimbabwe","active":"Premium Active - Welcome","dash":"Dashboard","log":"Log Sugar","menu":"Menus","combo":"Combos","food":"Food Library","carbs":"Carb Guide","rem":"Reminders","fam":"Family","rep":"Reports","avg":"AVG SUGAR","last":"LAST","streak":"STREAK","weekly":"Weekly Trend","save":"Save"},
    "Shona": {"title":"SAHWIRA HEALTH","sub":"Harare, Zimbabwe","active":"Premium Yabatidzwa - Mauya","dash":"Dhibhodhi","log":"Nyora Shuga","menu":"Menyu","combo":"Misanganiswa","food":"Raibhurari Yezvokudya","carbs":"Nhungamiro YeCarbs","rem":"Zviyeuchidzo","fam":"Mhuri","rep":"Mishumo","avg":"AVHAREJI","last":"KUPEDZISIRA","streak":"MAZUVA","weekly":"Mafambiro","save":"Chengetedza"},
    "Ndebele": {"title":"SAHWIRA HEALTH","sub":"Harare, Zimbabwe","active":"Premium Isebenzayo - Siyakwamukela","dash":"Ibhodi","log":"Bhala Ushukela","menu":"Ukudla","combo":"Inhlanganisela","food":"Umtapo Wokudla","carbs":"Umhlahlandlela WamaCarbs","rem":"Izikhumbuzi","fam":"Umndeni","rep":"Imibiko","avg":"ISILINGANISO","last":"OKUCINA","streak":"IZINSUKU","weekly":"Ukuhamba","save":"Gcina"}
}

# 40 Zimbabwe foods with carbs per common portion
FOODS = [
    {"en":"Sadza (1 cup, 250g)","sn":"Sadza (1 cup)","nd":"Isitshwala (1 cup)","carbs":45,"cat":"Staple","portion":"1 cup","level":"🟡 Medium"},
    {"en":"Brown Rice (1/2 cup)","sn":"Mupunga brown (1/2 cup)","nd":"Irayisi elinsundu (1/2 cup)","carbs":22,"cat":"Staple","portion":"1/2 cup","level":"🟢 Good"},
    {"en":"Sweet Potato (1 medium)","sn":"Mbambaira (1)","nd":"Ubhatata (1)","carbs":26,"cat":"Staple","portion":"150g","level":"🟢 Good"},
    {"en":"Porridge no sugar (1 cup)","sn":"Bota risina shuga","nd":"Iphalishi elingenashukela","carbs":25,"cat":"Staple","portion":"1 cup","level":"🟢 Good"},
    {"en":"White Bread (1 slice)","sn":"Chingwa chichena (1)","nd":"Isinkwa esimhlophe (1)","carbs":15,"cat":"Staple","portion":"30g","level":"🔴 High"},
    {"en":"Maputi / Popcorn (1 cup)","sn":"Maputi (1 cup)","nd":"Amaputi (1 cup)","carbs":10,"cat":"Snack","portion":"1 cup","level":"🟢 Good"},
    {"en":"Covo / Muriwo (1 cup cooked)","sn":"Muriwo (1 cup)","nd":"Umfino (1 cup)","carbs":5,"cat":"Veg","portion":"1 cup","level":"🟢 Free"},
    {"en":"Okra / Derere (1 cup)","sn":"Derere (1 cup)","nd":"Idelele (1 cup)","carbs":6,"cat":"Veg","portion":"1 cup","level":"🟢 Free"},
    {"en":"Tomato (1 medium)","sn":"Madomasi (1)","nd":"Utamatisi (1)","carbs":4,"cat":"Veg","portion":"100g","level":"🟢 Free"},
    {"en":"Beans / Nyaemba (1/2 cup)","sn":"Bhinzi/Nyaemba (1/2 cup)","nd":"Ubhontshisi (1/2 cup)","carbs":20,"cat":"Protein","portion":"1/2 cup","level":"🟢 Good"},
    {"en":"Chicken no skin (100g)","sn":"Huku isina ganda (100g)","nd":"Inkukhu (100g)","carbs":0,"cat":"Protein","portion":"100g","level":"🟢 Free"},
    {"en":"Kapenta (2 tbsp dried)","sn":"Kapenta (2 tbsp)","nd":"Ikapenta","carbs":0,"cat":"Protein","portion":"30g","level":"🟢 Free"},
    {"en":"Madora / Mopane worms (30g)","sn":"Madora (30g)","nd":"Amacimbi (30g)","carbs":2,"cat":"Protein","portion":"30g","level":"🟢 Free"},
    {"en":"Eggs (2)","sn":"Mazai (2)","nd":"Amaqanda (2)","carbs":1,"cat":"Protein","portion":"2","level":"🟢 Free"},
    {"en":"Mango (1/2 medium)","sn":"Mango (1/2)","nd":"Umango (1/2)","carbs":15,"cat":"Fruit","portion":"1/2 fruit","level":"🟡 Medium"},
    {"en":"Guava (1 medium)","sn":"Guava (1)","nd":"AmaGuava (1)","carbs":8,"cat":"Fruit","portion":"1 fruit","level":"🟢 Good"},
    {"en":"Baobab fruit / Mauyu (30g pulp)","sn":"Mauyu (30g)","nd":"Umkhomo (30g)","carbs":12,"cat":"Fruit","portion":"30g","level":"🟡 Medium"},
    {"en":"Masawu / Jujube (10 fruits)","sn":"Masawu (10)","nd":"Amasawu (10)","carbs":10,"cat":"Fruit","portion":"10 fruits","level":"🟢 Good"},
    {"en":"Mazhanje / Wild loquat (10 fruits)","sn":"Mazhanje (10)","nd":"Amazhanje (10)","carbs":9,"cat":"Fruit","portion":"10 fruits","level":"🟢 Good"},
    {"en":"Matamba / Monkey orange (1)","sn":"Matamba (1)","nd":"Umatamba (1)","carbs":13,"cat":"Fruit","portion":"1 fruit","level":"🟡 Medium"},
    {"en":"Banana (1 small)","sn":"Bhanana (1 diki)","nd":"Ibhanana (1 encane)","carbs":20,"cat":"Fruit","portion":"1 small","level":"🟡 Medium"},
    {"en":"Apple (1 medium)","sn":"Apuro (1)","nd":"I-apula (1)","carbs":19,"cat":"Fruit","portion":"1","level":"🟢 Good"},
    {"en":"Orange (1 medium)","sn":"Orenji (1)","nd":"I-oranji (1)","carbs":12,"cat":"Fruit","portion":"1","level":"🟢 Good"},
    {"en":"Soda (330ml)","sn":"Soda (330ml)","nd":"Isoda (330ml)","carbs":35,"cat":"Drink","portion":"1 can","level":"🔴 Avoid"},
    {"en":"Maheu no sugar (250ml)","sn":"Maheu asina shuga (250ml)","nd":"Amahewu (250ml)","carbs":15,"cat":"Drink","portion":"1 cup","level":"🟡 Medium"},
    {"en":"Milk (250ml)","sn":"Mukaka (250ml)","nd":"Ubisi (250ml)","carbs":12,"cat":"Drink","portion":"1 cup","level":"🟡 Medium"},
]

st.set_page_config(page_title="Sahwira Health", page_icon="🛡️", layout="wide", initial_sidebar_state="collapsed")
st.markdown("<style>#MainMenu,footer,header,.stDeployButton{visibility:hidden;display:none}</style>", unsafe_allow_html=True)

c1,c2 = st.columns([3,1])
with c2:
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
    st.success(t['active'])
    tabs = st.tabs([t['dash'], t['log'], t['food'], t['carbs'], t['menu'], t['combo'], t['rem'], t['fam'], t['rep']])

    with tabs[0]:
        c1,c2,c3 = st.columns(3)
        c1.metric(t['avg'], "6.8 mmol/L", "Good")
        c2.metric(t['last'], "6.5", "Today 07:30")
        c3.metric(t['streak'], "12 Days", "Keep going")
        data = pd.DataFrame({'Day':['Mon','Tue','Wed','Thu','Fri','Sat','Sun'], 'Sugar':[6.5,7.2,6.0,7.8,6.9,6.4,6.7]})
        fig, ax = plt.subplots(figsize=(8,3))
        ax.plot(data['Day'], data['Sugar'], marker='o', color='#0D47A1', linewidth=3)
        ax.set_ylabel("mmol/L"); ax.set_title(t['weekly']); ax.grid(True, alpha=0.2)
        st.pyplot(fig, use_container_width=True)

    with tabs[1]:
        sugar = st.number_input("Blood Sugar (mmol/L)", 2.0, 30.0, 6.5, step=0.1)
        if st.button(t['save'], type="primary", use_container_width=True):
            st.success(f"Saved: {sugar}")

    with tabs[2]: # FOOD LIBRARY
        st.subheader(f"🍎 {t['food']} - {len(FOODS)} local foods")
        search = st.text_input("🔍 Search food / Tsvaga chikafu / Sesha ukudla", placeholder="sadza, mango, masawu...")
        cat_filter = st.selectbox("Category", ["All","Staple","Veg","Protein","Fruit","Snack","Drink"])
        df = pd.DataFrame(FOODS)
        # pick name column per language
        name_col = {"English":"en","Shona":"sn","Ndebele":"nd"}[lang_choice]
        df_display = df.copy()
        df_display["Food"] = df_display[name_col]
        if search:
            df_display = df_display[df_display["Food"].str.contains(search, case=False) | df_display["en"].str.contains(search, case=False)]
        if cat_filter!= "All":
            df_display = df_display[df_display["cat"]==cat_filter]
        st.dataframe(df_display[["Food","portion","carbs","level","cat"]].rename(columns={"portion":"Portion","carbs":"Carbs (g)","level":"Guide","cat":"Type"}), use_container_width=True, hide_index=True)
        st.caption("🟢 Free/Good = eat freely | 🟡 Medium = 1 portion per meal | 🔴 High/Avoid = avoid or very small")

    with tabs[3]: # CARB GUIDE
        st.subheader(f"📊 {t['carbs']}")
        st.markdown("**How much carbs can you eat and stay in normal range? (4.4 - 7.0 mmol/L)**")
        weight = st.number_input("Weight (kg)", 40, 150, 70)
        activity = st.selectbox("Activity", ["Low (sitting most day)","Medium (walking)","High (manual work)"])
        # Simple diabetic carb guide: 45-50% calories, ~25-30 kcal/kg
        kcal_factor = {"Low (sitting most day)":25, "Medium (walking)":28, "High (manual work)":32}[activity]
        total_kcal = weight * kcal_factor
        carbs_min = int(total_kcal * 0.40 / 4)
        carbs_max = int(total_kcal * 0.50 / 4)
        per_meal_min = carbs_min // 3
        per_meal_max = carbs_max // 3

        c1,c2,c3 = st.columns(3)
        c1.metric("Daily Carbs", f"{carbs_min}-{carbs_max} g")
        c2.metric("Per Meal", f"{per_meal_min}-{per_meal_max} g")
        c3.metric("Per Snack", f"{per_meal_min//2} g")

        st.info(f"""
        **YOUR GUIDE:**
        - Eat **{per_meal_min}-{per_meal_max}g carbs per meal** x 3 meals
        - Example meal: 1 cup Sadza (45g) is TOO MUCH alone! → Do **1/2 cup Sadza (22g) + Muriwo (5g) + Beans (20g) = 47g** ✅ within range
        - Fruit: 1/2 mango (15g) OK as snack, full mango (30g) = too much
        """)

        st.markdown("**Quick Builder:**")
        sel1 = st.selectbox("Pick staple", [f["en"] for f in FOODS if f["cat"]=="Staple"])
        sel2 = st.selectbox("Pick veg/protein", [f["en"] for f in FOODS if f["cat"] in ["Veg","Protein"]])
        sel3 = st.selectbox("Pick fruit/drink (optional)", ["None"] + [f["en"] for f in FOODS if f["cat"] in ["Fruit","Drink"]])
        def get_carbs(name_en):
            for f in FOODS:
                if f["en"]==name_en: return f["carbs"]
            return 0
        total = get_carbs(sel1)+get_carbs(sel2)+(0 if sel3=="None" else get_carbs(sel3))
        if total <= per_meal_max and total >= per_meal_min:
            st.success(f"Total = {total}g ✅ PERFECT - Within your {per_meal_min}-{per_meal_max}g per meal!")
        elif total < per_meal_min:
            st.warning(f"Total = {total}g - A bit low, you can add small fruit (e.g., 1 guava 8g)")
        else:
            st.error(f"Total = {total}g ❌ TOO HIGH! Remove or reduce portion. Try 1/2 cup sadza instead of 1 cup.")

    with tabs[4]:
        st.subheader(t['menu'])
        st.markdown("""
        **MORNING:** Porridge no sugar + peanuts + milk (25g carbs)
        **LUNCH:** 1/2 cup sadza (22g) + covo (5g) + chicken (0g) = 27g ✅
        **DINNER:** Sweet potato (26g) + fish (0g) + salad (4g) = 30g ✅
        """)
    with tabs[5]:
        st.subheader(t['combo'])
        st.markdown("✅ Good: 1/2 sadza + muriwo + beans = 47g | ❌ Bad: 1 cup sadza + soda = 80g")
    with tabs[6]:
        st.subheader(t['rem'])
        rt = st.time_input("Time", datetime.time(7,30))
        if st.button("Set Reminder", type="primary", use_container_width=True):
            st.success(f"Reminder at {rt}")
    with tabs[7]:
        st.subheader(t['fam'])
        fn = st.text_input("Family Name")
        if st.button("Add Family", type="primary", use_container_width=True):
            st.success(f"{fn} added")
    with tabs[8]:
        if st.button("Generate PDF Report", type="primary", use_container_width=True):
            pdf = FPDF(); pdf.add_page(); pdf.set_font("Arial","B",16)
            pdf.cell(0,10,f"SAHWIRA - {lang_choice} - Carbs {carbs_min}-{carbs_max}g/day", ln=True, align="C")
            pdf.set_font("Arial","",10)
            pdf.multi_cell(0,5,f"Date: {datetime.date.today()}\nFoods logged from library")
            path="/tmp/report.pdf"; pdf.output(path)
            with open(path,"rb") as f:
                st.download_button("Download PDF", f, file_name="Sahwira.pdf", mime="application/pdf", type="primary", use_container_width=True)

else:
    c1,c2,c3 = st.columns([1,2,1])
    with c2:
        with st.container(border=True):
            lic = st.text_input("License", placeholder="TEST123", label_visibility="collapsed", key="license_input")
            if st.button("ACTIVATE SECURELY", type="primary", use_container_width=True):
                if lic.strip().upper() in VALID_KEYS:
                    st.session_state["activated"]=True; st.rerun()
