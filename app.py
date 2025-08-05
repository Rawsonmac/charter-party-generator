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

# Custom CSS for improved oil/gas-themed UI
st.markdown("""
    <style>
        body {
            background-image: linear-gradient(to bottom, #1e3a8a, #111827);
            background-size: cover;
            background-attachment: fixed;
        }
        .stApp {
            background-color: rgba(255, 255, 255, 0.97);
            border-radius: 0.75rem;
            padding: 2rem;
            max-width: 800px;
            margin: 0 auto;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
            animation: fadeIn 0.8s ease-in;
        }
        .dark-theme .stApp {
            background-color: rgba(17, 24, 39, 0.97);
            color: #e5e7eb;
        }
        .dark-theme .stTextInput > div > input, .dark-theme .stTextArea > div > textarea, .dark-theme .stSelectbox > div > select {
            background-color: #1f2937;
            color: #e5e7eb;
            border: 1px solid #374151;
            border-radius: 0.25rem;
        }
        .stExpander {
            background-color: rgba(255, 255, 255, 0.1);
            border-radius: 0.5rem;
            margin-bottom: 1rem;
        }
        .dark-theme .stExpander {
            background-color: rgba(31, 41, 55, 0.3);
        }
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(-10px); }
            to { opacity: 1; transform: translateY(0); }
        }
        .header-logo {
            display: flex;
            align-items: center;
            gap: 0.75rem;
            margin-bottom: 1rem;
        }
        .header-logo img {
            width: 2.5rem;
            height: 2.5rem;
        }
        .header-title {
            color: #1e3a8a;
            font-size: 2rem;
            font-weight: 600;
            margin: 0;
        }
        .dark-theme .header-title {
            color: #60a5fa;
        }
        .subheader {
            color: #4b5563;
            font-size: 1.1rem;
            margin-bottom: 1.5rem;
            text-align: center;
        }
        .dark-theme .subheader {
            color: #9ca3af;
        }
        .tooltip {
            position: relative;
            cursor: help;
            color: #2563eb;
            text-decoration: underline dotted;
        }
        .dark-theme .tooltip {
            color: #93c5fd;
        }
        .tooltip:hover::after {
            content: attr(data-tooltip);
            position: absolute;
            bottom: 100%;
            left: 50%;
            transform: translateX(-50%);
            background-color: #1f2937;
            color: white;
            padding: 0.5rem 0.75rem;
            border-radius: 0.25rem;
            font-size: 0.875rem;
            white-space: normal;
            width: 200px;
            z-index: 10;
        }
        .error {
            color: #dc2626;
            font-size: 0.9rem;
            margin-top: 0.25rem;
            font-weight: 500;
        }
        .section-title {
            color: #1e40af;
            font-size: 1.25rem;
            font-weight: 600;
            margin-bottom: 0.5rem;
        }
        .dark-theme .section-title {
            color: #93c5fd;
        }
        .stButton > button {
            background-color: #1e40af;
            color: white;
            border-radius: 0.25rem;
            padding: 0.5rem 1rem;
            font-weight: 500;
        }
        .stButton > button:hover {
            background-color: #2563eb;
        }
        .dark-theme .stButton > button {
            background-color: #2563eb;
        }
        .dark-theme .stButton > button:hover {
            background-color: #3b82f6;
        }
    </style>
""", unsafe_allow_html=True)

# Streamlit app
st.markdown("""
    <div class="header-logo">
        <img src="https://img.icons8.com/ios-filled/50/000000/oil-tanker.png" alt="Tanker Icon">
        <h1 class="header-title">Oil Brokerage Charter Party Generator</h1>
    </div>
    <p class="subheader">Create a customized TANKERVOY 87 charter party with clear, user-friendly inputs.</p>
""", unsafe_allow_html=True)

# Theme toggle
theme = st.session_state.get('theme', 'light')
if st.button("Switch to Dark/Light Theme"):
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

# Clause library with descriptions
clauses = [
    {
        "id": "demurrage",
        "title": "Demurrage",
        "content": "Demurrage shall be payable at the rate of USD [amount] per day or pro-rata for any part of a day.",
        "description": "Covers compensation for delays beyond agreed laytime at port."
    },
    {
        "id": "forceMajeure",
        "title": "Force Majeure",
        "content": "Neither party shall be liable for delays due to events beyond their reasonable control, including acts of God, war, or strikes.",
        "description": "Protects against liability for unavoidable delays (e.g., natural disasters, strikes)."
    },
    {
        "id": "cargoInspection",
        "title": "Cargo Inspection",
        "content": "Charterers shall have the right to appoint an independent inspector to verify cargo quantity and quality at loading and discharging ports.",
        "description": "Allows charterers to ensure cargo meets specifications via third-party inspection."
    }
]

# Route selection
with st.expander("Route Information", expanded=True):
    st.markdown('<p class="section-title">Select Route</p>', unsafe_allow_html=True)
    route = st.text_input(
        "Enter Route",
        placeholder="e.g., Houston to Rotterdam",
        help="Enter a route to get template suggestions tailored to common oil trade paths.",
        key="route"
    )
    if route:
        suggested_templates = suggest_templates_by_route(route)
        st.markdown("**Suggested Templates:**")
        st.write(", ".join(suggested_templates) or "None")

# Vessel and template selection
with st.expander("Vessel and Template", expanded=True):
    st.markdown('<p class="section-title">Vessel Details</p>', unsafe_allow_html=True)
    vessel_class = st.selectbox(
        "Vessel Class",
        ["Panamax", "Aframax", "Suezmax", "VLCC", "ULCC"],
        help="Select the vessel class to adjust cargo capacity and rates (e.g., Panamax for 60,000 tons).",
        key="vessel_class"
    )
    template_names = get_template_names()
    template_name = st.selectbox(
        "Charter Template",
        template_names,
        help="Choose a template (e.g., TANKERVOY 87 for voyage charters, Shell Time 4 for time charters).",
        key="template_name"
    )
    template = load_template(template_name)
    template = adjust_terms_by_vessel_class(template, vessel_class)

# Custom terms
with st.expander("Charter Terms", expanded=True):
    st.markdown('<p class="section-title">Customize Charter Terms</p>', unsafe_allow_html=True)
    custom_terms = {}
    errors = {}
    for key, default_value in template.items():
        if key not in ["Standard Clauses", "Modern Clauses", "Additional Clauses"]:
            label = f'<span class="tooltip" data-tooltip="{key.replace("_", " ").title()} for the charter agreement">{key.replace("_", " ").title()}</span>'
            custom_terms[key] = st.text_input(
                label,
                value=default_value,
                key=f"term_{key}",
                help=f"Enter the {key.lower()} (e.g., company name for Owners, cargo type for Cargo)."
            )
            if not custom_terms[key] and key in ["Owners", "Charterers", "Vessel Name"]:
                errors[key] = f"{key.replace('_', ' ')} is required"
        else:
            label = f'<span class="tooltip" data-tooltip="{key} for the charter">{key}</span>'
            custom_terms[key] = st.text_area(
                label,
                value=default_value,
                key=f"term_{key}",
                help=f"Edit {key.lower()} or leave as default. These are pre-filled from the template."
            )

# Additional fields
with st.expander("Ports and Dates", expanded=True):
    st.markdown('<p class="section-title">Specify Ports and Dates</p>', unsafe_allow_html=True)
    custom_terms["Loading Port"] = st.selectbox(
        '<span class="tooltip" data-tooltip="Port(s) where cargo is loaded">Loading Port</span>',
        ["Select a port"] + ports,
        help="Choose the port where cargo will be loaded (e.g., Houston for oil exports).",
        key="loading_port"
    )
    custom_terms["Discharging Port"] = st.selectbox(
        '<span class="tooltip" data-tooltip="Port(s) where cargo is unloaded">Discharging Port</span>',
        ["Select a port"] + ports,
        help="Choose the port where cargo will be discharged (e.g., Rotterdam for imports).",
        key="discharging_port"
    )
    custom_terms["Laydays"] = st.date_input(
        '<span class="tooltip" data-tooltip="Start date for cargo operations">Laydays Commencement</span>',
        help="Select the date when cargo operations can begin.",
        key="laydays"
    )
    custom_terms["Cancelling"] = st.date_input(
        '<span class="tooltip" data-tooltip="Date after which charter can be cancelled">Cancelling Date</span>',
        help="Select the date after which the charter can be cancelled if not started.",
        key="cancelling"
    )
    custom_terms["Freight Rate"] = st.text_input(
        '<span class="tooltip" data-tooltip="Rate per ton or Worldscale points">Freight Rate</span>',
        placeholder="e.g., WS100 or 50.00",
        help="Enter the freight rate (Worldscale points or USD per ton).",
        key="freight_rate"
    )
    custom_terms["Use Worldscale"] = st.checkbox(
        '<span class="tooltip" data-tooltip="Apply Worldscale rates for freight">Use Worldscale Terms</span>',
        value=True,
        help="Check to apply Worldscale freight rates; uncheck for custom rates.",
        key="use_worldscale"
    )

    # Validation
    if custom_terms["Loading Port"] == "Select a port":
        errors["Loading Port"] = "Please select a loading port"
    if custom_terms["Discharging Port"] == "Select a port":
        errors["Discharging Port"] = "Please select a discharging port"
    if custom_terms["Laydays"] and custom_terms["Cancelling"] and custom_terms["Laydays"] >= custom_terms["Cancelling"]:
        errors["Cancelling"] = "Cancelling date must be after laydays"
    if custom_terms["Freight Rate"] and not custom_terms["Freight Rate"].replace('.', '', 1).isdigit():
        errors["Freight Rate"] = "Freight rate must be a number"

    # Display errors next to fields
    for field, error in errors.items():
        st.markdown(f'<p class="error">{error}</p>', unsafe_allow_html=True)

# Clause selection
with st.expander("Additional Clauses", expanded=True):
    st.markdown('<p class="section-title">Add Optional Clauses</p>', unsafe_allow_html=True)
    selected_clauses = st.multiselect(
        "Select Clauses",
        [clause["title"] for clause in clauses],
        help="Choose additional clauses to include in the charter.",
        key="clauses"
    )
    for clause in clauses:
        if clause["title"] in selected_clauses:
            st.markdown(f"**{clause['title']}**: {clause['description']}")
            st.text_area(
                f"{clause['title']} Content",
                value=clause["content"],
                disabled=True,
                key=f"clause_{clause['id']}",
                help="This clause is included in the document."
            )
    selected_clause_content = "\n\n".join(
        clause["content"] for clause in clauses if clause["title"] in selected_clauses
    )
    if selected_clause_content:
        custom_terms["Additional Clauses"] = selected_clause_content

    additional_clauses = st.text_area(
        '<span class="tooltip" data-tooltip="Custom clauses for specific needs">Custom Clauses</span>',
        placeholder="Enter any custom clauses here...",
        help="Add custom clauses specific to your charter agreement.",
        key="additional_clauses"
    )
    if additional_clauses:
        custom_terms["Additional Clauses"] = (
            custom_terms.get("Additional Clauses", "") + "\n\n" + additional_clauses
        ).strip()

# Worldscale calculator
with st.expander("Worldscale Calculator", expanded=False):
    st.markdown('<p class="section-title">Estimate Freight Rate</p>', unsafe_allow_html=True)
    if st.button("Calculate Worldscale Rate"):
        distance = st.number_input(
            "Distance (nautical miles)",
            min_value=0.0,
            value=1000.0,
            help="Enter the voyage distance in nautical miles.",
            key="distance"
        )
        vessel_size = st.number_input(
            "Vessel Size (DWT)",
            min_value=0.0,
            value=50000.0,
            help="Enter the vessel's deadweight tonnage (DWT).",
            key="vessel_size"
        )
        rate = distance * vessel_size * 0.0001  # Mock calculation
        st.markdown(f"**Estimated Worldscale Rate**: USD {rate:.2f}")

# Save and generate
with st.expander("Generate and Save", expanded=True):
    st.markdown('<p class="section-title">Generate Charter</p>', unsafe_allow_html=True)
    save_charter = st.checkbox(
        "Save Charter for Future Reference",
        help="Check to save this charter to review later.",
        key="save_charter"
    )
    if st.button("Generate Charter Document"):
        if errors:
            st.error("Please correct the following errors:")
            for field, error in errors.items():
                st.markdown(f"- {error}", unsafe_allow_html=True)
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
                    "terms": {k: str(v) for k, v in custom_terms.items()}
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

# Saved charters
with st.expander("Saved Charters", expanded=False):
    st.markdown('<p class="section-title">View Saved Charters</p>', unsafe_allow_html=True)
    if os.path.exists(CHARTERS_FILE):
        with open(CHARTERS_FILE, "r") as f:
            saved_charters = json.load(f)
        if saved_charters:
            for i, charter in enumerate(saved_charters):
                st.markdown(f"**Charter {i+1}**: {charter['template']} - {charter['vessel_class']} - {charter['terms'].get('Vessel Name', 'Unnamed')}")
        else:
            st.write("No saved charters yet.")
    else:
        st.write("No saved charters yet.")
