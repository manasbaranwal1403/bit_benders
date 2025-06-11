from flask import request, jsonify
from models.scheme import Scheme
from config.database import schemes_collection
from bson import ObjectId
from datetime import datetime
from utils.notifier import send_notification

def get_all_schemes():
    try:
        page = int(request.args.get('page', 1))
        limit = int(request.args.get('limit', 10))
        skip = (page - 1) * limit

        schemes = list(schemes_collection.find().skip(skip).limit(limit))
        total = schemes_collection.count_documents({})

        # Convert ObjectId to string for JSON serialization
        for scheme in schemes:
            scheme['_id'] = str(scheme['_id'])

        return jsonify({
            "success": True,
            "data": schemes,
            "total": total,
            "page": page,
            "limit": limit
        }), 200
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500

def get_scheme_by_id(scheme_id):
    try:
        scheme = schemes_collection.find_one({"_id": ObjectId(scheme_id)})
        if scheme:
            scheme['_id'] = str(scheme['_id'])
            return jsonify({"success": True, "data": scheme}), 200
        return jsonify({"success": False, "message": "Scheme not found"}), 404
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500

def create_scheme():
    try:
        data = request.get_json()
        scheme = Scheme(
            name=data['name'],
            description=data['description'],
            eligibility=data['eligibility'],
            benefits=data['benefits'],
            documents_required=data['documents_required'],
            application_process=data['application_process'],
            website=data['website'],
            contact_info=data['contact_info'],
            category=data['category']
        )
        
        result = schemes_collection.insert_one(scheme.to_dict())
        return jsonify({
            "success": True,
            "message": "Scheme created successfully",
            "id": str(result.inserted_id)
        }), 201
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500

def update_scheme(scheme_id):
    try:
        data = request.get_json()
        data['updated_at'] = datetime.utcnow()
        
        result = schemes_collection.update_one(
            {"_id": ObjectId(scheme_id)},
            {"$set": data}
        )
        
        if result.modified_count:
            return jsonify({"success": True, "message": "Scheme updated successfully"}), 200
        return jsonify({"success": False, "message": "Scheme not found"}), 404
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500

def delete_scheme(scheme_id):
    try:
        result = schemes_collection.delete_one({"_id": ObjectId(scheme_id)})
        if result.deleted_count:
            return jsonify({"success": True, "message": "Scheme deleted successfully"}), 200
        return jsonify({"success": False, "message": "Scheme not found"}), 404
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500

def search_schemes():
    try:
        query = request.args.get('q', '')
        if not query:
            return jsonify({"success": False, "message": "Search query is required"}), 400

        # Create text search query
        search_query = {
            "$or": [
                {"name": {"$regex": query, "$options": "i"}},
                {"description": {"$regex": query, "$options": "i"}},
                {"category": {"$regex": query, "$options": "i"}}
            ]
        }

        schemes = list(schemes_collection.find(search_query))
        
        # Convert ObjectId to string for JSON serialization
        for scheme in schemes:
            scheme['_id'] = str(scheme['_id'])

        return jsonify({
            "success": True,
            "data": schemes
        }), 200
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500 