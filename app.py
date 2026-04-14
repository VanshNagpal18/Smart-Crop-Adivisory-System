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

/* ===== MAIN APP WRAPPER ===== */
.app-container {
    background: linear-gradient(135deg, #d4fc79, #96e6a1);
    padding: 20px;
    border-radius: 15px;
}

/* ===== HEADER ===== */
.app-container .header-box {
    text-align: center;
    padding: 20px;
    border-radius: 15px;
    margin-bottom: 25px;
    background: linear-gradient(90deg, #2d6a4f, #40916c);
    color: white;
    box-shadow: 0px 4px 15px rgba(0,0,0,0.2);
}

.app-container .header-box h1 {
    margin: 0;
    font-size: 42px;
    font-weight: 800;
}

.app-container .header-box p {
    margin: 5px 0 0;
    font-size: 18px;
    color: #d8f3dc;
}

/* ===== INPUT SECTION ===== */
.app-container .stSlider label {
    color: #1b4332 !important;
    font-weight: 600;
}

/* ===== BUTTON ===== */
.app-container .stButton>button {
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

.app-container .stButton>button:hover {
    background: linear-gradient(90deg, #008000, #38b000);
    transform: scale(1.05);
}

/* ===== RESULT BOXES ===== */
.app-container .stSuccess {
    background-color: #d8f3dc !important;
    color: #1b4332 !important;
    border-radius: 10px;
}

.app-container .stInfo {
    background-color: #e9f5db !important;
    color: #1b4332 !important;
    border-radius: 10px;
}

/* ===== CHART CONTAINER ===== */
.app-container .stPlotlyChart {
    background-color: white;
    border-radius: 15px;
    padding: 10px;
}

/* ===== FOOTER ===== */
.app-container .footer {
    text-align: center;
    margin-top: 40px;
    padding: 15px;
    border-radius: 12px;
    background: linear-gradient(90deg, #1b4332, #2d6a4f);
    color: white;
    font-size: 15px;
    box-shadow: 0px -3px 10px rgba(0,0,0,0.2);
}

/* ===== REMOVE STREAMLIT DEFAULT HEADER ===== */
header {visibility: hidden;}
footer {visibility: hidden;}

</style>
""", unsafe_allow_html=True)
st.markdown('<div class="app-container">', unsafe_allow_html=True)

# -------------------------------
# Header
# -------------------------------
st.markdown("""
<div class="header-box">
    <h1>🌾 GrowWise</h1>
    <p>Smart Crop Advisory System</p>
</div>
""", unsafe_allow_html=True)

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
st.markdown('</div>', unsafe_allow_html=True)







