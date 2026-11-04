import streamlit as st
import pandas as pd
import os

st.title("🥗 Smart AI Diet & Grocery Planner")
st.write("Class 12 AI Annual Practical Project (SDG 3 & SDG 12)")

# --- 0. ENSURE DATASET EXISTS (Fixes Red Missing File Errors) ---
csv_filename = 'foods.csv'

if not os.path.exists(csv_filename):
    # Built-in fallback data so the app never shows a red error if csv is missing
    fallback_data = {
        'food_id': [101, 102, 103, 104, 105, 106, 107, 108],
        'name': ['Oats with Milk', 'Boiled Eggs (2 pcs)', 'Moong Dal (Cooked)', 'Whole Wheat Roti', 'Paneer Tikka', 'Spinach Tomato Salad', 'Taco Bell Soft Chicken Taco', 'Almonds'],
        'category': ['Breakfast', 'Breakfast', 'Main Course', 'Main Course', 'Main Course', 'Snack', 'Fast Food', 'Snack'],
        'serving_size': ['1 bowl (250g)', '2 eggs (100g)', '1 bowl (200g)', '1 piece (40g)', '100g', '150g', '1 taco (120g)', '1 handful (30g)'],
        'calories': [220, 155, 180, 104, 260, 45, 170, 170],
        'protein_g': [10.5, 12.6, 12.0, 3.1, 18.0, 3.0, 12.0, 6.0],
        'carbs_g': [34.0, 1.1, 28.0, 22.0, 6.0, 7.0, 16.0, 6.0],
        'fats_g': [4.5, 10.6, 2.5, 0.5, 18.0, 0.5, 6.0, 14.0],
        'fiber_g': [4.0, 0.0, 6.5, 2.8, 1.0, 3.2, 2.0, 3.5],
        'calcium_mg': [240, 50, 45, 15, 480, 120, 80, 75],
        'vitamin_d_iu': [40, 82, 0, 0, 12, 0, 0, 0],
        'iron_mg': [1.8, 1.2, 2.5, 0.9, 0.4, 3.1, 1.1, 1.0],
        'vitamin_c_mg': [0.0, 0.0, 2.0, 0.0, 4.0, 28.0, 1.5, 0.0],
        'budget_tier': ['Low', 'Low', 'Low', 'Low', 'Medium', 'Low', 'Medium', 'High'],
        'diet_type': ['Veg', 'Non-Veg', 'Vegan', 'Vegan', 'Veg', 'Vegan', 'Non-Veg', 'Vegan'],
        'allergens': ['Dairy', 'None', 'None', 'Gluten', 'Dairy', 'None', 'Gluten', 'Nuts']
    }
    df_fallback = pd.DataFrame(fallback_data)
    df_fallback.to_csv(csv_filename, index=False)

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

# Social Event / Party Toggle
party_mode = st.sidebar.checkbox("🎉 Attending a Party / Eating Out Today?")

# --- 2. CALORIE & NUTRITION ENGINE ---
if "Sedentary" in activity:
    mult = 1.2
elif "Lightly" in activity:
    mult = 1.375
else:
    mult = 1.55

if gender == "Male":
    bmr = (10 * weight) + (6.25 * height) - (5 * age) + 5
else:
    bmr = (10 * weight) + (6.25 * height) - (5 * age) - 161

tdee = bmr * mult

if party_mode:
    tdee += 300  # Calorie buffer adjustment for social dining
    st.sidebar.warning("Party Mode Active: Adjusted calorie buffer applied!")

st.subheader("📊 Your Daily Nutritional Targets")
col1, col2, col3 = st.columns(3)
col1.metric("Daily Calorie Target", f"{tdee:.0f} kcal")
col2.metric("Target Protein", f"{(weight * 1.2):.1f} g")
col3.metric("Estimated Water", "3.0 Liters")

# --- 3. LOAD DATASET & FILTER MEALS ---
df = pd.read_csv(csv_filename)

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
    st.info("Showing general meal options based on your filters:")
    st.dataframe(df.head(5))

# --- 4. AUTO-GENERATED GROCERY LIST ---
st.markdown("---")
st.subheader("🛒 Automated 7-Day Grocery Shopping List")
st.write("To avoid the 'I don't have ingredients' excuse, here is your consolidated shopping list:")

if not valid_foods.empty:
    grocery_list = valid_foods[['name', 'category', 'serving_size']].drop_duplicates()
    st.table(grocery_list)
else:
    st.write("Complete your profile settings above to generate the grocery list.")
