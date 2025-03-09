import streamlit as st
import re
import random
import string
import pyperclip
from zxcvbn import zxcvbn

# Configure Page
st.set_page_config(page_title="🔒 Password Strength Meter", page_icon="🔑", layout="centered")

# Custom Styles
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .stTextInput > div > div > input { font-size: 18px; }
    .stButton>button { background-color: #007bff; color: white; font-size: 16px; padding: 10px; }
    .stButton>button:hover { background-color: #0056b3; }
    .stProgress > div > div { background-color: #28a745; }
    </style>
""", unsafe_allow_html=True)

# Generate Secure Password
def generate_password(length=12):
    characters = string.ascii_letters + string.digits + "!@#$%^&*()"
    return "".join(random.choice(characters) for _ in range(length))

# Check Password Strength
def check_password_strength(password):
    analysis = zxcvbn(password)
    score = analysis["score"]  # Score: 0 (Weak) to 4 (Strong)
    feedback = analysis["feedback"]["suggestions"]
    return score, feedback

# UI Layout
st.title("🔒 Password Strength Checker")
st.write("Check your password strength and get suggestions to improve security.")

# Password Input & Visibility Toggle
password = st.text_input("Enter your password", type="password", key="password_input")

# Show/Hide Password Toggle
show_password = st.checkbox("Show password")
if show_password:
    st.text("🔑 " + password)

# Password Strength Meter
if password:
    strength, feedback = check_password_strength(password)
    strength_levels = {0: "Very Weak", 1: "Weak", 2: "Moderate", 3: "Strong", 4: "Very Strong"}
    
    # Display Strength Level
    st.subheader(f"🔹 Strength: **{strength_levels[strength]}**")
    
    # Progress Bar Based on Strength
    st.progress((strength + 1) / 5)

    # Feedback for Improvement
    if feedback:
        st.warning("🔹 **Suggestions to Improve:**")
        for tip in feedback:
            st.write(f"✔ {tip}")
    else:
        st.success("✅ Your password is strong!")

# Password Generator Section
st.subheader("🔑 Generate a Strong Password")
length = st.slider("Select password length", min_value=8, max_value=32, value=12)
if st.button("Generate Password"):
    new_password = generate_password(length)
    st.text_input("Generated Password", value=new_password, key="generated_password", disabled=True)

    # Copy to Clipboard Button
    if st.button("📋 Copy to Clipboard"):
        pyperclip.copy(new_password)
        st.success("✅ Password copied to clipboard!")

# Download Report Feature
if password:
    report = f"""
    Password Strength Report
    =========================
    Password: {password}
    Strength Level: {strength_levels[strength]}
    
    Suggestions:
    {', '.join(feedback) if feedback else 'None'}
    """
    
    st.download_button("📥 Download Report", report, file_name="password_report.txt")

# Footer
st.markdown("---")
st.markdown("🔐 **Stay Secure. Use Strong Passwords.** © 2025")