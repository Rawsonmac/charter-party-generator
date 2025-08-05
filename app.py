import streamlit as st
from templates import load_template, get_template_names, suggest_templates_by_route
from document_generator import generate_document
import base64

# Streamlit app
st.title("Oil Brokerage Charter Party Generator")

# Route input for template suggestion
st.subheader("Route Information")
route = st.text_input("Enter Route (e.g., Houston to Rotterdam)", placeholder="Enter route for template suggestions")
suggested_templates = suggest_templates_by_route(route) if route else []

if suggested_templates:
    st.write("Suggested Templates for Route:")
    st.write(suggested_templates)

# Template selection
template_names = get_template_names()
template_name = st.selectbox("Select Charter Template", template_names)

# Load template
template = load_template(template_name)

# Input fields for custom terms
st.subheader("Customize Terms")
custom_terms = {}
for key, default_value in template.items():
    if key not in ["Standard Clauses", "Modern Clauses"]:
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
