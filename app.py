import streamlit as st
import pandas as pd

st.title("🥗 Smart AI Diet & Grocery Planner")
st.write("Class 12 AI Annual Practical Project (SDG 3 & SDG 12)")

# --- 1. SIDEBAR INPUTS (User Profile & Constraints) ---
st.sidebar.header("User Profile & Preferences")

age = st.sidebar.slider("Age", 10, 80, 18)
gender = st.sidebar.selectbox("Gender", ["Male", "Female"])
weight = st.sidebar.number_input("Weight (kg)", value=65.0)
height = st.sidebar.number_input("Height (cm)", value=175.0)
activity = st.sidebar.selectbox("Work / Activity Intensity", 
                                ["Sedentary (Little/no exercise)", 
                                 "Lightly Active (Light exercise/study)", 
                                 "Moderately Active (Daily exercise)"])

diet_type = st.sidebar.selectbox("Dietary Preference", ["Veg", "Non-Veg", "Vegan"])
budget = st.sidebar.selectbox("Budget Tier", ["Low", "Medium", "High"])
allergy = st.sidebar.selectbox("Allergy Restriction", ["None", "Dairy", "Gluten", "Nuts"])

# Social Event Toggle
party_mode = st.sidebar.checkbox("🎉 Attending a Party / Eating Out Today?")

# --- 2. CALORIE & NUTRITION ENGINE ---
# Activity multiplier logic
if "Sedentary" in activity:
    mult = 1.2
elif "Lightly" in activity:
    mult = 1.375
else:
    mult = 1.55

# Mifflin-St Jeor BMR calculation
if gender == "Male":
    bmr = (10 * weight) + (6.25 * height) - (5 * age) + 5
else:
    bmr = (10 * weight) + (6.25 * height) - (5 * age) - 161

tdee = bmr * mult

if party_mode:
    tdee += 300  # Adjust calorie target for social dining buffer
    st.sidebar.warning("Party Mode Active: Adjusted calorie buffer applied!")

st.subheader("📊 Your Daily Nutritional Targets")
col1, col2, col3 = st.columns(3)
col1.metric("Daily Calorie Target", f"{tdee:.0f} kcal")
col2.metric("Target Protein", f"{(weight * 1.2):.1f} g")
col3.metric("Estimated Water", "3.0 Liters")

# --- 3. LOAD DATASET & FILTER MEALS ---
# In your actual app, ensure 'foods.csv' is uploaded in the same folder
try:
    df = pd.read_csv('foods.csv')
except FileNotFoundError:
    st.error("Please ensure 'foods.csv' is uploaded to your project directory.")
    st.stop()

# Filtering logic
valid_foods = df[
    (df['diet_type'].isin([diet_type, 'Vegan'])) & 
    (df['budget_tier'] == budget)
]

if allergy != "None":
    valid_foods = valid_foods[~valid_foods['allergens'].str.contains(allergy, case=False, na=False)]

st.markdown("---")
st.subheader("📅 Your 7-Day Smart Meal Plan Preview")
if not valid_foods.empty:
    st.dataframe(valid_foods[['name', 'category', 'serving_size', 'calories', 'protein_g', 'calcium_mg']])
else:
    st.info("No exact matches found for your strict budget/allergy filter. Showing general options:")
    st.dataframe(df.head(5))

# --- 4. AUTO-GENERATED GROCERY LIST ---
st.markdown("---")
st.subheader("🛒 Automated 7-Day Grocery Shopping List")
st.write("To avoid the 'I don't have ingredients' excuse, here is your consolidated shopping list based on the weekly plan:")

if not valid_foods.empty:
    grocery_list = valid_foods[['name', 'category', 'serving_size']].drop_duplicates()
    st.table(grocery_list)
else:
    st.write("Complete your profile settings to generate the grocery list.")