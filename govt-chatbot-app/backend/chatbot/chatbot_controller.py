from flask import request, jsonify
from models.scheme_model import Scheme
from config.database import schemes_collection, chat_history_collection
from datetime import datetime
from bson import ObjectId

# Simple keyword-based response mapping
KEYWORDS = {
    "scheme": "We have various government schemes available. Please provide more details about what you're looking for.",
    "eligibility": "Eligibility criteria vary for different government schemes. Can you specify which scheme you're interested in?",
    "apply": "You can apply for most government schemes online or through designated offices. Which scheme are you interested in?",
    "document": "Most government schemes require identification documents like Aadhaar, PAN card, and income certificates. Specific requirements vary by scheme.",
    "benefit": "Government schemes offer various benefits like financial assistance, subsidies, healthcare, and educational support. Which area are you interested in?",
    "hello": "Hello! I'm a government scheme assistant. How can I help you today?",
    "hi": "Hi there! I can help you find information about government schemes. What would you like to know?",
    "help": "I can provide information about government schemes, eligibility criteria, application processes, and benefits. What would you like to know?"
}

def get_scheme_response(scheme_name):
    """Get detailed information about a specific scheme"""
    schemes = Scheme.find_by_query(scheme_name)
    
    if not schemes:
        return f"I couldn't find any scheme matching '{scheme_name}'. Please check the name or try another query."
    
    scheme = schemes[0]  # Get the first matching scheme
    
    response = f"**{scheme.name}**\n\n"
    response += f"**Description:** {scheme.description}\n\n"
    response += f"**Eligibility:** {scheme.eligibility_criteria}\n\n"
    response += f"**Required Documents:** {scheme.documents_required}\n\n"
    response += f"**How to Apply:** {scheme.application_process}\n\n"
    response += f"**Benefits:** {scheme.benefits}\n\n"
    
    if scheme.website:
        response += f"**Website:** {scheme.website}\n\n"
    
    if scheme.contact_info:
        response += f"**Contact:** {scheme.contact_info}"
    
    return response

def analyze_query(query):
    """Analyze the user query and return appropriate response"""
    query = query.lower()
    
    # Check if query contains scheme names
    schemes = Scheme.find_by_query(query)
    if schemes:
        scheme_names = [scheme.name.lower() for scheme in schemes]
        for name in scheme_names:
            if name.lower() in query:
                return get_scheme_response(name)
    
    # Check for keywords
    for keyword, response in KEYWORDS.items():
        if keyword in query:
            return response
    
    # Default response for no matches
    return "I'm not sure about that. Could you please provide more details or ask about specific government schemes?"

def process_message():
    try:
        data = request.get_json()
        user_message = data.get('message', '').lower()
        
        # Store chat history
        chat_history = {
            'user_message': user_message,
            'timestamp': datetime.utcnow(),
            'session_id': data.get('session_id')
        }
        
        # Basic response logic
        response = generate_response(user_message)
        
        # Store bot response
        chat_history['bot_response'] = response
        chat_history_collection.insert_one(chat_history)
        
        return jsonify({
            "success": True,
            "response": response
        }), 200
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500

def generate_response(message):
    # Basic keyword matching
    if 'hello' in message or 'hi' in message:
        return "Hello! I can help you find information about government schemes. What would you like to know?"
    
    if 'scheme' in message or 'schemes' in message:
        # Search for schemes in the database
        schemes = list(schemes_collection.find(
            {"$or": [
                {"name": {"$regex": message, "$options": "i"}},
                {"description": {"$regex": message, "$options": "i"}}
            ]}
        ).limit(3))
        
        if schemes:
            response = "I found these schemes that might interest you:\n\n"
            for scheme in schemes:
                response += f"- {scheme['name']}: {scheme['description'][:100]}...\n"
            return response
        else:
            return "I couldn't find any schemes matching your query. Could you please rephrase your question?"
    
    if 'eligibility' in message:
        return "To check eligibility for a specific scheme, please mention the scheme name and I'll provide the eligibility criteria."
    
    if 'apply' in message or 'application' in message:
        return "To get information about how to apply for a scheme, please mention the scheme name and I'll provide the application process."
    
    if 'benefit' in message or 'benefits' in message:
        return "To know about the benefits of a specific scheme, please mention the scheme name and I'll provide the details."
    
    return "I'm not sure I understand. Could you please rephrase your question? I can help you with information about government schemes, their eligibility criteria, benefits, and application process." 