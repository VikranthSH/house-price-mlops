import streamlit as st
import requests
import os

# API URL from environment variable or default to localhost
API_URL = os.getenv("API_URL", "http://localhost:8000")

# Page configuration
st.set_page_config(
    page_title="Bangalore House Price Predictor",
    page_icon="🏠",
    layout="wide"
)

# Custom CSS
st.markdown("""
    <style>
    .main {
        padding: 2rem;
    }
    .stButton>button {
        width: 100%;
        background-color: #FF4B4B;
        color: white;
        font-weight: bold;
        padding: 0.5rem;
        border-radius: 0.5rem;
    }
    .prediction-box {
        padding: 2rem;
        border-radius: 1rem;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        text-align: center;
        margin: 2rem 0;
    }
    .prediction-value {
        font-size: 3rem;
        font-weight: bold;
        margin: 1rem 0;
    }
    </style>
    """, unsafe_allow_html=True)

# Title and description
st.title("🏠 Bangalore House Price Prediction")
st.markdown("### Predict house prices in Bangalore using Machine Learning")

# Sidebar
with st.sidebar:
    st.header("ℹ️ About")
    st.info(
        "This application predicts house prices in Bangalore based on:\n"
        "- Location\n"
        "- Square Feet\n"
        "- Number of Bathrooms\n"
        "- Number of Bedrooms (BHK)"
    )
    
    st.header("🔗 API Status")
    try:
        response = requests.get(f"{API_URL}/health", timeout=5)
        if response.status_code == 200:
            st.success("✅ API is running")
        else:
            st.error("❌ API is not responding")
    except:
        st.error("❌ Cannot connect to API")

# Main content
col1, col2 = st.columns([2, 1])

with col1:
    st.header("📝 Enter Property Details")
    
    # Fetch available locations
    try:
        locations_response = requests.get(f"{API_URL}/locations", timeout=5)
        if locations_response.status_code == 200:
            locations = locations_response.json()
        else:
            locations = ["Whitefield", "Electronic City", "Hebbal"]
            st.warning("Using default locations. API may not be available.")
    except:
        locations = ["Whitefield", "Electronic City", "Hebbal"]
        st.warning("Using default locations. Cannot connect to API.")
    
    # Input form
    with st.form("prediction_form"):
        location = st.selectbox(
            "📍 Select Location",
            options=locations,
            help="Choose the location of the property"
        )
        
        col_input1, col_input2 = st.columns(2)
        
        with col_input1:
            sqft = st.number_input(
                "📐 Total Square Feet",
                min_value=300,
                max_value=30000,
                value=1500,
                step=50,
                help="Total area of the property in square feet"
            )
            
            bhk = st.slider(
                "🛏️ Number of Bedrooms (BHK)",
                min_value=1,
                max_value=10,
                value=3,
                help="Number of bedrooms"
            )
        
        with col_input2:
            bath = st.slider(
                "🚿 Number of Bathrooms",
                min_value=1,
                max_value=10,
                value=2,
                help="Number of bathrooms"
            )
        
        submitted = st.form_submit_button("🔮 Predict Price")
    
    if submitted:
        # Prepare request
        payload = {
            "location": location,
            "sqft": float(sqft),
            "bath": int(bath),
            "bhk": int(bhk)
        }
        
        # Make prediction
        with st.spinner("Predicting..."):
            try:
                response = requests.post(
                    f"{API_URL}/predict",
                    json=payload,
                    timeout=10
                )
                
                if response.status_code == 200:
                    result = response.json()
                    predicted_price = result["predicted_price"]
                    
                    # Display prediction
                    st.markdown(
                        f"""
                        <div class="prediction-box">
                            <h2>Predicted Price</h2>
                            <div class="prediction-value">₹ {predicted_price:.2f} Lakhs</div>
                            <p>≈ ₹ {predicted_price * 100000:,.0f}</p>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
                    
                    # Additional details
                    st.success("✅ Prediction successful!")
                    
                    col_detail1, col_detail2, col_detail3, col_detail4 = st.columns(4)
                    
                    with col_detail1:
                        st.metric("Location", location)
                    with col_detail2:
                        st.metric("Area", f"{sqft} sq ft")
                    with col_detail3:
                        st.metric("Bedrooms", f"{bhk} BHK")
                    with col_detail4:
                        st.metric("Bathrooms", bath)
                    
                    # Price per sqft
                    price_per_sqft = (predicted_price * 100000) / sqft
                    st.info(f"💰 Price per sq ft: ₹ {price_per_sqft:,.0f}")
                    
                else:
                    st.error(f"❌ Error: {response.json().get('detail', 'Unknown error')}")
                    
            except requests.exceptions.RequestException as e:
                st.error(f"❌ Cannot connect to API: {str(e)}")
            except Exception as e:
                st.error(f"❌ An error occurred: {str(e)}")

with col2:
    st.header("📊 Quick Stats")
    
    # Example predictions
    st.subheader("Example Prices")
    
    examples = [
        {"name": "1 BHK Apartment", "sqft": 600, "bhk": 1, "bath": 1},
        {"name": "2 BHK Apartment", "sqft": 1200, "bhk": 2, "bath": 2},
        {"name": "3 BHK House", "sqft": 1800, "bhk": 3, "bath": 3},
        {"name": "4 BHK Villa", "sqft": 3000, "bhk": 4, "bath": 4}
    ]
    
    for example in examples:
        with st.expander(f"📦 {example['name']}"):
            st.write(f"- Area: {example['sqft']} sq ft")
            st.write(f"- Bedrooms: {example['bhk']}")
            st.write(f"- Bathrooms: {example['bath']}")

# Footer
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center'>
        <p>Built with ❤️ using Streamlit & FastAPI | MLOps Project</p>
    </div>
    """,
    unsafe_allow_html=True
)