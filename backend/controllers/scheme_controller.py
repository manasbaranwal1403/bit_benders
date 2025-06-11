from flask import jsonify, request
from models.scheme import Scheme
from models.user import User
from utils.email_service import EmailService
from controllers.auth_controller import token_required

# Initialize email service
email_service = EmailService()

def get_schemes():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    
    schemes = Scheme.objects.paginate(page=page, per_page=per_page)
    
    return jsonify({
        'schemes': [scheme.to_dict() for scheme in schemes.items],
        'total': schemes.total,
        'pages': schemes.pages,
        'current_page': schemes.page
    })

def get_scheme(scheme_id):
    scheme = Scheme.objects(id=scheme_id).first()
    if not scheme:
        return jsonify({'message': 'Scheme not found!'}), 404
    
    return jsonify(scheme.to_dict())

def search_schemes():
    query = request.args.get('q', '')
    if not query:
        return jsonify({'message': 'Search query is required!'}), 400
    
    schemes = Scheme.objects.search_text(query).order_by('$text_score')
    return jsonify([scheme.to_dict() for scheme in schemes])

@token_required
def create_scheme(current_user):
    if current_user.role != 'admin':
        return jsonify({'message': 'Unauthorized!'}), 403
    
    data = request.get_json()
    scheme = Scheme(**data)
    scheme.save()
    
    # Send notifications to all users
    users = User.objects(role='user')
    for user in users:
        email_service.send_new_scheme_notification(user, scheme)
    
    return jsonify(scheme.to_dict()), 201

@token_required
def update_scheme(current_user, scheme_id):
    if current_user.role != 'admin':
        return jsonify({'message': 'Unauthorized!'}), 403
    
    scheme = Scheme.objects(id=scheme_id).first()
    if not scheme:
        return jsonify({'message': 'Scheme not found!'}), 404
    
    data = request.get_json()
    scheme.update(**data)
    scheme.reload()
    
    return jsonify(scheme.to_dict())

@token_required
def delete_scheme(current_user, scheme_id):
    if current_user.role != 'admin':
        return jsonify({'message': 'Unauthorized!'}), 403
    
    scheme = Scheme.objects(id=scheme_id).first()
    if not scheme:
        return jsonify({'message': 'Scheme not found!'}), 404
    
    scheme.delete()
    return jsonify({'message': 'Scheme deleted successfully!'})