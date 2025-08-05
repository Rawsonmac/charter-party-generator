import streamlit as st
from templates import load_template
from document_generator import generate_document
import base64

# Streamlit app
st.title("Oil Brokerage Charter Party Generator")

# Template selection
template_options = ["Shell Time 4", "Asbatankvoy 2025", "Shellvoy 6", "BPVOY4", "ExxonMobil Voy2000"]
template_name = st.selectbox("Select Charter Template", template_options)

# Load template
template = load_template(template_name)

# Input fields for custom terms
st.subheader("Customize Terms")
custom_terms = {}
for key, default_value in template.items():
    if key != "Standard Clauses":
        custom_terms[key] = st.text_input(key, value=default_value)
    else:
        custom_terms[key] = st.text_area(key, value=default_value)

# Additional custom clauses
additional_clauses = st.text_area("Additional Custom Clauses", placeholder="Enter any additional clauses here...")

# Generate document
if st.button("Generate Charter Document"):
    if additional_clauses:
        custom_terms["Additional Clauses"] = additional_clauses
    
    # Generate document
    doc_buffer = generate_document(template_name, custom_terms)
    
    # Provide download link
    b64 = base64.b64encode(doc_buffer.getvalue()).decode()
    href = f'<a href="data:application/vnd.openxmlformats-officedocument.wordprocessingml.document;base64,{b64}" download="{template_name}_Charter.docx">Download Charter Document</a>'
    st.markdown(href, unsafe_allow_html=True)
    st.success("Document generated successfully!")
