from flask import Blueprint

#  SuperAdmin authentication views
from .views.auth import SuperAdminView

module = Blueprint('super_admin',__name__,url_prefix='/super-admin/api')

#  SuperAdmin authentication routes
module.add_url_rule('/signup', 'signup', SuperAdminView.signup, methods=['POST'])
module.add_url_rule('/login','login', SuperAdminView.login, methods=['POST'])
module.add_url_rule('/update/<int:id>','update', SuperAdminView.update, methods=['PUT'])
module.add_url_rule('/dashboard','dashboard', SuperAdminView.dashboard, methods=['GET'])
module.add_url_rule('/logout','logout', SuperAdminView.logout, methods=['GET'])
module.add_url_rule('/delete/<int:id>', 'delete', SuperAdminView.delete,methods=['DELETE'])
