from datetime import datetime
from bson import ObjectId

class Scheme:
    def __init__(self, name, description, eligibility, benefits, documents_required, 
                 application_process, website, contact_info, category, status="active"):
        self.name = name
        self.description = description
        self.eligibility = eligibility
        self.benefits = benefits
        self.documents_required = documents_required
        self.application_process = application_process
        self.website = website
        self.contact_info = contact_info
        self.category = category
        self.status = status
        self.created_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()

    def to_dict(self):
        return {
            "name": self.name,
            "description": self.description,
            "eligibility": self.eligibility,
            "benefits": self.benefits,
            "documents_required": self.documents_required,
            "application_process": self.application_process,
            "website": self.website,
            "contact_info": self.contact_info,
            "category": self.category,
            "status": self.status,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }

    @staticmethod
    def from_dict(data):
        scheme = Scheme(
            name=data["name"],
            description=data["description"],
            eligibility=data["eligibility"],
            benefits=data["benefits"],
            documents_required=data["documents_required"],
            application_process=data["application_process"],
            website=data["website"],
            contact_info=data["contact_info"],
            category=data["category"],
            status=data.get("status", "active")
        )
        if "_id" in data:
            scheme._id = data["_id"]
        return scheme 