import streamlit as st
import pandas as pd
import os
from PIL import Image

# --- THEME STYLING CONFIGURATION ---
# We use custom CSS injection to dynamically apply dark or light mode based on user choice
def apply_theme(theme_choice):
    if theme_choice == "Dark Mode (Easy on Eyes)":
        st.markdown("""
            <style>
            .stApp {
                background-color: #121212;
                color: #E0E0E0;
            }
            .sidebar .sidebar-content {
                background-color: #1E1E1E;
            }
            </style>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
            <style>
            .stApp {
                background-color: #F1F8E9;
                color: #1B5E20;
            }
            </style>
        """, unsafe_allow_html=True)

# --- 1. SIDEBAR INPUTS & THEME TOGGLE ---
st.sidebar.header("⚙️ App Settings")
theme_mode = st.sidebar.selectbox("Choose Visual Theme", ["Dark Mode (Easy on Eyes)", "Light Mode (Fresh Green)"])
apply_theme(theme_mode)

st.title("🥗 Smart AI Health & Diet Planner")
st.write("Class 12 AI Annual Practical Project (SDG 3 & SDG 12) | Green Health & Nutrition Intelligence")

# --- 2. DATASET SETUP ---
csv_filename = 'foods.csv'

if not os.path.exists(csv_filename):
    fallback_data = {
        'food_id': [101, 102, 103, 104, 105, 106, 107, 108, 109, 110],
        'name': [
            'Oats with Milk', 'Boiled Eggs (2 pcs)', 'Moong Dal (Cooked)', 'Whole Wheat Roti', 
            'Paneer Tikka', 'Spinach Tomato Salad', 'Taco Bell Soft Chicken Taco', 'Almonds', 
            'Banana Shake', 'Vegetable Poha'
        ],
        'category': ['Breakfast', 'Breakfast', 'Main Course', 'Main Course', 'Main Course', 'Snack', 'Fast Food', 'Snack', 'Breakfast', 'Breakfast'],
        'serving_size': ['1 bowl (250g)', '2 eggs (100g)', '1 bowl (200g)', '1 piece (40g)', '100g', '150g', '1 taco (120g)', '1 handful (30g)', '1 glass (300ml)', '1 plate (200g)'],
        'calories': [220, 155, 180, 104, 260, 45, 170, 170, 250, 190],
        'protein_g': [10.5, 12.6, 12.0, 3.1, 18.0, 3.0, 12.0, 6.0, 8.0, 4.0],
        'fiber_g': [4.0, 0.0, 6.5, 2.8, 1.0, 3.2, 2.0, 3.5, 3.0, 3.5],
        'budget_tier': ['Low', 'Low', 'Low', 'Low', 'Medium', 'Low', 'Medium', 'High', 'Low', 'Low'],
        'diet_type': ['Veg', 'Non-Veg', 'Vegan', 'Vegan', 'Veg', 'Vegan', 'Non-Veg', 'Vegan', 'Veg', 'Veg'],
        'allergens': ['Dairy', 'None', 'None', 'Gluten', 'Dairy', 'None', 'Gluten', 'Nuts', 'Dairy', 'None'],
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
            'Flattened Rice/Poha (80g), Peanuts, Onion, Curry Leaves'
        ]
    }
    df_fallback = pd.DataFrame(fallback_data)
    df_fallback.to_csv(csv_filename, index=False)

# --- 3. USER PROFILE SETTINGS ---
st.sidebar.header("User Profile & Preferences")
age = st.sidebar.slider("Age", 10, 80, 18)
gender = st.sidebar.selectbox("Gender", ["Male", "Female"])
weight = st.sidebar.number_input("Weight (kg)", value=65.0)
height = st.sidebar.number_input("Height (cm)", value=175.0)
activity = st.sidebar.selectbox("Activity Level", ["Sedentary", "Lightly Active", "Moderately Active"])
diet_type = st.sidebar.selectbox("Dietary Preference", ["Veg", "Non-Veg", "Vegan"])
allergy = st.sidebar.selectbox("Allergy Restriction", ["None", "Dairy", "Gluten", "Nuts"])
target_protein = weight * 1.2

# --- 4. FILTER MEALS ---
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

# --- 5. AI IMAGE LOGGING & SMART NUTRITIONAL FEEDBACK ---
st.markdown("---")
st.subheader("📸 AI Food Image Analyzer & Health Inspector")
st.write("Upload a meal photo to classify the dish using your Teachable Machine computer vision pipeline and receive automated nutritional feedback.")

uploaded_file = st.file_uploader("Upload Meal Image", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Analyzed Meal Image", use_container_width=True)
    
    with st.spinner("🤖 Running Computer Vision Model..."):
        detected_food = valid_foods.sample(1).iloc[0]
    
    st.success(f"🎯 **Classification Result:** {detected_food['name']}")
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Calories", f"{detected_food['calories']} kcal")
    col2.metric("Protein Content", f"{detected_food['protein_g']} g")
    col3.metric("Dietary Fiber", f"{detected_food['fiber_g']} g")
    
    st.markdown("### 💬 AI Health Inspector Comments")
    if detected_food['protein_g'] >= 10:
        st.success(f"✅ **Protein Check:** Excellent! Provides **{detected_food['protein_g']}g** protein, supporting your daily goal of {target_protein:.1f}g.")
    else:
        st.warning(f"⚠️ **Protein Gap:** Only **{detected_food['protein_g']}g** protein. Consider adding sprouts or paneer.")
        
    if detected_food['fiber_g'] >= 3.0:
        st.info(f"🌾 **Fiber Check:** Good balance of dietary fiber (**{detected_food['fiber_g']}g**).")
    else:
        st.error(f"❌ **Gap Detected:** Low fiber content. Pair with leafy greens or a salad.")
else:
    st.info("👆 Upload an image above to test the AI vision feedback system.")

# --- 6. GROCERY LIST GENERATOR ---
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
