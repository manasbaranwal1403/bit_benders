from database import db, schemes_collection, users_collection
from datetime import datetime

def create_indexes():
    # Create text indexes for better search performance
    schemes_collection.create_index([
        ("name", "text"),
        ("description", "text"),
        ("category", "text")
    ])
    
    # Create compound index for status and category
    schemes_collection.create_index([
        ("status", 1),
        ("category", 1)
    ])
    
    # Create index for users collection
    users_collection.create_index("email", unique=True)
    users_collection.create_index("username", unique=True)

def add_initial_data():
    # Add sample schemes
    sample_schemes = [
        {
            "name": "Pradhan Mantri Awas Yojana",
            "description": "Housing for All by 2022 - Urban mission for providing housing to all urban poor",
            "eligibility": "Economically Weaker Section (EWS), Low Income Group (LIG), Middle Income Group (MIG)",
            "benefits": "Interest subsidy on home loans, affordable housing units",
            "documents_required": "Aadhaar Card, Income Certificate, Bank Statement",
            "application_process": "Apply through official website or visit nearest Common Service Centre",
            "website": "https://pmaymis.gov.in",
            "contact_info": "1800-11-3377",
            "category": "Housing",
            "status": "active",
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        },
        {
            "name": "Pradhan Mantri Kisan Samman Nidhi",
            "description": "Income support of Rs.6000 per year to all farmer families",
            "eligibility": "Small and marginal farmer families with combined landholding up to 2 hectares",
            "benefits": "Direct income support of Rs.6000 per year in three equal installments",
            "documents_required": "Aadhaar Card, Land Records, Bank Account Details",
            "application_process": "Register at nearest Common Service Centre or through official website",
            "website": "https://pmkisan.gov.in",
            "contact_info": "155261",
            "category": "Agriculture",
            "status": "active",
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        },
        {
            "name": "Ayushman Bharat Yojana",
            "description": "National Health Protection Scheme providing health coverage up to Rs.5 lakhs per family per year",
            "eligibility": "Families identified as deprived and vulnerable based on SECC database",
            "benefits": "Health coverage up to Rs.5 lakhs per family per year for secondary and tertiary care hospitalization",
            "documents_required": "Aadhaar Card, Ration Card, Income Certificate",
            "application_process": "Visit nearest empaneled hospital or Common Service Centre",
            "website": "https://pmjay.gov.in",
            "contact_info": "14555",
            "category": "Healthcare",
            "status": "active",
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        }
    ]
    
    # Add sample admin user
    admin_user = {
        "username": "admin",
        "email": "admin@example.com",
        "password": "hashed_password_here",  # In production, use proper password hashing
        "role": "admin",
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    }
    
    try:
        # Insert schemes
        schemes_collection.insert_many(sample_schemes)
        print("Sample schemes added successfully")
        
        # Insert admin user
        users_collection.insert_one(admin_user)
        print("Admin user added successfully")
        
    except Exception as e:
        print(f"Error adding initial data: {str(e)}")

if __name__ == "__main__":
    create_indexes()
    add_initial_data() 