from flask import Blueprint
from controllers.auth_controller import (
    register, login, get_profile, token_required,
    request_password_reset, reset_password
)

auth = Blueprint('auth', __name__)

# Public routes
auth.route('/register', methods=['POST'])(register)
auth.route('/login', methods=['POST'])(login)
auth.route('/request-reset', methods=['POST'])(request_password_reset)
auth.route('/reset-password', methods=['POST'])(reset_password)

# Protected routes
auth.route('/profile', methods=['GET'])(token_required(get_profile)) 