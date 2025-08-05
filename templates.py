def load_template(template_name):
    templates = {
        "Shell Time 4": {
            "Vessel Name": "TBN",
            "Charterer": "[Charterer Name]",
            "Period": "12 months +/- 1 month",
            "Hire Rate": "[To be specified] USD/day",
            "Delivery Port": "[To be specified]",
            "Redelivery Port": "[To be specified]",
            "Standard Clauses": """
                1. Vessel to comply with ISM and ISPS codes.
                2. Charterer to pay port costs and bunkers.
                3. Owners to maintain vessel insurance and class certification.
                4. Hire payment due monthly in advance.
            """
        },
        "Asbatankvoy 2025": {
            "Vessel Name": "TBN",
            "Charterer": "[Charterer Name]",
            "Cargo": "Crude Oil",
            "Load Port": "[To be specified]",
            "Discharge Port": "[To be specified]",
            "Laytime": "72 hours",
            "Demurrage": "[To be specified] USD/day",
            "Standard Clauses": """
                1. Freight payable upon completion of discharge.
                2. Laytime not to commence before 0600 on ETA unless agreed.
                3. Owners to provide safe berth.
                4. Compliance with ESG and digital reporting requirements.
                5. Arbitration in New York, London, Singapore, or Hong Kong (New York default).
            """
        },
        "Shellvoy 6": {
            "Vessel Name": "TBN",
            "Charterer": "[Charterer Name]",
            "Cargo": "Crude Oil or Products",
            "Load Port": "[To be specified]",
            "Discharge Port": "[To be specified]",
            "Laytime": "72 hours",
            "Demurrage": "[To be specified] USD/day",
            "Standard Clauses": """
                1. NOR invalid if free pratique not granted within 6 hours of tendering.
                2. Charterer responsible for port costs.
                3. Vessel to comply with ship-to-ship transfer protocols.
                4. Time lost due to vessel condition not to count as laytime.
            """
        },
        "BPVOY4": {
            "Vessel Name": "TBN",
            "Charterer": "[Charterer Name]",
            "Cargo": "Crude Oil or Products",
            "Load Port": "[To be specified]",
            "Discharge Port": "[To be specified]",
            "Laytime": "72 hours",
            "Demurrage": "[To be specified] USD/day",
            "Standard Clauses": """
                1. Balanced terms for owners and charterers.
                2. Freight payable upon completion of discharge.
                3. Vessel to comply with modern safety and environmental regulations.
                4. Reduced need for rider clauses due to comprehensive terms.
            """
        },
        "ExxonMobil Voy2000": {
            "Vessel Name": "TBN",
            "Charterer": "[Charterer Name]",
            "Cargo": "Crude Oil or Products",
            "Load Port": "[To be specified]",
            "Discharge Port": "[To be specified]",
            "Laytime": "72 hours",
            "Demurrage": "[To be specified] USD/day",
            "Standard Clauses": """
                1. Clear and concise terms for loading and discharge.
                2. Charterer to provide safe port/berth.
                3. Freight payable upon completion of discharge.
                4. Vessel to maintain class and regulatory compliance.
            """
        }
    }
    return templates.get(template_name, {})
