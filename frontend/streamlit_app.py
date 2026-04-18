"""
STEP 7: Production UI - Streamlit Application

Features:
- Image upload
- Real-time OCR
- Nutrition data extraction
- Health analysis with score
- Diet suitability checker
- Q&A with Qwen LLM
- Product comparison

Installation:
    pip install streamlit pillow

Run:
    streamlit run streamlit_app.py
"""

import streamlit as st
import json
from pathlib import Path
from PIL import Image
from inference.inference import (
    process_image, 
    compare_products,
    analyze_health,
    check_diet
)

# =============================
# PAGE CONFIG
# =============================
st.set_page_config(
    page_title="Nutrition OCR Pro",
    page_icon="🥗",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("🥗 Nutrition OCR Pro - Production Ready")
st.markdown("Extract nutrition data from labels using OCR + AI analysis")

# =============================
# SIDEBAR CONFIG
# =============================
st.sidebar.header("⚙️ Configuration")
mode = st.sidebar.selectbox(
    "Select Mode",
    ["Single Product Analysis", "Product Comparison", "Batch Analysis"]
)

# =============================
# MODE 1: SINGLE PRODUCT ANALYSIS
# =============================
if mode == "Single Product Analysis":
    st.header("📸 Single Product Analysis")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("1️⃣ Upload Image")
        uploaded_file = st.file_uploader(
            "Choose nutrition label image",
            type=["jpg", "jpeg", "png", "bmp"]
        )
        
        if uploaded_file:
            image = Image.open(uploaded_file)
            st.image(image, caption="Uploaded Label", use_column_width=True)
            
            # Save temporarily
            temp_path = f"/tmp/{uploaded_file.name}"
            with open(temp_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
            
            # Process
            with st.spinner("🔍 Analyzing nutrition label..."):
                result = process_image(temp_path)
            
            if result["success"]:
                # Tab 1: Extracted Data
                tab1, tab2, tab3, tab4 = st.tabs(
                    ["📊 Data", "❤️ Health", "🎯 Diet", "💬 Q&A"]
                )
                
                with tab1:
                    st.subheader("Extracted Nutrition Data")
                    
                    # Confidence badge
                    confidence_color = {
                        "high": "🟢",
                        "medium": "🟡",
                        "low": "🔴"
                    }
                    st.write(
                        f"Confidence: {confidence_color[result['confidence']]} "
                        f"{result['confidence'].upper()}"
                    )
                    
                    # Nutrition table
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("Calories", result["data"]["calories"])
                        st.metric("Fat", result["data"]["fat"])
                    with col2:
                        st.metric("Protein", result["data"]["protein"])
                        st.metric("Sodium", result["data"]["sodium"])
                    with col3:
                        st.metric("Carbs", result["data"]["carbs"])
                    
                    # Raw text
                    with st.expander("View extracted text"):
                        st.code(result["text"])
                
                with tab2:
                    st.subheader("❤️ Health Analysis")
                    
                    health = result["health_analysis"]
                    
                    # Score with color
                    score = health["score"]
                    color = "🟢" if score >= 7 else "🟡" if score >= 4 else "🔴"
                    
                    col1, col2 = st.columns([2, 1])
                    with col1:
                        st.write(f"### Health Score: {color} {score}/10")
                        st.write(f"**Recommendation:** {health['recommendation']}")
                    with col2:
                        st.metric("Score", score, delta=health['recommendation'])
                    
                    st.write("### Analysis Factors:")
                    st.write(health["summary"])
                
                with tab3:
                    st.subheader("🎯 Diet Suitability")
                    
                    diet = result["diet_suitability"]
                    
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        status = "✅ Suitable" if diet["keto"] else "❌ Not suitable"
                        st.write(f"### Keto\n{status}")
                    with col2:
                        status = "✅ Suitable" if diet["muscle_gain"] else "❌ Not suitable"
                        st.write(f"### Muscle Gain\n{status}")
                    with col3:
                        status = "✅ Suitable" if diet["diabetic_friendly"] else "❌ Not suitable"
                        st.write(f"### Diabetic Friendly\n{status}")
                
                with tab4:
                    st.subheader("💬 Ask Questions")
                    
                    # Predefined questions
                    predefined = [
                        "Is this healthy?",
                        "Good for weight loss?",
                        "Good for muscle building?",
                        "How much protein does it have?"
                    ]
                    
                    selected = st.multiselect(
                        "Select questions or enter custom ones",
                        predefined,
                        default=predefined[:2]
                    )
                    
                    custom = st.text_input("Custom question:")
                    if custom:
                        selected = list(selected) + [custom]
                    
                    if st.button("🤖 Get Answers"):
                        with st.spinner("Thinking..."):
                            result_qa = process_image(temp_path, questions=selected)
                        
                        if result_qa["success"]:
                            for q, a in result_qa["answers"].items():
                                st.write(f"**Q:** {q}")
                                st.write(f"**A:** {a}")
                                st.divider()
            else:
                st.error(f"❌ Error: {result['error']}")

# =============================
# MODE 2: PRODUCT COMPARISON
# =============================
elif mode == "Product Comparison":
    st.header("⚖️ Product Comparison")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Product 1")
        uploaded1 = st.file_uploader(
            "Product 1 label",
            type=["jpg", "jpeg", "png"],
            key="prod1"
        )
        
        if uploaded1:
            st.image(Image.open(uploaded1), use_column_width=True)
            temp_path1 = f"/tmp/prod1_{uploaded1.name}"
            with open(temp_path1, "wb") as f:
                f.write(uploaded1.getbuffer())
            
            result1 = process_image(temp_path1)
    
    with col2:
        st.subheader("Product 2")
        uploaded2 = st.file_uploader(
            "Product 2 label",
            type=["jpg", "jpeg", "png"],
            key="prod2"
        )
        
        if uploaded2:
            st.image(Image.open(uploaded2), use_column_width=True)
            temp_path2 = f"/tmp/prod2_{uploaded2.name}"
            with open(temp_path2, "wb") as f:
                f.write(uploaded2.getbuffer())
            
            result2 = process_image(temp_path2)
    
    if uploaded1 and uploaded2:
        if result1["success"] and result2["success"]:
            st.subheader("📊 Comparison Results")
            
            comparison = compare_products(result1["data"], result2["data"])
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.write(f"### Winner: {comparison['winner']}")
            with col2:
                st.write(f"### Score Difference: {comparison['health_score_diff']}")
            with col3:
                st.write("### Details:")
            
            st.write(comparison["protein_comparison"])
            st.write(comparison["carbs_comparison"])
            st.write(comparison["calories_comparison"])

# =============================
# MODE 3: BATCH ANALYSIS
# =============================
elif mode == "Batch Analysis":
    st.header("📦 Batch Analysis")
    
    st.info("Upload multiple product images for analysis (coming soon)")
    
    uploaded_files = st.file_uploader(
        "Choose multiple images",
        type=["jpg", "jpeg", "png"],
        accept_multiple_files=True
    )
    
    if uploaded_files and st.button("🔄 Analyze All"):
        results = []
        progress_bar = st.progress(0)
        
        for idx, file in enumerate(uploaded_files):
            temp_path = f"/tmp/batch_{idx}_{file.name}"
            with open(temp_path, "wb") as f:
                f.write(file.getbuffer())
            
            result = process_image(temp_path)
            if result["success"]:
                results.append({
                    "file": file.name,
                    **result
                })
            
            progress_bar.progress((idx + 1) / len(uploaded_files))
        
        st.subheader("Batch Results")
        for res in results:
            with st.expander(f"📄 {res['file']}"):
                st.json({
                    "data": res["data"],
                    "health_score": res["health_analysis"]["score"],
                    "confidence": res["confidence"]
                })

# =============================
# FOOTER
# =============================
st.divider()
st.markdown("""
---
**Nutrition OCR Pro v2.0** | Production-Ready
- ✅ Enhanced regex patterns
- ✅ Confidence scoring  
- ✅ Health analysis (1-10)
- ✅ Diet suitability checker
- ✅ Qwen LLM integration
- ✅ Product comparison
- ✅ Optimized performance

Built with Streamlit + Qwen2.5 + PaddleOCR
""")
