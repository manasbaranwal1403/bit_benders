from flask import Blueprint
from controllers.scheme_controller import (
    get_schemes, get_scheme, create_scheme,
    update_scheme, delete_scheme, search_schemes
)
from middleware.api_key import require_api_key

scheme_bp = Blueprint('schemes', __name__)

# Public routes (with API key)
scheme_bp.route('/', methods=['GET'])(require_api_key(get_schemes))
scheme_bp.route('/<scheme_id>', methods=['GET'])(require_api_key(get_scheme))
scheme_bp.route('/search', methods=['GET'])(require_api_key(search_schemes))

# Protected routes (require both API key and authentication)
scheme_bp.route('/', methods=['POST'])(require_api_key(create_scheme))
scheme_bp.route('/<scheme_id>', methods=['PUT'])(require_api_key(update_scheme))
scheme_bp.route('/<scheme_id>', methods=['DELETE'])(require_api_key(delete_scheme)) 