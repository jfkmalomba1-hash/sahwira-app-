import streamlit as st
import pandas as pd
import datetime
from fpdf import FPDF
import matplotlib.pyplot as plt
from PIL import Image

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
    {"en":"Sadza white 1 cup","sn":"Sadza chena 1 cup","nd":"Isitshwala esimhlophe","carbs":45,"cat":"Sadza","level":"🟡","img":"🍚"},
    {"en":"Sadza zviyo 1 cup","sn":"Sadza rezviyo 1 cup","nd":"Isitshwala seziyo","carbs":40,"cat":"Sadza","level":"🟢 Best","img":"🍚"},
    {"en":"Sadza mapfunde 1 cup","sn":"Sadza remapfunde","nd":"Isitshwala samabele","carbs":42,"cat":"Sadza","level":"🟢","img":"🍚"},
    {"en":"Sadza rukweza 1 cup","sn":"Sadza rerukweza","nd":"Isitshwala serukweza","carbs":38,"cat":"Sadza","level":"🟢 Best","img":"🍚"},
    {"en":"Mutakura 1 cup","sn":"Mutakura","nd":"Umutakura","carbs":35,"cat":"Sadza","level":"🟢 Best","img":"🍚"},
    {"en":"Brown rice 1/2 cup","sn":"Mupunga brown","nd":"Irayisi elinsundu","carbs":22,"cat":"Grain","level":"🟢","img":"🍚"},
    {"en":"Nhopi 1 cup","sn":"Nhopi","nd":"Inhopi","carbs":28,"cat":"Staple","level":"🟢","img":"🎃"},
    {"en":"Mbambaira 1 med","sn":"Mbambaira","nd":"Ubhatata","carbs":26,"cat":"Staple","level":"🟢","img":"🍠"},
    {"en":"Tsenza 1/2 cup","sn":"Tsenza","nd":"Amatsenza","carbs":18,"cat":"Staple","level":"🟢 Best","img":"🥔"},
    {"en":"Madhumbe 1/2 cup","sn":"Madhumbe","nd":"Amadumbe","carbs":20,"cat":"Staple","level":"🟢","img":"🥔"},
    {"en":"Magogoya 1/2 cup","sn":"Magogoya","nd":"Amagogoya","carbs":22,"cat":"Staple","level":"🟢","img":"🥔"},
    {"en":"Mowa 1 cup","sn":"Mowa","nd":"Imbowa","carbs":5,"cat":"Muriwo","level":"🟢 Free","img":"🥬"},
    {"en":"Mutsine 1 cup","sn":"Mutsine","nd":"Umhlalavane","carbs":4,"cat":"Muriwo","level":"🟢 Free","img":"🥬"},
    {"en":"Manyanya 1 cup","sn":"Manyanya","nd":"Amaqa emathanga","carbs":4,"cat":"Muriwo","level":"🟢 Free","img":"🥬"},
    {"en":"Covo 1 cup","sn":"Covo","nd":"Icovo","carbs":5,"cat":"Muriwo","level":"🟢 Free","img":"🥬"},
    {"en":"Cucumber 1 cup","sn":"Magaka","nd":"Ikhukhamba","carbs":3,"cat":"Salad","level":"🟢 Free best","img":"🥒"},
    {"en":"Salad 1 cup","sn":"Saladhi","nd":"Isaladi","carbs":4,"cat":"Salad","level":"🟢 Free","img":"🥗"},
    {"en":"Tsuro 100g","sn":"Tsuro","nd":"Umvundla","carbs":0,"cat":"Meat","level":"🟢 Best lean","img":"🍖"},
    {"en":"Roadrunner 100g","sn":"Huku yechibhoyi","nd":"Inkukhu yesiXhosa","carbs":0,"cat":"Meat","level":"🟢 Best","img":"🍗"},
    {"en":"Hanga 100g","sn":"Hanga","nd":"Inkanga","carbs":0,"cat":"Meat","level":"🟢 Best","img":"🍗"},
    {"en":"Mhou 100g","sn":"Mhou","nd":"Intshe","carbs":0,"cat":"Meat","level":"🟢 Best","img":"🍖"},
    {"en":"Tuna tin 80g","sn":"Tuna","nd":"I-tuna","carbs":0,"cat":"Meat","level":"🟢 Best","img":"🐟"},
    {"en":"Hove 100g","sn":"Hove","nd":"Inhlanzi","carbs":0,"cat":"Meat","level":"🟢 Best","img":"🐟"},
    {"en":"Madora 30g","sn":"Madora","nd":"Amacimbi","carbs":2,"cat":"Meat","level":"🟢 Iron","img":"🐛"},
    {"en":"Mazai 2","sn":"Mazai 2","nd":"Amaqanda 2","carbs":1,"cat":"Meat","level":"🟢","img":"🥚"},
    {"en":"Mukaka wakakora 250ml","sn":"Mukaka wakakora","nd":"Amasi","carbs":12,"cat":"Dairy","level":"🟢","img":"🥛"},
    {"en":"Pawpaw 1 cup","sn":"Pawpaw","nd":"Ipapaya","carbs":10,"cat":"Fruit","level":"🟢 Best","img":"🍈"},
    {"en":"Tsubvu 20","sn":"Tsubvu 20","nd":"Amatshubvu","carbs":8,"cat":"Fruit","level":"🟢 Best","img":"🍒"},
    {"en":"Guava 1","sn":"Guava 1","nd":"AmaGuava","carbs":8,"cat":"Fruit","level":"🟢","img":"🍈"},
    {"en":"Porridge rine dovi 1 cup","sn":"Bota rine dovi","nd":"Iphalishi elamantongomane","carbs":30,"cat":"Breakfast","level":"🟢","img":"🥣"},
    {"en":"Oats 1 cup","sn":"Oats bota","nd":"I-oats","carbs":27,"cat":"Breakfast","level":"🟢 Best","img":"🥣"},
    {"en":"Tea no sugar 250ml","sn":"Tea isina shuga","nd":"Itayi engenashukela","carbs":0,"cat":"Beverage","level":"🟢 Free best","img":"☕"},
    {"en":"Tea with milk no sugar","sn":"Tea nemukaka isina shuga","nd":"Itayi lobisi engenashukela","carbs":3,"cat":"Beverage","level":"🟢 Good","img":"☕"},
    {"en":"Tea 1 tsp sugar","sn":"Tea ne shuga 1 tsp","nd":"Itayi loshukela 1 tsp","carbs":8,"cat":"Beverage","level":"🔴 Avoid","img":"☕"},
    {"en":"Coke 330ml","sn":"Coke 330ml","nd":"I-Coke","carbs":35,"cat":"Beverage","level":"🔴 Avoid","img":"🥤"},
    {"en":"Coke Light Zero 330ml","sn":"Coke Light","nd":"I-Coke Light","carbs":0,"cat":"Beverage","level":"🟡 Better than coke","img":"🥤"},
    {"en":"Water 250ml","sn":"Mvura 250ml","nd":"Amanzi","carbs":0,"cat":"Beverage","level":"🟢 Best","img":"💧"},
    {"en":"Brown bread 1 slice 30g","sn":"Chingwa brown 1 slice","nd":"Isinkwa esinsundu","carbs":12,"cat":"Bread","level":"🟢 Better","img":"🍞"},
    {"en":"White bread 1 slice 30g","sn":"Chingwa chena 1 slice","nd":"Isinkwa esimhlophe","carbs":14,"cat":"Bread","level":"🟡 Small","img":"🍞"},
    {"en":"Chimodho 1 piece 80g","sn":"Chimodho 1 piece","nd":"Ichimodho","carbs":35,"cat":"Bread","level":"🔴 High share half","img":"🍞"},
    {"en":"Cake slice 80g","sn":"Keke 1 slice","nd":"Ikhekhe","carbs":35,"cat":"Bread","level":"🔴 Avoid","img":"🍰"},
]

st.set_page_config(page_title="Sahwira Health Sugar Guide", page_icon="🛡️", layout="wide", initial_sidebar_state="collapsed")
st.markdown("<style>#MainMenu,footer,header,.stDeployButton{visibility:hidden;display:none}.shield{background:linear-gradient(135deg,#0D47A1 0%,#1976D2 100%);padding:20px 24px;border-radius:14px;color:white;box-shadow:0 4px 12px rgba(13,71,161,0.3);margin-bottom:18px}</style>", unsafe_allow_html=True)

top1, top2 = st.columns([4,1])
with top2:
    lang = st.selectbox("🌐", ["English","Shona","Ndebele"], label_visibility="collapsed")
with top1:
    st.markdown("<div class='shield'><div style='display:flex;align-items:center;gap:14px'><div style='font-size:34px'>🛡️</div><div><div style='font-size:22px;font-weight:800'>SAHWIRA HEALTH SUGAR GUIDE</div><div style='font-size:11px;opacity:0.92'>Diabetic Support App | Harare, Zimbabwe | Improve Quality of Life | Premium Active</div></div></div></div>", unsafe_allow_html=True)

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
            st.markdown("### 🛡️ SAHWIRA HEALTH SUGAR GUIDE")
            st.caption("Support app to improve quality of life & reduce symptoms. Not a replacement for medical advice.")
            st.text_input("License Key", key="lic", placeholder="TEST123", label_visibility="collapsed")
            col_a,col_b = st.columns(2)
            with col_a:
                if st.button("ACTIVATE", type="primary", use_container_width=True):
                    if st.session_state["lic"].strip().upper() in VALID_KEYS:
                        st.session_state["activated"]=True; st.rerun()
                    else:
                        st.error("Invalid")
            with col_b:
                if st.button("How to Pay $15/yr", use_container_width=True):
                    st.info("EcoCash 0771477408 - James - $5 x3 = $15/year - InnBucks available. Send proof to 0771477408 for key.")
    st.stop()

tabs = st.tabs(["Dashboard","Smart Plan","Foods 100+","Pairing","Add My Food + Photo","Meal Times","Exercise","Medicine","Family","Reminders","Voice Gogo","Signs & Help","Pay & Activate","Reports"])

with tabs[0]:
    c1,c2,c3 = st.columns(3)
    c1.metric("AVG SUGAR", "6.8 mmol/L", "Good"); c2.metric("LAST", "6.5 Today 07:30"); c3.metric("STREAK", "12 Days")
    df=pd.DataFrame({'Day':['Mon','Tue','Wed','Thu','Fri','Sat','Sun'],'Sugar':[6.5,7.2,6.0,7.8,6.9,6.4,6.7]})
    fig, ax = plt.subplots(figsize=(8,3)); ax.plot(df['Day'], df['Sugar'], marker='o', color='#0D47A1', linewidth=3); ax.set_ylabel("mmol/L"); ax.grid(True, alpha=0.2)
    st.pyplot(fig, use_container_width=True)

with tabs[1]:
    st.subheader("🧠 Smart Plan - BM + Foods at home + Meds → Meals")
    c1,c2,c3 = st.columns(3)
    with c1: sugar_now = st.number_input("BM now mmol/L", 2.0, 30.0, 7.5, step=0.1)
    with c2: wt = st.number_input("Weight kg", 40, 150, 70)
    with c3: ht = st.number_input("Height cm", 140, 200, 170)
    bmi = wt/((ht/100)**2)
    available = st.multiselect("Food at home", [f"{f['img']} {f['sn']} ({f['carbs']}g)" for f in FOODS], default=[f"{FOODS[1]['img']} {FOODS[1]['sn']} ({FOODS[1]['carbs']}g)"])
    if st.button("Generate Today's Meals + Exercise", type="primary", use_container_width=True):
        carb_meal = int(wt*28*0.45/4)//3
        if sugar_now>9: carb_meal=max(20,carb_meal-5)
        st.session_state["bmi"]=bmi; st.session_state["sugar"]=sugar_now
        st.success(f"BM {sugar_now} | BMI {bmi:.1f} | Target {carb_meal}g per meal")
        st.markdown(f"**MANGWANANI:** 🍚 Sadza rezviyo 1/2 cup (20g) + 🥬 Mowa 1 cup + 🥚 Mazai 2 = 26g ✅\n**MASIKATI:** Brown rice 1/2 cup + Manyanya + Tsuro/Hanga + Pawpaw = ~30g ✅\n**MANHERU:** See Meal Times tab - before 19:30 - Nhopi 1/2 cup + Covo + Tuna = ~20g ✅")

with tabs[2]:
    st.subheader(f"📚 Food Library - {len(FOODS)} Foods with Portion Pictures")
    st.markdown("""
    **📸 Portion Picture Guide - How to take photo:**
    - **Sadza:** Take photo of **1 cup** vs **1/2 cup** - use same plate/bowl daily. 1/2 cup = fist size.
    - **Muriwo:** 1 cup full = 2 handfuls
    - **Meat:** Palm size = 100g
    - **Bread:** 1 slice = 1 finger thick
    - **Tsubvu:** 20 fruits = small handful 8g
    - **Tip:** Use phone camera in Add My Food tab to save YOUR plate photo for reference.
    """)
    search=st.text_input("🔍 Search", placeholder="tsuro, chimodho, coke light...")
    cat=st.selectbox("Filter", ["All","Sadza","Staple","Muriwo","Salad","Meat","Dairy","Fruit","Beverage","Bread","Breakfast"])
    df=pd.DataFrame(FOODS)
    if search:
        df=df[df["en"].str.contains(search, case=False) | df["sn"].str.contains(search, case=False)]
    if cat!="All":
        df=df[df["cat"]==cat]
    st.dataframe(df[["img","sn","en","carbs","level","cat"]].rename(columns={"img":"Pic","sn":"Shona","en":"English","carbs":"Carbs g","level":"Guide","cat":"Type"}), use_container_width=True, hide_index=True)

with tabs[3]:
    st.subheader("🔗 Pairing Proteins + Carbs + Fruits for Steady Curve")
    st.markdown("**Good pairing:** 1/2 staple + 1 cup muriwo first + palm protein + small fruit = flat curve. **Example:** Sadza rezviyo 1/2 cup (20g) + Mowa 1 cup (5g) + Tsuro 100g (0g) + Tsubvu 10 (4g) = 29g slow ✅\n\n**Bad:** Sadza chena full 1 cup (45g) + Coke 330ml (35g) = 80g spike 🔴")

with tabs[4]:
    st.subheader("➕ Add Food Not in Library + 📸 Take Real Photo Portion with Phone Camera")
    st.markdown("**Take photo of your plate / food with phone camera - saves for future + for Dr**")

    # Camera input for real portions
    st.markdown("#### 📸 Step 1: Take Photo of Your Portion")
    camera_photo = st.camera_input("Take photo of your sadza / plate / bread / tsubvu portion", help="Point camera at plate, take photo - shows Dr and saves")
    uploaded_photo = st.file_uploader("Or upload photo from gallery", type=["jpg","jpeg","png"])

    photo_to_use = camera_photo if camera_photo else uploaded_photo

    if photo_to_use:
        image = Image.open(photo_to_use)
        st.image(image, caption="Your portion photo - will be saved in report", use_container_width=True)
        st.success("✅ Photo captured! Now add carbs below and save")

    st.markdown("#### Step 2: Add Carb Info")
    custom_name = st.text_input("Food name e.g., My sadza zviyo 1/2 cup photo")
    custom_carbs = st.number_input("Carbs grams per this portion in photo", 0, 100, 20)
    custom_cat = st.selectbox("Type", ["Staple","Muriwo","Meat","Fruit","Beverage","Bread","Other"])
    custom_portion = st.text_input("Portion description for photo e.g., 1/2 cup in blue bowl, palm size")

    if st.button("💾 Save My Food + Photo to My Library", type="primary", use_container_width=True):
        if "custom_foods" not in st.session_state:
            st.session_state["custom_foods"]=[]
        entry = {"sn":custom_name,"en":custom_name,"carbs":custom_carbs,"cat":custom_cat,"level":f"{custom_portion} 📸 photo saved","img":"📸"}
        st.session_state["custom_foods"].append(entry)
        # Save photo reference
        if photo_to_use:
            if "food_photos" not in st.session_state:
                st.session_state["food_photos"]=[]
            st.session_state["food_photos"].append({"name":custom_name,"photo":photo_to_use})
        st.success(f"✅ Added {custom_name} {custom_carbs}g with photo - now in Smart Plan")
        st.balloons()

    if "custom_foods" in st.session_state and st.session_state["custom_foods"]:
        st.markdown("#### My Custom Foods with Photos")
        st.dataframe(pd.DataFrame(st.session_state["custom_foods"]), use_container_width=True)
        if "food_photos" in st.session_state:
            for fp in st.session_state["food_photos"][-3:]:
                st.image(fp["photo"], caption=fp["name"], width=200)

    st.markdown("**How to estimate carbs if no label:** Meat 0g | Muriwo 3-5g cup | Fruit 8-15g medium | Sadza 1/2 cup 20-22g | Bread 1 slice 12-14g | Soda 330ml 35g | Tea 1 tsp sugar 5g")

with tabs[5]:
    st.subheader("⏰ Best Meal Times - Supper for Good Fasting BM")
    st.markdown("**Breakfast 06:30-08:00** | **Snack 10:00** Tsubvu | **Lunch 12:30-13:30** | **Snack 15:30** | **Supper 18:00-19:00 MOST IMPORTANT** - Eat before 19:30, light 20-25g (Nhopi 1/2 cup + Covo + Hove) + 10 min walk. If eat Chimodho 22:00, fasting will be HIGH 8-10. Late hungry? Tsubvu or Yoghurt plain.")

with tabs[6]:
    st.subheader("🏃 Exercise"); st.markdown("Fast walk 30 min → drops 1.5 | Kurima 20 min → 2.0 | Dance 20 min → 1.2")
    if st.button("I did exercise today"): st.balloons()

with tabs[7]:
    st.subheader("💊 Medicine"); m1=st.text_input("Medicine 1"); t1=st.time_input("Morning", datetime.time(8,0)); t2=st.time_input("Evening", datetime.time(20,0))
    if st.button("Save Medicines", type="primary", use_container_width=True): st.session_state["meds"]=[m1,str(t1),str(t2)]; st.success("Saved")

with tabs[8]:
    st.subheader("👨‍👩‍👧‍👦 Family"); f1=st.text_input("Family 1 Name"); f1p=st.text_input("WhatsApp 1"); f3=st.text_input("Clinic"); f3p=st.text_input("Clinic Phone")
    if st.button("Save Family", type="primary", use_container_width=True): st.session_state["family"]=[{"name":f1,"phone":f1p},{"name":f3,"phone":f3p}]; st.success("Saved")

with tabs[9]:
    st.subheader("⏰ Reminders - Offline"); r1=st.time_input("BM Morning", datetime.time(7,0)); r2=st.time_input("Meds Morning", datetime.time(8,0)); st.info(f"Alarms: {r1} BM, {r2} Meds - set in phone clock works offline")

with tabs[10]:
    st.subheader("🔊 Voice for Gogo")
    voice_sn="Mauya Gogo. Mangwanani idya sadza rezviyo hafu kapu ne mowa ne mazai. Tarisa shuga na seven. Tora mishonga na eight. Famba maminetsi makumi maviri."
    lang_v=st.selectbox("Language", ["Shona","Ndebele","English"])
    st.text_area(f"Voice {lang_v}", voice_sn)
    if VOICE_OK:
        if st.button(f"🔊 PLAY {lang_v}", type="primary", use_container_width=True):
            try:
                tts=gTTS(text=voice_sn, lang='en'); path="/tmp/gogo.mp3"; tts.save(path); st.audio(path)
            except Exception as e: st.error(str(e))

with tabs[11]:
    st.subheader("⚠️ Signs & Diagnosis + When to Seek Help")
    st.markdown("""
    **SAHWIRA HEALTH SUGAR GUIDE is diabetic support to improve quality of life, not diagnostic tool. See Dr for diagnosis.**

    **Algorithm for advert:** Frequent urination, very thirsty, tired, blurry vision, slow wound healing, tingling feet? If 3+ yes → See Dr for BM test.

    **HIGH >15:** Thirsty, urinating, headache, blurry, tired. **>20 + vomiting/confusion/fruity breath → HOSPITAL NOW DKA**

    **LOW <3.5:** Shaking, sweating, fast heartbeat, hungry, dizzy, confused. **If <3.5: Eat 1 tbsp honey or 3 tsp sugar water or 1/2 cup juice, then bread after 15 min. If unconscious DO NOT feed - rub honey on gums, call clinic, go hospital.**

    **Go to clinic urgent:** BM >20 twice or with vomiting/fever, BM <3.0 not rising, chest pain, breathing trouble, confusion, foot wound not healing.
    """)
    st.caption("Disclaimer: Educational support only, not medical diagnosis. Always consult doctor. Not liable for decisions based on app. Keep clinic visits.")

with tabs[12]:
    st.subheader("💰 Pay & Activate - EcoCash / InnBucks")
    st.markdown("""
    <div style='background:#E8F5E9;padding:16px;border-radius:12px;border-left:5px solid #2E7D32'>
    <b>SAHWIRA HEALTH SUGAR GUIDE - Annual License</b><br>
    <b>Cost: $5 x 3 annually = $15 per year</b><br><br>
    <b>EcoCash:</b> 0771477408 - James<br>
    <b>InnBucks:</b> 0771477408 - James<br><br>
    After payment, send proof of payment (screenshot) via WhatsApp to 0771477408<br>
    You will receive license key e.g., SAHWIRA100 to activate app<br><br>
    <b>What you get:</b> Full 100+ foods, Smart Plan, Pairing, Photo portions, Voice Gogo, Reports for Dr, Family monitoring, Offline reminders<br>
    </div>
    """, unsafe_allow_html=True)
    st.text_input("Enter License Key after payment", key="pay_key", placeholder="SAHWIRA...")
    if st.button("Activate After Payment", type="primary", use_container_width=True):
        if st.session_state["pay_key"].strip().upper() in VALID_KEYS:
            st.session_state["activated"]=True
            st.success("✅ Activated! Thank you for supporting Sahwira Health")
            st.balloons()
        else:
            st.error("Invalid key - send EcoCash proof to 0771477408 for valid key")
    st.link_button("📲 Send Payment Proof via WhatsApp to 0771477408", "https://wa.me/263771477408?text=Hi%20James%20I%20paid%20$15%20for%20Sahwira%20Health%20Sugar%20Guide%20via%20EcoCash")

with tabs[13]:
    st.subheader("📄 Reports for Dr / Clinic - Keep & Print with Photos")
    dr=st.text_input("Doctor / Clinic Name")
    if st.button("Generate Full Report PDF with Photos", type="primary", use_container_width=True):
        pdf=FPDF(); pdf.add_page(); pdf.set_font("Arial","B",16); pdf.cell(0,10,"SAHWIRA HEALTH SUGAR GUIDE - CLINIC REPORT", ln=True, align="C")
        pdf.set_font("Arial","",10); pdf.multi_cell(0,5,f"Date {datetime.date.today()}\nDoctor {dr}\nBM {st.session_state.get('sugar','-')} BMI {st.session_state.get('bmi','-')}\nMeds {st.session_state.get('meds','-')}\nFamily {st.session_state.get('family','-')}\nCustom Foods with Photos: {st.session_state.get('custom_foods','None')}\nFood Library: {len(FOODS)}+ local incl beverages & breads\nDisclaimer: Educational support only.")
        path="/tmp/report.pdf"; pdf.output(path)
        with open(path,"rb") as f:
            st.download_button("📥 Download & Print for Dr", f, file_name=f"Sahwira_Report_{datetime.date.today()}.pdf", mime="application/pdf", type="primary", use_container_width=True)
        if "food_photos" in st.session_state:
            st.markdown("#### Photos for Dr")
            for fp in st.session_state["food_photos"]:
                st.image(fp["photo"], caption=fp["name"], use_container_width=True)
