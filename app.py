"""
ClaimEquity AI - Insurance Justice Engine
Main Streamlit application for hackathon submission
"""
import streamlit as st
import os
from utils import (
    parse_claim, summarize_claim, detect_bias, init_db, 
    add_anon_data, get_claim_features
)
from models import (
    train_appeal_predictor, load_appeal_predictor, predict_appeal,
    dedalus_agent_summarize, grok_real_time_analysis,
    knot_payment_link, capital_one_impact, amplitude_track_event
)

# Page configuration
st.set_page_config(
    page_title="ClaimEquity AI",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 1rem;
    }
    .subtitle {
        text-align: center;
        color: #666;
        margin-bottom: 2rem;
    }
    .stButton>button {
        width: 100%;
        background-color: #1f77b4;
        color: white;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize session state
if 'db_initialized' not in st.session_state:
    st.session_state.db_initialized = False
if 'model_loaded' not in st.session_state:
    st.session_state.model_loaded = False
if 'model' not in st.session_state:
    st.session_state.model = None
if 'db_conn' not in st.session_state:
    st.session_state.db_conn = None

# Auto-initialize database on first load
if not st.session_state.db_initialized:
    try:
        st.session_state.db_conn = init_db()
        st.session_state.db_initialized = True
    except Exception as e:
        st.session_state.db_conn = None

# Header
st.markdown('<h1 class="main-header">⚖️ ClaimEquity AI</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Insurance Justice Engine | Healthcare Equity Platform</p>', unsafe_allow_html=True)

# Sidebar for API keys and settings
with st.sidebar:
    st.header("🔑 API Configuration")
    st.caption("Configure API keys for enhanced features")
    
    openai_key = st.text_input("OpenAI API Key", type="password", help="For claim summarization")
    dedalus_key = st.text_input("Dedalus Labs API Key", type="password", help="For AI agent appeal generation")
    # Get xAI key from environment variable or user input
    default_xai_key = os.getenv('XAI_API_KEY', '')
    xai_key = st.text_input("xAI (Grok) API Key", type="password", value=default_xai_key, help="For claim summarization and real-time bias analysis")
    knot_key = st.text_input("Knot API Key", type="password", help="For payment links")
    cap_one_key = st.text_input("Capital One API Key", type="password", help="For financial impact")
    amplitude_key = st.text_input("Amplitude API Key", type="password", help="For analytics")
    
    st.divider()
    st.header("📊 Settings")
    use_xai = st.checkbox("Use xAI Grok for Summarization", value=bool(xai_key), help="Uses your xAI credits for better summaries")
    use_openai = st.checkbox("Use OpenAI for Summarization", value=False, help="Alternative to xAI")
    enable_analytics = st.checkbox("Enable Analytics", value=bool(amplitude_key))
    
    # Database status
    if st.session_state.db_initialized:
        st.success("✅ Database initialized")
    else:
        if st.button("Initialize Database"):
            try:
                st.session_state.db_conn = init_db()
                st.session_state.db_initialized = True
                st.success("✅ Database initialized!")
            except Exception as e:
                st.error(f"Database initialization error: {e}")
    
    st.divider()
    st.caption("Built for HackPrinceton Fall 2025")
    st.caption("Healthcare Track | AI Innovation | Financial Hack")

# Main content tabs
tab1, tab2, tab3, tab4 = st.tabs(["📄 Claim Analysis", "🔮 Appeal Prediction", "🚨 Bias Detection", "📝 Appeal Generator"])

# Tab 1: Claim Analysis
with tab1:
    st.header("Upload & Analyze Insurance Claim")
    
    uploaded_file = st.file_uploader(
        "Upload Claim PDF",
        type=['pdf'],
        help="Upload your insurance claim denial document"
    )
    
    if uploaded_file:
        # Parse claim
        with st.spinner("Parsing claim document..."):
            claim_text = parse_claim(uploaded_file)
        
        if claim_text and not claim_text.startswith("Error"):
            st.success("✅ Claim parsed successfully!")
            
            # Display raw text (truncated)
            with st.expander("📋 View Raw Claim Text"):
                st.text(claim_text[:2000] + "..." if len(claim_text) > 2000 else claim_text)
            
            # Summarize
            st.subheader("📝 Claim Summary")
            with st.spinner("Generating summary with xAI Grok..." if use_xai else "Generating summary..."):
                summary = summarize_claim(
                    claim_text,
                    use_openai=use_openai and bool(openai_key),
                    api_key=openai_key if use_openai else None,
                    use_xai=use_xai and bool(xai_key),
                    xai_key=xai_key if use_xai else None
                )
                if use_xai:
                    st.success("✅ Summary generated using xAI Grok API")
                st.write(summary)
            
            # Extract features for ML
            claim_features = get_claim_features(claim_text)
            
            # Store in session state
            st.session_state.claim_text = claim_text
            st.session_state.claim_features = claim_features
            
            # Track event
            if enable_analytics and amplitude_key:
                amplitude_track_event("claim_analyzed", properties={"text_length": len(claim_text)}, api_key=amplitude_key)
        else:
            st.error(f"Error parsing PDF: {claim_text}")

# Tab 2: Appeal Prediction
with tab2:
    st.header("🔮 Predict Appeal Success Probability")
    st.caption("ML-powered prediction based on claim characteristics and demographics")
    
    # Load or train model
    if not st.session_state.model_loaded:
        with st.spinner("Loading ML model..."):
            st.session_state.model = load_appeal_predictor()
            st.session_state.model_loaded = True
    
    # User input form
    col1, col2, col3 = st.columns(3)
    
    with col1:
        age = st.number_input("Age", min_value=18, max_value=100, value=45, step=1)
    
    with col2:
        zip_code = st.text_input("Zip Code", value="08540", help="5-digit zip code")
    
    with col3:
        claim_amount = st.number_input("Claim Amount ($)", min_value=0.0, value=5000.0, step=100.0)
    
    # Additional inputs
    has_prior_auth = st.checkbox("Has Prior Authorization", value=False)
    denial_reason = st.selectbox(
        "Denial Reason",
        ["Missing Documentation", "Not Medically Necessary", "Out of Network", "Prior Auth Required", "Other"]
    )
    
    if st.button("🔮 Predict Appeal Success", type="primary"):
        if st.session_state.model:
            user_data = {
                'age': age,
                'zip': int(zip_code) if zip_code.isdigit() else 10000,
                'amount': claim_amount,
                'demo': f"age_{age//10*10}"  # Age group
            }
            
            # Get claim features if available
            claim_features = st.session_state.get('claim_features', {})
            if has_prior_auth:
                claim_features['has_prior_auth'] = 1
            
            with st.spinner("Running prediction..."):
                success_prob = predict_appeal(
                    st.session_state.model,
                    user_data,
                    claim_features
                )
            
            # Display result
            st.metric("Appeal Success Probability", f"{success_prob}%")
            
            # Visual indicator
            if success_prob >= 70:
                st.success("✅ High chance of success! Consider filing an appeal.")
            elif success_prob >= 50:
                st.warning("⚠️ Moderate chance. Appeal may be worth pursuing.")
            else:
                st.error("❌ Low probability. Consider gathering more documentation first.")
            
            # Financial impact
            st.subheader("💰 Financial Impact")
            financial_impact = capital_one_impact(claim_amount, cap_one_key)
            st.info(financial_impact.get('impact', f"Out-of-pocket cost: ${claim_amount:,.2f}"))
            
            # Track event
            if enable_analytics and amplitude_key:
                amplitude_track_event(
                    "appeal_predicted",
                    properties={"success_prob": success_prob, "claim_amount": claim_amount},
                    api_key=amplitude_key
                )
        else:
            st.error("Model not loaded. Please refresh the page.")

# Tab 3: Bias Detection
with tab3:
    st.header("🚨 Bias Detection Engine")
    st.caption("Anonymized pattern analysis to detect systemic biases in claim denials")
    
    # Get database connection
    conn = st.session_state.get('db_conn')
    if not conn:
        try:
            conn = init_db()
            st.session_state.db_conn = conn
            st.session_state.db_initialized = True
        except Exception as e:
            st.error(f"Database error: {e}")
            st.stop()
    
    # User demographics for bias check
    st.subheader("Your Demographics (for bias check)")
    col1, col2 = st.columns(2)
    
    with col1:
        check_zip = st.text_input("Zip Code", value="08540", key="bias_zip")
        check_demo = st.selectbox(
            "Demographic Group",
            ["age_40-50", "age_50-60", "age_60-70", "age_70+", "other"],
            key="bias_demo"
        )
    
    with col2:
        check_amount = st.number_input("Claim Amount", value=5000.0, key="bias_amount")
        check_outcome = st.selectbox("Outcome", ["Denied", "Approved"], key="bias_outcome")
    
    # Opt-in data sharing
    st.subheader("📊 Contribute to Bias Detection")
    st.caption("Anonymized data helps identify systemic patterns. All data is hashed and cannot be traced to you.")
    
    if st.button("🔒 Opt-in: Share Anonymized Data"):
        anon_data = {
            'reason': 'denied' if check_outcome == "Denied" else 'approved',
            'zip': check_zip,
            'demo': check_demo,
            'amount': check_amount,
            'outcome': 0 if check_outcome == "Denied" else 1
        }
        add_anon_data(conn, anon_data)
        st.success("✅ Data added (anonymized and hashed)")
        
        if enable_analytics and amplitude_key:
            amplitude_track_event("data_shared", properties={"demo": check_demo}, api_key=amplitude_key)
    
    # Detect bias
    if st.button("🔍 Detect Bias Patterns"):
        user_data = {
            'zip': check_zip,
            'demo': check_demo
        }
        
        with st.spinner("Analyzing patterns..."):
            bias_msg, figure_path = detect_bias(conn, user_data)
        
        st.markdown(f"### {bias_msg}")
        
        if figure_path and os.path.exists(figure_path):
            st.image(figure_path, caption="Bias Pattern Visualization")
        
        # Real-time Grok analysis
        if xai_key:
            st.subheader("🤖 Real-Time Grok Analysis")
            grok_query = f"Analyze current insurance denial trends and bias patterns for zip code {check_zip} and demographic {check_demo} in healthcare claims."
            with st.spinner("Querying Grok for real-time insights..."):
                grok_insights = grok_real_time_analysis(grok_query, xai_key)
                st.info(grok_insights)
        
        if enable_analytics and amplitude_key:
            amplitude_track_event("bias_detected", properties={"demo": check_demo}, api_key=amplitude_key)

# Tab 4: Appeal Generator
with tab4:
    st.header("📝 AI-Powered Appeal Letter Generator")
    st.caption("Generate professional appeal letters using AI agents")
    
    # Check if claim is available
    if 'claim_text' not in st.session_state:
        st.warning("⚠️ Please upload and analyze a claim first (go to 'Claim Analysis' tab)")
        st.info("You can still generate a template appeal letter below.")
        claim_text_for_appeal = ""
    else:
        claim_text_for_appeal = st.session_state.claim_text
        st.success("✅ Using analyzed claim data")
    
    # Appeal customization
    st.subheader("Appeal Details")
    patient_name = st.text_input("Patient Name", value="[Your Name]")
    insurance_company = st.text_input("Insurance Company", value="[Insurance Company]")
    policy_number = st.text_input("Policy Number", value="[Policy Number]")
    additional_notes = st.text_area("Additional Notes/Arguments", value="")
    
    if st.button("✨ Generate Appeal Letter", type="primary"):
        if claim_text_for_appeal or additional_notes:
            # Combine claim text with additional notes
            full_context = f"{claim_text_for_appeal}\n\nAdditional Notes: {additional_notes}"
            
            with st.spinner("Generating appeal letter with AI agent..."):
                appeal_letter = dedalus_agent_summarize(full_context, dedalus_key)
            
            st.subheader("📄 Generated Appeal Letter")
            st.markdown(appeal_letter)
            
            # Download button
            st.download_button(
                label="📥 Download Appeal Letter",
                data=appeal_letter,
                file_name="appeal_letter.txt",
                mime="text/plain"
            )
            
            # Payment link (if appeal fee required)
            st.subheader("💳 Appeal Fee Payment")
            appeal_fee = st.number_input("Appeal Fee Amount", value=50.0, min_value=0.0)
            
            if st.button("🔗 Generate Payment Link (Knot API)"):
                if knot_key:
                    payment_info = knot_payment_link(
                        appeal_fee,
                        f"Appeal fee for {insurance_company}",
                        knot_key
                    )
                    if payment_info.get('link'):
                        st.success(f"Payment link: {payment_info['link']}")
                    else:
                        st.info("Payment link generation (sandbox mode)")
                else:
                    st.warning("Knot API key required for payment links")
            
            if enable_analytics and amplitude_key:
                amplitude_track_event("appeal_generated", properties={"has_claim": bool(claim_text_for_appeal)}, api_key=amplitude_key)
        else:
            st.error("Please provide claim text or additional notes")

# Footer
st.divider()
st.markdown("""
<div style='text-align: center; color: #666; padding: 2rem;'>
    <p><strong>ClaimEquity AI</strong> | Built for Healthcare Equity</p>
    <p>HackPrinceton Fall 2025 | Healthcare Track</p>
    <p>Eligible for: Best Practical AI Innovation, Best Financial Hack, Best Use of Dedalus, Best Predictive Intelligence, Best Use of Grok</p>
</div>
""", unsafe_allow_html=True)

