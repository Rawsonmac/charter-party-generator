import streamlit as st
from templates import load_template, get_template_names, suggest_templates_by_route, adjust_terms_by_vessel_class
from document_generator import generate_document
import base64
import json
import os
from docx import Document
from io import BytesIO

# Ensure absolute path for charters.json on Streamlit Cloud
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CHARTERS_FILE = os.path.join(BASE_DIR, "charters.json")

# Custom CSS for oil/gas theme
st.markdown("""
    <style>
        body {
            background-image: linear-gradient(to bottom, #1e3a8a, #111827);
            background-size: cover;
            background-attachment: fixed;
        }
        .stApp {
            background-color: rgba(255, 255, 255, 0.95);
            border-radius: 0.5rem;
            padding: 2rem;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            animation: fadeIn 1s ease-in;
        }
        .dark-theme .stApp {
            background-color: rgba(17, 24, 39, 0.95);
            color: #e5e7eb;
        }
        .dark-theme .stTextInput > div > input, .dark-theme .stTextArea > div > textarea, .dark-theme .stSelectbox > div > select {
            background-color: #1f2937;
            color: #e5e7eb;
            border-color: #374151;
        }
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(-10px); }
            to { opacity: 1; transform: translateY(0); }
        }
        .header-logo {
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }
        .header-logo img {
            width: 2rem;
            height: 2rem;
        }
        .tooltip {
            position: relative;
        }
        .tooltip:hover::after {
            content: attr(data-tooltip);
            position: absolute;
            bottom: 100%;
            left: 50%;
            transform: translateX(-50%);
            background-color: #1f2937;
            color: white;
            padding: 0.5rem;
            border-radius: 0.25rem;
            white-space: nowrap;
            z-index: 10;
        }
        .error {
            color: #dc2626;
            font-size: 0.875rem;
        }
    </style>
""", unsafe_allow_html=True)

# Streamlit app
st.markdown("""
    <div class="header-logo">
        <img src="https://img.icons8.com/ios-filled/50/000000/oil-tanker.png" alt="Tanker Icon">
        <h1 style="color: #1e3a8a;">Oil Brokerage Charter Party Generator</h1>
    </div>
    <p style="text-align: center; color: #4b5563;">Generate a customized TANKERVOY 87 charter party with an oil and gas theme.</p>
""", unsafe_allow_html=True)

# Theme toggle
theme = st.session_state.get('theme', 'light')
if st.button("Toggle Dark/Light Theme"):
    theme = 'dark' if theme == 'light' else 'light'
    st.session_state.theme = theme
st.markdown(f'<div class="{theme}-theme">', unsafe_allow_html=True)

# Mock port data
ports = [
    "Rotterdam, Netherlands (Major crude oil hub)",
    "Houston, USA (Key US oil export port)",
    "Singapore, Singapore (Asian bunkering hub)",
    "Fujairah, UAE (Middle East bunkering)",
    "Shanghai, China (Major import port)",
    "Ras Tanura, Saudi Arabia (Crude export)",
    "Antwerp, Belgium (European refining)",
    "Port Said, Egypt (Suez Canal access)"
]

# Clause library
clauses = [
    {"id": "demurrage", "title": "Demurrage", "content": "Demurrage shall be payable at the rate of USD [amount] per day or pro-rata for any part of a day."},
    {"id": "forceMajeure", "title": "Force Majeure", "content": "Neither party shall be liable for delays due to events beyond their reasonable control, including acts of God, war, or strikes."},
    {"id": "cargoInspection", "title": "Cargo Inspection", "content": "Charterers shall have the right to appoint an independent inspector to verify cargo quantity and quality at loading and discharging ports."}
]

# Route input for template suggestion
st.subheader("Route Information")
route = st.text_input("Enter Route (e.g., Houston to Rotterdam)", placeholder="Enter route for template suggestions", key="route")
suggested_templates = suggest_templates_by_route(route) if route else []
if suggested_templates:
    st.write("Suggested Templates for Route:")
    st.write(suggested_templates)

# Vessel class selection
st.subheader("Vessel Class")
vessel_class = st.selectbox("Select Vessel Class", ["Panamax", "Aframax", "Suezmax", "VLCC", "ULCC"], key="vessel_class")

# Template selection
template_names = get_template_names()
template_name = st.selectbox("Select Charter Template", template_names, key="template_name")
template = load_template(template_name)
template = adjust_terms_by_vessel_class(template, vessel_class)

# Input fields for custom terms
st.subheader("Customize Terms")
custom_terms = {}
errors = {}
for key, default_value in template.items():
    if key not in ["Standard Clauses", "Modern Clauses", "Additional Clauses"]:
        label = f'<span class="tooltip" data-tooltip="{key} details">{key}</span>'
        custom_terms[key] = st.text_input(label, value=default_value, key=f"term_{key}", help=f"Enter {key.lower()} details")
        if not custom_terms[key] and key in ["Owners", "Charterers", "Vessel Name"]:
            errors[key] = f"{key} is required"
    else:
        custom_terms[key] = st.text_area(key, value=default_value, key=f"term_{key}", help=f"Enter {key.lower()} details")

# Additional fields for ports and dates
custom_terms["Loading Port"] = st.selectbox(
    '<span class="tooltip" data-tooltip="Port(s) for loading cargo">Loading Port(s)</span>',
    [""] + ports, key="loading_port", help="Select or type a loading port"
)
custom_terms["Discharging Port"] = st.selectbox(
    '<span class="tooltip" data-tooltip="Port(s) for discharging cargo">Discharging Port(s)</span>',
    [""] + ports, key="discharging_port", help="Select or type a discharging port"
)
custom_terms["Laydays"] = st.date_input(
    '<span class="tooltip" data-tooltip="Date when laydays commence">Laydays Commencement</span>',
    key="laydays", help="Select laydays commencement date"
)
custom_terms["Cancelling"] = st.date_input(
    '<span class="tooltip" data-tooltip="Date after which charter can be cancelled">Cancelling Date</span>',
    key="cancelling", help="Select cancelling date"
)
custom_terms["Freight Rate"] = st.text_input(
    '<span class="tooltip" data-tooltip="Freight rate per ton">Freight Rate (per ton)</span>',
    key="freight_rate", help="Enter freight rate per ton"
)
custom_terms["Use Worldscale"] = st.checkbox(
    '<span class="tooltip" data-tooltip="Use Worldscale rates or custom terms">Use Worldscale Terms</span>',
    value=True, key="use_worldscale", help="Check to use Worldscale terms"
)

# Validation for additional fields
if not custom_terms["Loading Port"]:
    errors["Loading Port"] = "Loading port is required"
if not custom_terms["Discharging Port"]:
    errors["Discharging Port"] = "Discharging port is required"
if custom_terms["Laydays"] and custom_terms["Cancelling"] and custom_terms["Laydays"] >= custom_terms["Cancelling"]:
    errors["Cancelling"] = "Cancelling date must be after laydays"
if custom_terms["Freight Rate"] and not custom_terms["Freight Rate"].replace('.', '', 1).isdigit():
    errors["Freight Rate"] = "Freight rate must be a number"

# Display errors
for field, error in errors.items():
    st.markdown(f'<p class="error">{error}</p>', unsafe_allow_html=True)

# Clause selection
st.subheader("Additional Clauses")
selected_clauses = st.multiselect(
    "Select Additional Clauses",
    [clause["title"] for clause in clauses],
    help="Select optional clauses to include",
    key="clauses"
)
selected_clause_content = "\n\n".join(
    clause["content"] for clause in clauses if clause["title"] in selected_clauses
)
if selected_clause_content:
    custom_terms["Additional Clauses"] = selected_clause_content

# Additional custom clauses
additional_clauses = st.text_area(
    '<span class="tooltip" data-tooltip="Add custom clauses here">Additional Custom Clauses</span>',
    placeholder="Enter any additional clauses here...", key="additional_clauses", help="Add custom clauses"
)
if additional_clauses:
    custom_terms["Additional Clauses"] = (
        custom_terms.get("Additional Clauses", "") + "\n\n" + additional_clauses
    ).strip()

# Save charter option
save_charter = st.checkbox("Save Charter for Future Use", key="save_charter")

# Worldscale calculator
if st.button("Worldscale Calculator"):
    distance = st.number_input("Enter Distance (nautical miles)", min_value=0.0, value=1000.0, key="distance")
    vessel_size = st.number_input("Enter Vessel Size (DWT)", min_value=0.0, value=50000.0, key="vessel_size")
    rate = distance * vessel_size * 0.0001  # Mock calculation
    st.write(f"Estimated Worldscale Rate: USD {rate:.2f}")

# Generate document
if st.button("Generate Charter Document"):
    if errors:
        st.error("Please fix the errors above before generating the document.")
    else:
        # Save charter
        if save_charter:
            saved_charters = []
            if os.path.exists(CHARTERS_FILE):
                with open(CHARTERS_FILE, "r") as f:
                    saved_charters = json.load(f)
            saved_charters.append({
                "template": template_name,
                "vessel_class": vessel_class,
                "terms": {k: str(v) for k, v in custom_terms.items()}  # Convert dates to strings
            })
            with open(CHARTERS_FILE, "w") as f:
                json.dump(saved_charters, f)

        # Generate document
        doc_text = generate_document(template_name, custom_terms)
        st.markdown("### Document Preview")
        st.markdown(doc_text, unsafe_allow_html=True)

        # Generate Word document
        doc = Document()
        for paragraph in doc_text.split('\n\n'):
            doc.add_paragraph(paragraph.replace('\n', ' '))
        
        # Save to BytesIO
        doc_buffer = BytesIO()
        doc.save(doc_buffer)
        doc_buffer.seek(0)
        
        # Provide download link
        b64 = base64.b64encode(doc_buffer.getvalue()).decode()
        href = f'<a href="data:application/vnd.openxmlformats-officedocument.wordprocessingml.document;base64,{b64}" download="{template_name}_Charter_{vessel_class}.docx">Download Charter Document (Word)</a>'
        st.markdown(href, unsafe_allow_html=True)
        st.success("Document generated successfully!")

# Display saved charters
if os.path.exists(CHARTERS_FILE):
    with open(CHARTERS_FILE, "r") as f:
        saved_charters = json.load(f)
    if saved_charters:
        st.subheader("Saved Charters")
        for i, charter in enumerate(saved_charters):
            st.write(f"Charter {i+1}: {charter['template']} - {charter['vessel_class']} - {charter['terms'].get('Vessel Name', 'Unnamed')}")
