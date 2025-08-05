def generate_document(template_name, custom_terms):
    # Extract custom terms with defaults
    owners = custom_terms.get('Owners', 'Owners')
    charterers = custom_terms.get('Charterers', 'Charterers')
    vessel_name = custom_terms.get('Vessel Name', 'Vessel Name')
    vessel_description = custom_terms.get('Vessel Description', 'Description of the vessel including class, tonnage, and specifications.')
    loading_port = custom_terms.get('Loading Port', 'In Charterers\' option.')
    discharging_port = custom_terms.get('Discharging Port', 'In Charterers\' option.')
    laydays = custom_terms.get('Laydays', 'Date').strftime('%Y-%m-%d') if hasattr(custom_terms.get('Laydays'), 'strftime') else custom_terms.get('Laydays', 'Date')
    cancelling = custom_terms.get('Cancelling', 'Date').strftime('%Y-%m-%d') if hasattr(custom_terms.get('Cancelling'), 'strftime') else custom_terms.get('Cancelling', 'Date')
    freight_rate = custom_terms.get('Freight Rate', 'Rate')
    use_worldscale = custom_terms.get('Use Worldscale', True)
    standard_clauses = custom_terms.get('Standard Clauses', '')
    modern_clauses = custom_terms.get('Modern Clauses', '')
    additional_clauses = custom_terms.get('Additional Clauses', '')

    # Compliance check for TOVALOP
    compliance_warnings = []
    if 'TOVALOP' not in (standard_clauses + modern_clauses + additional_clauses):
        compliance_warnings.append("Warning: TOVALOP clause recommended for pollution liability compliance.")

    # Generate document
    document = f"""
# TANKERVOY 87
## Tanker Voyage Charter Party

**IT IS THIS DAY AGREED** between {owners} (hereinafter referred to as "Owners") of the motor/tank vessel called {vessel_name} and {charterers} (hereinafter referred to as "Charterers") that the transportation herein provided for will be performed subject to the terms and conditions of this Charter, which includes Part I and Part II. If there is any conflict between the provisions of Part I and those of Part II, the provisions of Part I shall prevail.

---

### PART I

**(A) Vessel's Description**  
{vessel_description}

**(D) Loading Port(s) or Range(s)**  
{loading_port}

**(E) Discharging Port(s) or Range(s)**  
{discharging_port}

**(F) Laydays**  
Laydays shall not commence before noon (local time) on {laydays}, unless with Charterers' consent.

**(G) Cancelling**  
Noon (local time) on: {cancelling}.

**(H) Worldscale Terms**  
{'Except as otherwise stated or required by the context of this Charter, all terms and conditions of the current scale of nominal tanker freight rates published by the Worldscale Association (London) Ltd and the Worldscale Association (NYC) Inc. as in force on the date of commencement of loading ("Worldscale") shall apply.' if use_worldscale else 'Custom freight terms apply as specified.'}

**(J) Freight Rate**  
Freight shall be paid at the rate of {freight_rate} per ton on the intaken quantity of cargo.

**(Q) Standard Clauses**  
{standard_clauses or 'None.'}

**(R) Modern Clauses**  
{modern_clauses or 'None.'}

**(S) Additional Clauses**  
{additional_clauses or 'None.'}

**IN WITNESS WHEREOF** Owners and Charterers have caused this Charter consisting of a preamble and Parts I and II to be executed the day and year first above written.

For OWNERS: __________________________  
For CHARTERERS: ______________________

---

### PART II

**1. Condition of Vessel**  
The vessel's class as specified in Part I shall be maintained during the currency of this Charter. The Owners shall:  
(a) before and at the beginning of the loaded voyage exercise due diligence to make the vessel seaworthy and in every way fit for the voyage and for the carriage of the cargo.

**6. Cancellation by Charterer**  
If the vessel has not given a valid notice of readiness in accordance with Clause 8 before Cancelling specified in Part I (G), Charterers shall have the option of cancelling this Charter unless the vessel shall have been delayed due to Charterers' late nomination or revised orders.

**12. Freight Payment**  
(a) Subject to Clauses 4 and 35, freight shall be paid at the rate(s) specified in Part I (J), and calculated on the intaken quantity of cargo and on Collected Wastings. Payment of freight shall be made by Charterers in cash without deductions.

**20. ETA**  
(a) The master shall radio Charterers and agents at loading and discharging ports advising the vessel's ETA on sailing from the last port or when bound for such ports.

**28. New Jason Clause**  
General Average shall be payable according to the York/Antwerp Rules, 1974. If the adjustment is made in accordance with the law and practice of the United States of America, the following clause shall apply:  
"In the event of accident, danger, damage or disaster before or after the commencement of the voyage, resulting from any cause whatsoever, whether due to negligence or not..."

**31. Bills of Lading**  
Subject to all the relevant provisions of this Charter, bills of lading are to be signed as presented, but without prejudice to the Charter. Charterers hereby indemnify Owners against all liabilities and expenses (including legal costs) that may arise from the signing of bills of lading as presented.

**32. TOVALOP**  
Owners warrant that the vessel is a tanker owned by a Participating Owner in TOVALOP and will so remain during the currency of this Charter. When an escape or discharge of Oil occurs from the vessel and causes or threatens to cause Pollution Damage, Charterers may undertake measures to prevent or minimize such Pollution Damage.

---

**Compliance Warnings**  
{'; '.join(compliance_warnings) if compliance_warnings else 'None'}
"""
    return document
