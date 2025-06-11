from flask import Flask, jsonify
from flask_cors import CORS
from routes.scheme_routes import scheme_bp
from routes.auth_routes import auth
from chatbot.chatbot_controller import process_message
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS

# Register blueprints
app.register_blueprint(scheme_bp, url_prefix='/api/schemes')
app.register_blueprint(auth, url_prefix='/api/auth')

# Chatbot endpoint
app.route('/api/chatbot', methods=['POST'])(process_message)

# Health check endpoint
@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({"status": "ok"}), 200

# Error handlers
@app.errorhandler(404)
def not_found(error):
    return jsonify({"success": False, "message": "Resource not found"}), 404

@app.errorhandler(500)
def server_error(error):
    return jsonify({"success": False, "message": "Internal server error"}), 500

if __name__ == "__main__":
    app.run(debug=True, port=5000) 