from flask import Blueprint

#  admin authentication views
from .views.auth import student
from .views.personal import PersonalInfo
from .views.academic import AcademicProfile
from .views.personal import StudentAvatarView

module = Blueprint('student',__name__,url_prefix='/api/student/')


""" Routes for Student Creation & Authentication """
#
module.add_url_rule('/dashboard', 'student_dashboard', student.student_dashboard, methods=['GET'])
module.add_url_rule('/students', 'students', student.students, methods=['GET'])
module.add_url_rule('/<int:id>/student', 'student', student.student, methods=['GET'])
module.add_url_rule('/create', 'create', student.create, methods=['POST'])
module.add_url_rule('/login', 'login', student.login, methods=['POST'])
module.add_url_rule('/logout', 'logout', student.logout, methods=['GET'])
module.add_url_rule('/<int:id>/update', 'update', student.update, methods=['PUT'])
module.add_url_rule('/<int:id>/delete', 'delete', student.delete, methods=['DELETE'])
module.add_url_rule('/password-reset', 'password_reset', student.password_reset, methods=['POST'])


""" Routes for Student's Personal Information """

module.add_url_rule('/<int:id>/address', 'student_address', PersonalInfo.addresses, methods=['GET'])
module.add_url_rule('/<int:id>/address/create', 'create_address', PersonalInfo.create_address, methods=['POST'])
module.add_url_rule('/<int:id>/address/update', 'update_address', PersonalInfo.update_address, methods=['PUT'])
module.add_url_rule('/<int:id>/address/delete', 'delete_address', PersonalInfo.delete_address, methods=['DELETE'])


""" Routes for Student's Academic Information """

module.add_url_rule('/<int:id>/academic', 'profiles', AcademicProfile.profiles, methods=['GET'])
module.add_url_rule('/<int:id>/academic/create', 'create_profile', AcademicProfile.create_profile, methods=['POST'])
module.add_url_rule('/<int:id>/academic/update', 'update_profile', AcademicProfile.update_profile, methods=['PUT'])


module.add_url_rule('/avatar/upload','upload_avatar', StudentAvatarView.upload_avatar, methods=["POST"])
