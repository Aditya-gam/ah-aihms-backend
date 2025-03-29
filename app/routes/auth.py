from flask import Blueprint, jsonify

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/status', methods=['GET'])
def status():
    return jsonify({"status": "auth route working"}), 200
