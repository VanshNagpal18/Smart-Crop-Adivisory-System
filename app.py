import streamlit as st
import pandas as pd
from sklearn.tree import DecisionTreeClassifier
import plotly.express as px

# -------------------------------
# Load Dataset & Train Model
# -------------------------------
data = pd.read_csv("crop_data.csv")

X = data[["temperature", "humidity", "ph", "rainfall"]]
y = data["crop"]

model = DecisionTreeClassifier()
model.fit(X, y)

# -------------------------------
# Streamlit Page Settings
# -------------------------------
st.set_page_config(page_title="Smart Crop Advisor 🌿", page_icon="🌾", layout="wide")

# Custom CSS for styling
st.markdown("""
    <style>
     body {
        background: linear-gradient(to bottom right, #e7f5dc, #c2e59c);
        color: #1b4332;
        font-family: 'Segoe UI', sans-serif;
    }
    .main-title {
        text-align: center;
        color: #2d6a4f;
        font-size: 38px;
        font-weight: 700;
        margin-bottom: 5px;
        background: linear-gradient(90deg, #38b000, #70e000);
    }
    .subtitle {
        text-align: center;
        color: #40916c;
        font-size: 18px;
        background: linear-gradient(90deg, #38b000, #70e000);
        margin-bottom: 30px;
    }

    /* Buttons */
    .stButton>button {
        background: linear-gradient(90deg, #38b000, #70e000);
        color: white;
        border-radius: 12px;
        height: 3em;
        width: 100%;
        font-size: 17px;
        border: none;
        font-weight: 600;
        transition: 0.3s ease;
    }

    .stButton>button:hover {
        background: linear-gradient(90deg, #008000, #38b000);
        transform: scale(1.05);
    }

    /* Footer */
    .footer {
        text-align: center;
        background: linear-gradient(90deg, #38b000, #70e000);
        color: #2d6a4f;
        font-size: 15px;
        margin-top: 40px;
        padding: 10px;
        border-top: 1px solid #95d5b2;
    }

    </style>
""", unsafe_allow_html=True)

# -------------------------------
# Header
# -------------------------------
st.markdown('<div class="main-title">🌾 GrowWise</div>', unsafe_allow_html=True) 
st.markdown('<div class="subtitle">Smart Crop Advisory System</div>', unsafe_allow_html=True)
st.divider()

# -------------------------------
# Input Fields
# -------------------------------
st.markdown("### 🌱 Enter Field Conditions")
col1, col2 = st.columns(2)
with col1:
    temp = st.slider("🌡️ Temperature (°C)", 10, 45, 25)
    ph = st.slider("🌿 Soil pH", 4.0, 8.5, 6.5)
with col2:
    humidity = st.slider("💧 Humidity (%)", 30, 100, 70)
    rainfall = st.slider("🌧️ Rainfall (mm)", 50, 300, 150)

# -------------------------------
# Predict Button
# -------------------------------
if st.button("🚀 Predict Best Crop"):
    crop = model.predict([[temp, humidity, ph, rainfall]])[0]
    st.success(f"🌿 Recommended Crop: **{crop.upper()}**")

    # Fertilizer suggestions
    fertilizers = {
        "rice": "Urea (N), DAP (P), MOP (K)",
        "wheat": "Urea, DAP, Potash",
        "maize": "DAP, MOP, Nitrogen",
        "sugarcane": "NPK 12:32:16",
        "cotton": "NPK 10:26:26",
        "barley": "Urea, Phosphate fertilizers",
        "millet": "Nitrogen-rich fertilizers",
        "coffee": "Compost + NPK",
        "tea": "Organic manure + NPK",
        "pulses": "Phosphorus-rich fertilizers"
    }
    st.info(f"📋 **Fertilizer Advice:** {fertilizers.get(crop, 'Balanced NPK recommended')}")

# -------------------------------
# AI Chatbot (Rule-Based)
# -------------------------------
st.markdown("### 💬 Ask Farming Questions")
user_query = st.text_input("Type your question here:")

if user_query:
    query = user_query.lower()
    response = "Sorry, I can only answer crop-related queries. Please ask about crops or soil."
    
    # Simple rule-based logic
    if "high rainfall" in query or "humid" in query:
        response = "Rice and sugarcane are suitable for high rainfall and humid conditions."
    elif "dry" in query or "low rainfall" in query:
        response = "Cotton, millet, and pulses grow well in dry or low rainfall areas."
    elif "acidic soil" in query or "ph < 6" in query:
        response = "Tea prefers acidic soil conditions."
    elif "neutral soil" in query or "ph 6-7" in query:
        response = "Wheat, maize, and rice grow well in neutral soil."
    elif "high temperature" in query or "hot" in query:
        response = "Millet, cotton, and maize prefer hot climates."
    elif "hi" in query or "hello" in query:
        response = "Hello Sir, Tell Me Your Query."
    elif "what is this" in query or "growwise" in query:
        response = "GrowWise, It is an AI-powered Crop Advisiory System."
    elif "who made you" in query or "name the developer" in query:
        response = "GrowWise is Developed By Vansh Nagpal in 2025."
    elif "is it useful" in query or "is it practical to use" in query:
        response = "Yes, It is."
    
    st.info(f"🤖 Chatbot Response: {response}")

# -------------------------------
# Data Visualization
# -------------------------------
st.markdown("### 📊 Crop Data Visualization")

# Crop count bar chart
crop_count = data['crop'].value_counts().reset_index()
crop_count.columns = ['Crop', 'Count']
fig1 = px.bar(crop_count, x='Crop', y='Count', color='Crop', title="Crop Distribution in Dataset",
              color_discrete_sequence=px.colors.sequential.Greens)
st.plotly_chart(fig1, use_container_width=True)

# Temperature vs Rainfall scatter
fig2 = px.scatter(data, x="temperature", y="rainfall", color="crop",
                  size="humidity", title="Temperature vs Rainfall (Bubble=Humidity)",
                  color_discrete_sequence=px.colors.sequential.Greens)
st.plotly_chart(fig2, use_container_width=True)

# -------------------------------
# Footer
# -------------------------------
st.markdown("""
<div class="footer">
🌱 <b>Smart Crop Advisor</b> | Developed by Vansh Nagpal</b><br>
© 2025, GrowWise- AI powered Crop Recommendation 🌾
</div>
""", unsafe_allow_html=True)








