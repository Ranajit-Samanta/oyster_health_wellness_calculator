import streamlit as st
import math
import os
import pandas as pd
import smtplib
from email.mime.text import MIMEText
import uuid
import base64
st.set_page_config(layout="wide")

# Apply Background Color
st.markdown(
    """
    <style>
    .stApp {
        background-color: lightblue;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# Initialize session state variables if not set
if "name" not in st.session_state:
    st.session_state.name = None
if "dry_tissue_weight" not in st.session_state:
    st.session_state.dry_tissue_weight = None
if "shell_cavity_volume" not in st.session_state:
    st.session_state.shell_cavity_volume = None
if "CI" not in st.session_state:
    st.session_state.CI = None
if "ci_results" not in st.session_state:
    st.session_state.ci_results = {}



# Define calculations
def calculate_ci(dry_tissue_weight,shell_cavity_volume):
    return (dry_tissue_weight/shell_cavity_volume)*100


def get_user_session_id():
    """Ensure the session ID persists across interactions."""
    if "session_id" not in st.session_state:
        st.session_state.session_id = str(uuid.uuid4())  # Create a new session ID for the user
    return st.session_state.session_id

#====== saving this values in excel ======#

def save_to_excel():
    # Define file path
    user_ip = get_user_session_id()
    excel_file = f"oyster_health_wellness_checker_{user_ip}.xlsx"

    # Ensure all necessary calculations have been performed
    if None in [st.session_state.get("CI")]:
        st.error("Please perform all calculations before saving to Excel.")
        return

    # Retrieve values from session state
    data = {
        "Name": [st.session_state.get("name", "N/A")],
        "Dry tissue weight (gm)": [st.session_state.get("dry_tissue_weight", "N/A")],
        "Shell cavity volume (ml)": [st.session_state.get("shell_cavity_volume", "N/A")],
        "CI": [st.session_state.get("CI", "N/A")],
               
    }

    # Convert to DataFrame
    new_data = pd.DataFrame(data)

    # Check if the file exists
    if os.path.exists(excel_file):
        # Load existing data
        existing_data = pd.read_excel(excel_file, engine="openpyxl")
        # Append new data
        updated_data = pd.concat([existing_data, new_data], ignore_index=True)
    else:
        # If file doesn't exist, create a new one
        updated_data = new_data

    # Save data to Excel
    updated_data.to_excel(excel_file, index=False, engine="openpyxl")

    st.success(f"Session data saved to {excel_file} successfully!")

def display():
    user_ip=get_user_session_id()
    excel_file=f"oyster_health_wellness_checker_{user_ip}.xlsx"
    #   Display existing data
    if os.path.exists(excel_file):
        st.subheader("Stored Data:")
        df = pd.read_excel(excel_file, engine="openpyxl")
        st.dataframe(df)
    
def delete_item_from_excel(delete_name):
    user_ip=get_user_session_id()
    excel_file=f"oyster_health_wellness_checker_{user_ip}.xlsx"
    
    if os.path.exists(excel_file):
        # Read the existing Excel file into a DataFrame
        data = pd.read_excel(excel_file, engine="openpyxl")

        # Check if the name exists in the data and delete that row
        data = data[data["Name"] != delete_name]

        # Save the updated DataFrame back to Excel
        data.to_excel(excel_file, index=False, engine="openpyxl")

        st.success(f"Item with the name '{delete_name}' has been deleted from the Excel file!")
    else:
        st.error("The Excel file does not exist.")

# Layout

# st.write("<h1 style='color:white; text-align:center; padding: 20px; background-color: black; font-family: Times New Roman, Times, serif; font-style: italic;'>🌳Unlocking the Tree Carbon Locker🌍</h1>", unsafe_allow_html=True)
def get_base64_image(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()

image_base64 = get_base64_image("WhatsApp Image 2025-03-23 at 11.27.56 PM.jpeg")

st.write(f"""
    <div class="unlocking_div" style='color: white; text-align:center; padding: 10px; background-color: #353839; 
    font-family: Times New Roman, Times, serif; font-style: italic; display: flex; 
    align-items: center; justify-content: center; gap: 18px;'>
        <img src="data:image/png;base64,{image_base64}" alt="Logo" 
        style="width:100px; height:auto;border-radius:50px">
        <h1 style='margin: 0; font-size: 38px;color: white;'>OYSTER HEATH & WELLNESS CALCULATOR</h1>
    </div>
""", unsafe_allow_html=True)




col1, col2 = st.columns([2, 1])

# ======= Oyster CONDITION CALCULATOR =======
with col1:
    st.write("<h1 style='color: purple;'>Oyster Condition Index Calculator</h1>", unsafe_allow_html=True)

    name = st.text_input("Name of the oyster species")
    dry_tissue_weight = st.number_input("Dry tissue weight (in gm)", value=None)
    shell_cavity_volume = st.number_input("Shell cavity volume (in ml)",value=None)
    

    if st.button("Calculate CI"):
        try:

            CI = calculate_ci(dry_tissue_weight,shell_cavity_volume)

          

            # Store results in session state
            st.session_state.name=name
            st.session_state.dry_tissue_weight = dry_tissue_weight
            st.session_state.shell_cavity_volume = shell_cavity_volume
            
            st.session_state.CI = CI
            st.session_state.ci_results = {
            "Total CI": CI
            }
        except:
            st.warning("Please enter proper values!!!")

    # Display Stem Biomass Results
    if st.session_state.ci_results:
        st.subheader("Calculated CI:")
        for key, value in st.session_state.ci_results.items():
            st.write(f"{key}: {value}")

    #if st.session_state.stem_results:
        


with col2:
    st.write("<h1 style='color: purple;'>Field Activities</h1>", unsafe_allow_html=True)
    st.write("<h3 style='color: black;'>Condition Index</h3>", unsafe_allow_html=True)
    st.write(
        "<h6 style='color: black;'>The condition index of an oyster is a measure of its physiological health and productivity. It is calculated using the formula: (Dry meat weight / Shell cavity volume) × 100. This method provides a more accurate reflection of tissue development relative to available space. A higher index suggests better environmental conditions and feeding efficiency. It is commonly used in ecological and aquaculture studies to monitor oyster well-being.</h6>",
        unsafe_allow_html=True,
    )
    st.image("WhatsApp Image 2025-03-24 at 12.22.09 AM.jpeg",width=300)
    st.write(
        "<h6 style='color: black;'>For more information click the below link:</h6>",
        
        unsafe_allow_html=True,
    )
    url = "https://www.researchgate.net/profile/Abhijit-Mitra-4;"
    st.write(" Profile Link: [Click Here](%s)" % url)
    
    urll = "https://www.linkedin.com/in/abhijit-mitra-20750056/"
    st.markdown("LinkedIn: [Click Here](%s)" % urll)


#========= Image ==========#

col1,col2,col3=st.columns([1,1,1])
with col1:
    st.image("WhatsApp Image 2025-03-22 at 2.27.17 PM.jpeg", width=350)
with col2:
    st.image("WhatsApp Image 2025-03-24 at 12.23.05 AM (1).jpeg",width=350)

with col3:
    st.image("WhatsApp Image 2025-03-24 at 12.18.34 AM.jpeg",width=225)


if st.button("Save Results to Excel"):
    save_to_excel()
    display()
    st.warning("Please download your Excel file before refresh the page!!!")

# Example usage: Delete a row with a specific name
delete_name = st.text_input("Enter the Name to delete:")
if st.button("Delete Item"):
    delete_item_from_excel(delete_name)






#===== end note  =========#
col1,col2=st.columns([2,1])
with col1:
    st.write(
        "<h2 style='color: purple;'>End Note</h2>",
        unsafe_allow_html=True,
    )
    st.write(
        "<h5 style='color: black;'>1. Water Filtration and Quality Improvement: </h5>",
        unsafe_allow_html=True,
    )
    st.write(
        "<h6 style='color: blue;'>Oysters are natural filter feeders, capable of filtering large volumes of water to remove plankton, nutrients, suspended sediments, and other pollutants. A single oyster can filter up to 50 liters of water per day, improving water clarity and quality, which benefits the overall health of coastal and estuarine ecosystems.</h6>",
        unsafe_allow_html=True,
    )
    st.write(
        "<h5 style='color: black;'>2. Habitat Formation and Biodiversity Support: </h5>",
        unsafe_allow_html=True,
    )
    st.write(
        "<h6 style='color: blue;'>Oyster reefs provide complex three-dimensional structures that serve as habitats for a wide range of marine organisms, including fish, crabs, worms, and other invertebrates. These reefs enhance local biodiversity, support nursery grounds for commercially important fish species, and contribute to the resilience of coastal ecosystems.</h6>",
        unsafe_allow_html=True,
    )
    st.write(
        "<h5 style='color: black;'>3. Coastal Protection and Shoreline Stabilization: </h5>",
        unsafe_allow_html=True,
    )
    st.write(
        "<h6 style='color: blue;'>Oyster reefs act as natural breakwaters, absorbing wave energy and reducing shoreline erosion. By stabilizing sediments and buffering storm surges, they play a critical role in protecting coastal areas from the impacts of climate change, such as rising sea levels and increased storm intensity.</h6>",
        unsafe_allow_html=True,
    )
    

with col2:
   st.write("<h3 style='color: black;'>Ecosystem Services of Oyster</h3>", unsafe_allow_html=True)
   st.video("SEA LEVEL RISE - A MAJOR THREAT IN THE PRESENT ERA BY DR. ABHIJIT MITRA.mp4") 



#========== email configuration=========#



col1,col2=st.columns([2,1])

with col1:
   

# Email Configuration

# Load email credentials from Streamlit Secrets
    EMAIL_ADDRESS = st.secrets["email"]["EMAIL_ADDRESS"]
    EMAIL_PASSWORD = st.secrets["email"]["EMAIL_PASSWORD"]

    SMTP_SERVER = "smtp.gmail.com"
    SMTP_PORT = 587

    def send_email(name, user_email, message):
        subject = f"New Contact Form Submission from {name}"
        body = f"Name: {name}\nEmail: {user_email}\n\nMessage:\n{message}"

        msg = MIMEText(body)
        msg["Subject"] = subject
        msg["From"] = EMAIL_ADDRESS  # Use your email as sender
        msg["To"] = EMAIL_ADDRESS  # Send to yourself

        try:
            server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
            server.starttls()  # Secure the connection
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            server.sendmail(EMAIL_ADDRESS, EMAIL_ADDRESS, msg.as_string())
            server.quit()
            return "✅ Your message has been sent successfully!"
        except Exception as e:
            return f"❌ Error: {str(e)}"

# Streamlit UI
    st.title("📩 Contact Us")

    name = st.text_input("Your Name")
    email = st.text_input("Your Email")
    message = st.text_area("Your Message")

    if st.button("Send Email"):
        if name and email and message:
            response = send_email(name, email, message)
            st.success(response)
        else:
            st.error("⚠️ Please fill in all fields.")




with col2:
    st.write("<h1 style='color: black;'>Knowledge Hunter</h1>", unsafe_allow_html=True)
    st.image("WhatsApp Image 2025-02-27 at 11.03.36 PM.jpeg",width=180)
    st.write("<h3 style='color: black;'>Dr. Abhijit Mitra</h3>", unsafe_allow_html=True)
    st.write("<h5 style='color: blue;'>Email: abhijitresearchmitra@gmail.com</h5>", unsafe_allow_html=True)
    st.write('<h5 style="color: black;">"Dive deep into the sea of knowledge to get pearl of peace."</h5>', unsafe_allow_html=True)



st.markdown(
    """
    <style>
        .footer {
            
            bottom: 0;
            width: 100%;
            text-align: center;
            font-size: 14px;
            color: gray;
            padding: 10px;
            background-color: #f8f9fa;
        }
    </style>
    <div class="footer">
        © 2025 Oyster Health & Wellness Checker. All rights reserved.
    </div>
    """,
    unsafe_allow_html=True
)






