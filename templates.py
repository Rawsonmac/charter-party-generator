def load_template(template_name):
    templates = {
        "Shell Time 4": {
            "Vessel Name": "TBN",
            "Charterer": "[Charterer Name]",
            "Period": "12 months +/- 1 month",
            "Hire Rate": "[To be specified] USD/day",
            "Delivery Port": "[To be specified]",
            "Redelivery Port": "[To be specified]",
            "Route": "Any",
            "Standard Clauses": """
                1. Vessel to comply with ISM and ISPS codes.
                2. Charterer to pay port costs and bunkers.
                3. Owners to maintain vessel insurance and class certification.
                4. Hire payment due monthly in advance.
            """,
            "Modern Clauses": """
                1. Compliance with IMO 2020 sulfur limits.
                2. Sanctions compliance with U.S., EU, and UN regulations.
                3. Force majeure includes pandemics and geopolitical disruptions.
                4. Support for electronic Bills of Lading (e-BL).
            """
        },
        "Asbatankvoy 2025": {
            "Vessel Name": "TBN",
            "Charterer": "[Charterer Name]",
            "Cargo": "Crude Oil",
            "Cargo Capacity": "[To be specified] tons",
            "Load Port": "[To be specified]",
            "Discharge Port": "[To be specified]",
            "Laytime": "72 hours",
            "Demurrage": "[To be specified] USD/day",
            "Freight Rate": "[To be specified] Worldscale points",
            "Route": "Any",
            "Standard Clauses": """
                1. Freight payable upon completion of discharge.
                2. Laytime not to commence before 0600 on ETA unless agreed.
                3. Owners to provide safe berth.
                4. Arbitration in New York, London, Singapore, or Hong Kong (New York default).
            """,
            "Modern Clauses": """
                1. Compliance with ESG and carbon intensity reporting.
                2. Support for electronic Bills of Lading (e-BL).
                3. Sanctions compliance with U.S., EU, and UN regulations.
                4. Force majeure includes port disruptions and pandemics.
            """
        },
        "Shellvoy 6": {
            "Vessel Name": "TBN",
            "Charterer": "[Charterer Name]",
            "Cargo": "Crude Oil or Products",
            "Cargo Capacity": "[To be specified] tons",
            "Load Port": "[To be specified]",
            "Discharge Port": "[To be specified]",
            "Laytime": "72 hours",
            "Demurrage": "[To be specified] USD/day",
            "Freight Rate": "[To be specified] Worldscale points",
            "Route": "Any",
            "Standard Clauses": """
                1. NOR invalid if free pratique not granted within 6 hours of tendering.
                2. Charterer responsible for port costs.
                3. Vessel to comply with ship-to-ship transfer protocols.
                4. Time lost due to vessel condition not to count as laytime.
            """,
            "Modern Clauses": """
                1. Compliance with IMO 2020 sulfur limits.
                2. Sanctions compliance with U.S., EU, and UN regulations.
                3. Force majeure includes geopolitical disruptions.
                4. Support for electronic Bills of Lading (e-BL).
            """
        },
        "BPVOY4": {
            "Vessel Name": "TBN",
            "Charterer": "[Charterer Name]",
            "Cargo": "Crude Oil or Products",
            "Cargo Capacity": "[To be specified] tons",
            "Load Port": "[To be specified]",
            "Discharge Port": "[To be specified]",
            "Laytime": "72 hours",
            "Demurrage": "[To be specified] USD/day",
            "Freight Rate": "[To be specified] Worldscale points",
            "Route": "Any",
            "Standard Clauses": """
                1. Balanced terms for owners and charterers.
                2. Freight payable upon completion of discharge.
                3. Vessel to comply with modern safety and environmental regulations.
                4. Reduced need for rider clauses due to comprehensive terms.
            """,
            "Modern Clauses": """
                1. Compliance with IMO 2020 sulfur limits.
                2. Support for digital reporting and e-BL.
                3. Sanctions compliance with U.S., EU, and UN regulations.
                4. Force majeure includes pandemics and port disruptions.
            """
        },
        "ExxonMobil Voy2000": {
            "Vessel Name": "TBN",
            "Charterer": "[Charterer Name]",
            "Cargo": "Crude Oil or Products",
            "Cargo Capacity": "[To be specified] tons",
            "Load Port": "[To be specified]",
            "Discharge Port": "[To be specified]",
            "Laytime": "72 hours",
            "Demurrage": "[To be specified] USD/day",
            "Freight Rate": "[To be specified] Worldscale points",
            "Route": "Any",
            "Standard Clauses": """
                1. Clear and concise terms for loading and discharge.
                2. Charterer to provide safe port/berth.
                3. Freight payable upon completion of discharge.
                4. Vessel to maintain class and regulatory compliance.
            """,
            "Modern Clauses": """
                1. Compliance with IMO 2020 sulfur limits.
                2. Sanctions compliance with U.S., EU, and UN regulations.
                3. Force majeure includes geopolitical disruptions.
                4. Support for electronic Bills of Lading (e-BL).
            """
        },
        "INTERTANKVOY 76": {
            "Vessel Name": "TBN",
            "Charterer": "[Charterer Name]",
            "Cargo": "Crude Oil or Products",
            "Cargo Capacity": "[To be specified] tons",
            "Load Port": "[To be specified]",
            "Discharge Port": "[To be specified]",
            "Laytime": "72 hours",
            "Demurrage": "[To be specified] USD/day",
            "Freight Rate": "[To be specified] Worldscale points",
            "Route": "Any",
            "Standard Clauses": """
                1. Freight payable upon completion of loading.
                2. Laytime to commence 6 hours after NOR unless otherwise agreed.
                3. Owners to ensure vessel suitability for cargo.
                4. Charterer to nominate safe port/berth.
            """,
            "Modern Clauses": """
                1. Compliance with IMO 2020 sulfur limits.
                2. Support for electronic Bills of Lading (e-BL).
                3. Sanctions compliance with U.S., EU, and UN regulations.
                4. Force majeure includes pandemics and port disruptions.
            """
        }
    }
    return templates.get(template_name, {})

def get_template_names():
    return [
        "Shell Time 4",
        "Asbatankvoy 2025",
        "Shellvoy 6",
        "BPVOY4",
        "ExxonMobil Voy2000",
        "INTERTANKVOY 76"
    ]

def suggest_templates_by_route(route):
    common_routes = {
        "Houston to Rotterdam": ["Asbatankvoy 2025", "Shellvoy 6", "BPVOY4", "ExxonMobil Voy2000", "INTERTANKVOY 76"],
        "Persian Gulf to Singapore": ["Asbatankvoy 2025", "Shellvoy 6", "ExxonMobil Voy2000", "INTERTANKVOY 76"],
        "West Africa to China": ["Asbatankvoy 2025", "Shellvoy 6", "BPVOY4", "INTERTANKVOY 76"],
        "Any": ["Shell Time 4", "Asbatankvoy 2025", "Shellvoy 6", "BPVOY4", "ExxonMobil Voy2000", "INTERTANKVOY 76"]
    }
    route = route.lower() if route else "Any"
    for key in common_routes:
        if key.lower() in route or route in key.lower():
            return common_routes[key]
    return ["Any"]

def adjust_terms_by_vessel_class(template, vessel_class):
    vessel_classes = {
        "Panamax": {"Cargo Capacity": "60,000 tons", "Freight Rate": "WS100–WS150", "Demurrage": "$20,000/day"},
        "Aframax": {"Cargo Capacity": "80,000–100,000 tons", "Freight Rate": "WS90–WS140", "Demurrage": "$25,000/day"},
        "Suezmax": {"Cargo Capacity": "120,000–150,000 tons", "Freight Rate": "WS80–WS130", "Demurrage": "$30,000/day"},
        "VLCC": {"Cargo Capacity": "200,000–250,000 tons", "Freight Rate": "WS50–WS100", "Demurrage": "$40,000/day"},
        "ULCC": {"Cargo Capacity": "300,000+ tons", "Freight Rate": "WS40–WS90", "Demurrage": "$50,000/day"}
    }
    adjusted_template = template.copy()
    if vessel_class in vessel_classes:
        class_data = vessel_classes[vessel_class]
        if "Cargo Capacity" in adjusted_template:
            adjusted_template["Cargo Capacity"] = class_data["Cargo Capacity"]
        if "Freight Rate" in adjusted_template:
            adjusted_template["Freight Rate"] = class_data["Freight Rate"]
        if "Demurrage" in adjusted_template:
            adjusted_template["Demurrage"] = class_data["Demurrage"]
    return adjusted_template
