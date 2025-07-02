import re
from service.database_service import DatabaseService
from utils.password_utils import hash_password, verify_password
from flask import session
from config import Config
from utils.sensitive_filter import SensitiveFilter

# 启动用户数据库服务
user_db = DatabaseService('user')


# 认证服务类
class AuthService:
    @staticmethod
    def register_user(user_id: str, password: str):
        """
        用户注册（设计文档用例01）
        """
        # 验证用户ID格式
        register_result = AuthService._validate_user_id(user_id)
        if not register_result[0]:
            return {"success": False, "message": register_result[1]}

        # 检查用户是否已存在
        if user_db.user_exists(user_id):
            return {"success": False, "message": "该用户ID已被注册"}

        # 验证密码强度
        if len(password) < 6:
            return {"success": False, "message": "密码长度至少6位"}

        # 加密密码
        hashed_pw = hash_password(password)

        # 创建用户
        user_db.create_user(user_id, hashed_pw)

        return {"success": True, "message": "注册成功"}

    @staticmethod
    def login_user(user_id: str, password: str):
        """
        用户登录（设计文档用例01）
        """
        # 验证用户ID格式
        login_result = AuthService._validate_user_id(user_id)
        if not login_result[0]:
            return {"success": False, "message": login_result[1]}

        # 获取用户数据
        user_data = user_db.get_user(user_id)
        if not user_data:
            return {"success": False, "message": "用户不存在"}

        # 验证密码
        if not verify_password(password, user_data['hashed_password']):
            return {"success": False, "message": "密码错误"}

        # 设置session
        session['user_id'] = user_id
        session['role'] = user_data['role']
        session['logged_in'] = True

        return {"success": True, "role": user_data['role'], "message": "登录成功"}

    @staticmethod
    def login_admin(admin_id: str, password: str):
        """
        管理员登录（设计文档用例01）
        """
        # 必须是管理员ID格式
        if not admin_id.startswith(Config.ADMIN_ID_PREFIX):
            return {"success": False, "message": "无效的管理员ID"}

        # 获取管理员数据
        admin_data = user_db.get_admin(admin_id)
        if not admin_data:
            return {"success": False, "message": "管理员不存在"}

        # 验证密码
        if not verify_password(password, admin_data['password']):
            return {"success": False, "message": "密码错误"}

        # 设置session
        session['admin_id'] = admin_id
        session['role'] = '管理员'
        session['logged_in'] = True

        return {"success": True, "role": "管理员", "message": "管理员登录成功"}

    @staticmethod
    def logout():
        """
        退出登录
        """
        session.clear()
        return {"success": True, "message": "已退出登录"}

    @staticmethod
    def _validate_user_id(user_id: str) -> tuple:
        """
        验证用户ID格式（支持中英文自定义ID）
        新规则：
        1. 长度在4-20个字符之间（中文算1个字符）
        2. 允许使用中文字符、英文字母、数字、下划线(_)、连字符(-)、点号(.)
        3. 必须以字母或中文开头
        4. 不能包含空格
        5. 不能包含敏感词或特殊符号
        """
        # 检查长度
        if len(user_id) < 2:
            return False, "ID长度至少需要2个字符"
        if len(user_id) > 10:
            return False, "ID长度不能超过10个字符"

        # 检查是否包含空格
        if ' ' in user_id:
            return False, "ID不能包含空格"

        # 检查开头字符（必须以字母或中文开头）
        first_char = user_id[0]
        if not (first_char.isalpha() or '\u4e00' <= first_char <= '\u9fff'):
            return False, "ID必须以字母或中文开头"

        # 检查允许的字符集
        pattern = r'^[a-zA-Z0-9\u4e00-\u9fff_\-\.]+$'
        if not re.match(pattern, user_id):
            return False, "ID只能包含中文字符、英文字母、数字、下划线、连字符和点号"

        # 检查常见非法用户名模式
        if user_id.startswith(('admin', 'root', 'system', 'administrator')):
            return False, "该ID为系统保留字"

        # 检查敏感词（可选，根据需求开启）
        if SensitiveFilter.check(user_id):  # 使用之前实现的敏感词检测
            return False, "ID包含敏感词"

        # 所有检查通过
        return True,  "ID格式正确"
