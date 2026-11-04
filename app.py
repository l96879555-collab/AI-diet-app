import streamlit as st
import pandas as pd
import os

st.title("🥗 Smart AI Diet & Grocery Planner")
st.write("Class 12 AI Annual Practical Project (SDG 3 & SDG 12)")

# --- 0. DATASET SETUP ---
csv_filename = 'foods.csv'

if not os.path.exists(csv_filename):
    fallback_data = {
        'food_id': [101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120],
        'name': [
            'Oats with Milk', 'Boiled Eggs (2 pcs)', 'Moong Dal (Cooked)', 'Whole Wheat Roti', 
            'Paneer Tikka', 'Spinach Tomato Salad', 'Taco Bell Soft Chicken Taco', 'Almonds', 
            'Banana Shake', 'Vegetable Poha', 'Masala Omelette', 'Aloo Paratha with Curd', 
            'Chole Bhature', 'Rajma Chawal', 'Chicken Biryani', 'Sprouts Salad', 
            'Apple & Peanut Butter', 'Greek Yogurt with Berries', 'Dal Makhani with Rice', 'Vegetable Khichdi'
        ],
        'category': [
            'Breakfast', 'Breakfast', 'Main Course', 'Main Course', 
            'Main Course', 'Snack', 'Fast Food', 'Snack', 
            'Breakfast', 'Breakfast', 'Breakfast', 'Breakfast', 
            'Main Course', 'Main Course', 'Main Course', 'Snack', 
            'Snack', 'Snack', 'Main Course', 'Main Course'
        ],
        'serving_size': [
            '1 bowl (250g)', '2 eggs (100g)', '1 bowl (200g)', '1 piece (40g)', 
            '100g', '150g', '1 taco (120g)', '1 handful (30g)', 
            '1 glass (300ml)', '1 plate (200g)', '2 eggs (120g)', '2 parathas + 1 cup curd', 
            '1 plate', '1 plate', '1 plate (300g)', '1 bowl (150g)', 
            '1 apple + 2 tbsp PB', '1 bowl (150g)', '1 plate', '1 bowl (250g)'
        ],
        'calories': [220, 155, 180, 104, 260, 45, 170, 170, 250, 190, 210, 420, 550, 400, 480, 120, 280, 160, 520, 240],
        'protein_g': [10.5, 12.6, 12.0, 3.1, 18.0, 3.0, 12.0, 6.0, 8.0, 4.0, 14.0, 10.0, 14.0, 12.0, 24.0, 8.0, 6.0, 12.0, 14.0, 7.0],
        'budget_tier': ['Low', 'Low', 'Low', 'Low', 'Medium', 'Low', 'Medium', 'High', 'Low', 'Low', 'Low', 'Medium', 'Medium', 'Low', 'Medium', 'Low', 'Medium', 'Medium', 'Medium', 'Low'],
        'diet_type': ['Veg', 'Non-Veg', 'Vegan', 'Vegan', 'Veg', 'Vegan', 'Non-Veg', 'Vegan', 'Veg', 'Veg', 'Non-Veg', 'Veg', 'Veg', 'Veg', 'Non-Veg', 'Vegan', 'Veg', 'Veg', 'Veg', 'Vegan'],
        'allergens': ['Dairy', 'None', 'None', 'Gluten', 'Dairy', 'None', 'Gluten', 'Nuts', 'Dairy', 'None', 'None', 'Gluten, Dairy', 'Gluten', 'None', 'Dairy', 'None', 'Nuts', 'Dairy', 'Dairy', 'None'],
        'raw_ingredients': [
            'Rolled Oats (50g), Milk (200ml)', 
            'Eggs (2 pcs)', 
            'Yellow Moong Dal (100g), Spices/Oil', 
            'Whole Wheat Flour / Atta (40g)', 
            'Paneer (100g), Yogurt/Curd, Spices', 
            'Spinach (100g), Tomatoes (50g), Lemon', 
            'Chicken breast, Taco Shells, Lettuce, Cheese', 
            'Almonds (30g)', 
            'Bananas (2 pcs), Milk (250ml)', 
            'Flattened Rice/Poha (80g), Peanuts, Onion, Curry Leaves',
            'Eggs (2 pcs), Onion, Tomato, Green Chili, Oil/Butter',
            'Whole Wheat Flour (100g), Potatoes (150g), Curd (200ml), Spices',
            'Kabuli Chana/Chickpeas (100g), Maida/Refined Flour, Spices, Tomatoes',
            'Kidney Beans / Rajma (100g), Basmati Rice (100g), Onions, Tomatoes',
            'Chicken (150g), Basmati Rice (100g), Curd, Biryani Spices, Ghee',
            'Mixed Sprouts (100g), Cucumber, Tomato, Lemon, Chaat Masala',
            'Apple (1 pc), Peanut Butter (2 tbsp)',
            'Greek Yogurt (150g), Mixed Berries (50g)',
            'Whole Urad Dal & Kidney Beans (100g), Butter/Cream, Basmati Rice (100g)',
            'Rice (60g), Moong Dal (40g), Mixed Vegetables, Turmeric, Ghee'
        ]
    }
    df_fallback = pd.DataFrame(fallback_data)
    df_fallback.to_csv(csv_filename, index=False)

# --- 1. SIDEBAR INPUTS ---
st.sidebar.header("User Profile & Preferences")
age = st.sidebar.slider("Age", 10, 80, 18)
gender = st.sidebar.selectbox("Gender", ["Male", "Female"])
weight = st.sidebar.number_input("Weight (kg)", value=65.0)
height = st.sidebar.number_input("Height (cm)", value=175.0)
activity = st.sidebar.selectbox("Activity Level", ["Sedentary", "Lightly Active", "Moderately Active"])
diet_type = st.sidebar.selectbox("Dietary Preference", ["Veg", "Non-Veg", "Vegan"])
budget = st.sidebar.selectbox("Budget Tier", ["Low", "Medium", "High"])
allergy = st.sidebar.selectbox("Allergy Restriction", ["None", "Dairy", "Gluten", "Nuts"])
party_mode = st.sidebar.checkbox("🎉 Attending a Party / Eating Out Today?")

# --- 2. CALORIE ENGINE ---
mult = 1.2 if "Sedentary" in activity else (1.375 if "Lightly" in activity else 1.55)
bmr = (10 * weight) + (6.25 * height) - (5 * age) + (5 if gender == "Male" else -161)
tdee = (bmr * mult) + (300 if party_mode else 0)

st.subheader("📊 Your Daily Nutritional Targets")
col1, col2, col3 = st.columns(3)
col1.metric("Daily Calorie Target", f"{tdee:.0f} kcal")
col2.metric("Target Protein", f"{(weight * 1.2):.1f} g")
col3.metric("Estimated Water", "3.0 Liters")

# --- 3. FILTER MEALS ---
df = pd.read_csv(csv_filename)

if diet_type == "Veg":
    valid_foods = df[df['diet_type'].isin(['Veg', 'Vegan'])]
elif diet_type == "Vegan":
    valid_foods = df[df['diet_type'] == 'Vegan']
else:
    valid_foods = df.copy()

if allergy != "None":
    valid_foods = valid_foods[~valid_foods['allergens'].str.contains(allergy, case=False, na=False)]

if valid_foods.empty:
    valid_foods = df.copy()

st.markdown("---")
st.subheader("📅 Your 7-Day Smart Meal Plan Preview")
st.dataframe(valid_foods[['name', 'category', 'serving_size', 'calories', 'protein_g']])

# --- 4. SAFE GROCERY LIST GENERATOR ---
st.markdown("---")
st.subheader("🛒 Automated Raw Ingredient Grocery List")

try:
    raw_list = valid_foods['raw_ingredients'].dropna().tolist()
    unique_ingredients = set()
    for item in raw_list:
        for p in str(item).split(','):
            clean_item = p.strip()
            if clean_item:
                unique_ingredients.add(clean_item)
    
    if unique_ingredients:
        grocery_df = pd.DataFrame(sorted(list(unique_ingredients)), columns=["Required Grocery Item"])
        st.table(grocery_df)
    else:
        st.info("No ingredients to display yet.")
except Exception as e:
    st.error(f"Error generating grocery list: {e}")
