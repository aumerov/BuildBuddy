import streamlit as st
import os
from dotenv import load_dotenv
from src.claude_client import ClaudeClient
from src.image_processor import ImageProcessor
from src.prompts import get_system_prompt


load_dotenv()


def initialize_session_state():
    if 'claude_client' not in st.session_state:
        try:
            st.session_state.claude_client = ClaudeClient()
        except ValueError as e:
            st.session_state.claude_client = None
            st.session_state.api_error = str(e)

# Error and directions to configure Claude API
def check_api_configuration():
    if st.session_state.claude_client is None:
        st.error("⚠️ Claude API not configured properly")
        st.error(st.session_state.get('api_error', 'Unknown error'))
        
        with st.expander("🔧 Setup Instructions"):
            st.markdown("""
            1. Copy `.env.example` to `.env`
            2. Add your Anthropic API key to the `.env` file:
               ```
               ANTHROPIC_API_KEY=your_actual_api_key_here
               ```
            3. Restart the application
            
            Get your API key from: https://console.anthropic.com/
            """)
        return False
    return True


def main():
    st.set_page_config(
        page_title="BuildBuddy - AI Hardware Assistant",
        page_icon="🔧",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    initialize_session_state()
    
    st.title("🔧 BuildBuddy")
    st.subheader("AI-Powered Hardware Repair & Design Assistant")
    
    if not check_api_configuration():
        return
    
    st.markdown("---")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.header("📷 Upload Hardware Image")
        uploaded_file = st.file_uploader(
            "Choose an image of your hardware",
            type=['jpg', 'jpeg', 'png', 'webp'],
            help="Upload a clear image of the hardware you need help with"
        )
        
        if uploaded_file:
            st.image(uploaded_file, caption="Uploaded Image", use_container_width=True)
            
            with st.expander("📊 Image Details"):
                img_info = ImageProcessor.get_image_info(uploaded_file)
                if 'error' not in img_info:
                    st.json(img_info)
                else:
                    st.error(img_info['error'])
    
    with col2:
        st.header("📝 Describe the Problem")
        problem_description = st.text_area(
            "What's wrong with your hardware?",
            placeholder="Describe the issue you're experiencing...\n\nFor example:\n- My PCB isn't working after assembly\n- Drone motor making strange noises\n- Circuit board has visible damage\n- Need help designing a new component",
            height=200
        )
        
        st.header("⚙️ Analysis Options")
        analysis_type = st.selectbox(
            "Type of analysis",
            ["General Repair", "Design Review", "Troubleshooting", "Component Analysis"],
            help="Select the type of assistance you need"
        )
    
    st.markdown("---")
    
    if st.button("🔍 Analyze Hardware", type="primary", use_container_width=True):
        if not uploaded_file and not problem_description.strip():
            st.warning("Please upload an image or describe your problem to get started.")
            return
        
        with st.spinner("🤖 Analyzing your hardware with Claude..."):
            image_data = None
            image_format = None
            
            if uploaded_file:
                processed_data, processed_format = ImageProcessor.process_image(uploaded_file)
                if processed_data:
                    image_data = processed_data
                    image_format = processed_format
                else:
                    st.error("Failed to process the uploaded image. Please try again.")
                    return
            
            system_prompt = get_system_prompt(has_image=uploaded_file is not None)
            
            full_description = problem_description
            if analysis_type != "General Repair":
                full_description = f"[{analysis_type}] {problem_description}"
            
            try:
                response = st.session_state.claude_client.analyze_hardware(
                    image_data=image_data,
                    image_format=image_format,
                    problem_description=full_description,
                    system_prompt=system_prompt
                )
                
                st.header("🎯 Analysis Results")
                st.markdown(response)
                
                with st.expander("💾 Save Analysis"):
                    st.download_button(
                        label="📄 Download as Text",
                        data=response,
                        file_name=f"buildbuddy_analysis_{analysis_type.lower().replace(' ', '_')}.txt",
                        mime="text/plain"
                    )
                
            except Exception as e:
                st.error(f"Error during analysis: {str(e)}")
    
    with st.sidebar:
        st.header("ℹ️ About BuildBuddy")
        st.markdown("""
        BuildBuddy is your AI-powered hardware assistant that helps with:
        
        - 🔧 **Hardware Repair**: Diagnose and fix broken devices
        - 🎨 **Design Review**: Get feedback on your PCB layouts
        - 🔍 **Troubleshooting**: Step-by-step problem solving
        - 🧩 **Component Analysis**: Understand your hardware better
        
        Simply upload an image and/or describe your problem to get started!
        """)
        
        st.header("💡 Tips for Best Results")
        st.markdown("""
        - Use clear, well-lit photos
        - Include multiple angles if helpful
        - Describe symptoms clearly
        - Mention what you've already tried
        - Specify your skill level
        """)
        
        st.header("⚠️ Safety First")
        st.warning("""
        Always follow safety guidelines when working with hardware:
        - Disconnect power before repairs
        - Use proper ESD protection
        - Wear safety equipment
        - When in doubt, consult a professional
        """)


if __name__ == "__main__":
    main()