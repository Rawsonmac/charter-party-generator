import psycopg2
from psycopg2.extras import Json
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Database connection
def get_db_connection():
    return psycopg2.connect(
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT")
    )

# Initialize database with templates table
def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS templates (
            id SERIAL PRIMARY KEY,
            template_name VARCHAR(255) UNIQUE,
            terms JSONB
        );
    """)
    conn.commit()
    cursor.close()
    conn.close()

# Load template from database
def load_template(template_name):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT terms FROM templates WHERE template_name = %s", (template_name,))
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    return result[0] if result else {}

# Save template to database
def save_template(template_name, terms):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO templates (template_name, terms)
        VALUES (%s, %s)
        ON CONFLICT (template_name) DO UPDATE
        SET terms = EXCLUDED.terms
    """, (template_name, Json(terms)))
    conn.commit()
    cursor.close()
    conn.close()

# Get all template names
def get_template_names():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT template_name FROM templates")
    names = [row[0] for row in cursor.fetchall()]
    cursor.close()
    conn.close()
    return names

# Initialize default templates if not already in database
def initialize_default_templates():
    default_templates = {
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
    for name, terms in default_templates.items():
        save_template(name, terms)

# Run initialization
init_db()
initialize_default_templates()
