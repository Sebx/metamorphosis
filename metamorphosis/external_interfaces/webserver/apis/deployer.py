from flask import jsonify
from app.models import User

@bp.route('/users/<int:id>', methods=['GET'])
def get_user(id):
    return jsonify(User.query.get_or_404(id).to_dict())

class deployer(object):
    """description of class"""


