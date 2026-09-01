import streamlit as st
import pandas as pd
import datetime
import matplotlib.pyplot as plt
from fpdf import FPDF

st.set_page_config(page_title="Sahwira Sugar Guide", page_icon="💙", layout="wide")

# ================== LICENSE KEY SYSTEM ==================
VALID_KEYS = ["SAHWIRA100", "SAHWIRA200", "SAHWIRA300"]

def check_key():
    st.sidebar.title("🔒 Activate App")
    key = st.sidebar.text_input("Enter your License Key", type="password")
    if st.sidebar.button("Activate"):
        if key in VALID_KEYS:
            st.session_state["activated"] = True
            st.sidebar.success("Activated! Welcome to Sahwira")
            st.experimental_rerun()
        else:
            st.sidebar.error("Invalid Key. Pay via EcoCash 0771477408 to get a key")
    return st.session_state.get("activated", False)

# ================== MAIN APP ==================
if check_key():
    st.title("💙 Sahwira Sugar Guide")
    st.subheader("Take Control of Your Sugar. Together.")
    st.caption("Made for Zimbabwe. Track. Learn. Live Well.")
    
    st.sidebar.header("Menu")
    page = st.sidebar.radio("Go to", ["Home", "Blood Sugar Tracker", "Meal Log", "Reports", "Tips"])

    if page == "Home":
        st.header("Welcome to Sahwira 👋")
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
        st.header("📊 Weekly Report")
        st.write("Your sugar trend will show here once you add 3+ readings.")
        data = pd.DataFrame({
            'Day': ['Mon', 'Tue', 'Wed', 'Thu', 'Fri'],
            'Sugar': [6.5, 7.2, 6.0, 6.8, 6.2]
        })
        fig, ax = plt.subplots()
        ax.plot(data['Day'], data['Sugar'], marker='o')
        ax.set_ylabel("mmol/L")
        ax.set_title("Last 5 Days")
        st.pyplot(fig)
        if st.button("Download PDF Report"):
            st.info("PDF download coming in next update")

    elif page == "Tips":
        st.header("💡 Daily Sugar Tips")
        st.write("1. **Drink Water**: 8 glasses a day helps control sugar")
        st.write("2. **Walk 10 mins**: After meals to lower blood sugar")
        st.write("3. **Check Same Time**: Consistency gives better data")
        st.write("4. **Eat Veggies First**: Helps slow sugar spikes")
        st.warning("If sugar >15 or <4, contact your clinic immediately")

else:
    st.title("💙 Sahwira Sugar Guide")
    st.warning("🔒 Please enter your license key in the sidebar to activate")
    st.write("### How to Buy:")
    st.write("1. EcoCash to: **0771477408**")
    st.write("2. Amount: **$5 for 3 months**")
    st.write("3. WhatsApp me your number and I’ll send your key")
