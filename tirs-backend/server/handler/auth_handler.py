"""
注册认证功能接口，包括注册、登录、退出登录、检查登录状态等功能
"""

from flask import Blueprint, request, jsonify, session
from service.auth_service import AuthService
from config import Config
from utils.information_utils import export_universities_departments

# 创建注册认证蓝图
auth_blue = Blueprint('auth', __name__, url_prefix='/auth')


@auth_blue.route('/register', methods=['POST'])
def register():
    """
    用户注册接口（设计文档用例01）
    """
    data = request.json

    # 验证必需参数
    required_fields = ['user_id', 'password']
    if not all(field in data for field in required_fields):
        return jsonify({"error": "缺少必要参数: user_id 或 password"}), 400

    user_id = data['user_id'].strip()
    password = data['password']

    # 调用服务层
    register_result = AuthService.register_user(user_id, password)

    # 注册失败
    if not register_result["success"]:
        return jsonify({"error": register_result["message"]}), 400

    # 注册成功
    return jsonify({"message": register_result["message"]}), 200


@auth_blue.route('/login', methods=['POST'])
def login():
    """
    登录接口（设计文档用例01）
    只允许邮箱登录
    """
    data = request.json

    # 验证必需参数
    required_fields = ['user_id', 'password']
    if not all(field in data for field in required_fields):
        return jsonify({"error": "缺少必要参数: user_id 或 password"}), 400

    user_id = data['user_id'].strip()
    password = data['password']
    # export_universities_departments()  # 更新支持的大学和学院信息

    # 管理员登录
    if user_id.startswith(Config.ADMIN_ID_PREFIX):  # ADMIN_ID_PREFIX为管理员ID前缀，定义在config.py中
        login_result = AuthService.login_admin(user_id, password)
        # 登录失败
        if not login_result["success"]:
            return jsonify({"error": login_result["message"]}), 400

        # 登录成功
        export_universities_departments()  # 更新支持的大学和学院信息
        return jsonify({"message": login_result["message"], "role": login_result["role"], "admin_id": user_id}), 200

    # 普通用户登录
    else:
        login_result = AuthService.login_user(user_id, password)
        # 登录失败
        if not login_result["success"]:
            return jsonify({"error": login_result["message"]}), 400

        # 登录成功
        export_universities_departments()  # 更新支持的大学和学院信息
        return jsonify({"message": login_result["message"], "role": login_result["role"], "user_id": user_id}), 200


@auth_blue.route('/logout', methods=['POST'])
def logout():
    """
    退出登录接口
    """
    logout_result = AuthService.logout()
    # 退出失败
    if not logout_result["success"]:
        return jsonify({"error": logout_result["message"]}), 400

    return jsonify({"message": logout_result["message"]}), 200


@auth_blue.route('/check_session', methods=['GET'])
def check_session():
    """
    检查登录状态（设计文档用例01）
    """
    if 'logged_in' in session and session['logged_in']:
        response = {
            "logged_in": True,
            "role": session.get('role')
        }

        if session['role'] == '管理员':
            response['admin_id'] = session.get('admin_id')
        else:
            response['user_id'] = session.get('user_id')

        return jsonify(response), 200

    return jsonify({"logged_in": False}), 200
