from datetime import datetime
from bson import ObjectId
from config.db import get_db

db = get_db()
schemes_collection = db["schemes"]

class Scheme:
    def __init__(self, name, description, eligibility_criteria, documents_required, 
                 application_process, benefits, department, state=None, target_audience=None, 
                 start_date=None, end_date=None, website=None, contact_info=None, _id=None):
        self.name = name
        self.description = description
        self.eligibility_criteria = eligibility_criteria
        self.documents_required = documents_required
        self.application_process = application_process
        self.benefits = benefits
        self.department = department
        self.state = state
        self.target_audience = target_audience
        self.start_date = start_date
        self.end_date = end_date
        self.website = website
        self.contact_info = contact_info
        self._id = _id if _id else str(ObjectId())
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
    
    @classmethod
    def find_all(cls, limit=100, skip=0):
        """Retrieve all schemes with pagination"""
        cursor = schemes_collection.find({}).limit(limit).skip(skip)
        return [cls.from_mongo(scheme) for scheme in cursor]
    
    @classmethod
    def find_by_id(cls, scheme_id):
        """Find a scheme by its ID"""
        scheme = schemes_collection.find_one({"_id": scheme_id})
        return cls.from_mongo(scheme) if scheme else None
    
    @classmethod
    def find_by_query(cls, query, limit=100):
        """Search schemes by name, description, or department"""
        regex_query = {"$regex": query, "$options": "i"}
        cursor = schemes_collection.find({
            "$or": [
                {"name": regex_query},
                {"description": regex_query},
                {"department": regex_query},
                {"target_audience": regex_query}
            ]
        }).limit(limit)
        return [cls.from_mongo(scheme) for scheme in cursor]
    
    def save(self):
        """Save or update a scheme"""
        scheme_data = self.to_mongo()
        if schemes_collection.find_one({"_id": self._id}):
            scheme_data["updated_at"] = datetime.now()
            schemes_collection.update_one({"_id": self._id}, {"$set": scheme_data})
        else:
            schemes_collection.insert_one(scheme_data)
        return self
    
    def delete(self):
        """Delete a scheme"""
        result = schemes_collection.delete_one({"_id": self._id})
        return result.deleted_count > 0
    
    def to_mongo(self):
        """Convert instance to MongoDB document"""
        return {
            "_id": self._id,
            "name": self.name,
            "description": self.description,
            "eligibility_criteria": self.eligibility_criteria,
            "documents_required": self.documents_required,
            "application_process": self.application_process,
            "benefits": self.benefits,
            "department": self.department,
            "state": self.state,
            "target_audience": self.target_audience,
            "start_date": self.start_date,
            "end_date": self.end_date,
            "website": self.website,
            "contact_info": self.contact_info,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }
    
    @classmethod
    def from_mongo(cls, scheme_data):
        """Create instance from MongoDB document"""
        return cls(
            name=scheme_data.get("name"),
            description=scheme_data.get("description"),
            eligibility_criteria=scheme_data.get("eligibility_criteria"),
            documents_required=scheme_data.get("documents_required"),
            application_process=scheme_data.get("application_process"),
            benefits=scheme_data.get("benefits"),
            department=scheme_data.get("department"),
            state=scheme_data.get("state"),
            target_audience=scheme_data.get("target_audience"),
            start_date=scheme_data.get("start_date"),
            end_date=scheme_data.get("end_date"),
            website=scheme_data.get("website"),
            contact_info=scheme_data.get("contact_info"),
            _id=scheme_data.get("_id")
        ) 