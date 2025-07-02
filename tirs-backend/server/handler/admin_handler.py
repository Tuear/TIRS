"""
管理员功能接口，存放管理员可使用的功能接口
"""
from flask import Blueprint, request, jsonify
from flask import session
from service.database_service import DatabaseService
from service.review_service import ReviewService
from utils.status_monitor import get_platform_stats
from utils.status_monitor import get_user_information

# 创建推荐引擎蓝图
admin_blue = Blueprint('admin_function', __name__, url_prefix='/admin')

@admin_blue.route('/get_all_reviews', methods=['GET'])
def get_all_reviews():
    """
    获取所有评价接口
    功能：返回所有评价的列表，包括评价ID、导师姓名、学校、学院/系、评价内容等
    :return: 包含所有评价的列表
    """
    result = ReviewService.get_all_reviews()
    if not result["success"]:
        return jsonify({"error": result["message"]}), 400
    return jsonify(result)

@admin_blue.route('/get_all_users', methods=['GET'])
def get_all_users():
    """
    获取所有用户接口
    功能：返回所有用户的列表，包括用户ID、姓名、角色等
    :return: 包含所有用户的列表
    """
    user_db = DatabaseService('user')
    result = user_db.get_all_users()
    if not result["success"]:
        return jsonify({"error": result["message"]}), 400
    return jsonify(result)

@admin_blue.route('/delete_review', methods=['POST'])
def delete_review():
    """
    删除评价接口
    功能：根据评价ID删除指定的评价
    :param sentence_id: 评价ID
    """
    data = request.json
    sentence_id = data.get('sentence_id')
    # 添加参数校验
    if not sentence_id:
        return jsonify({"error": "缺少评价ID参数"}), 400

    result = ReviewService.delete_review(sentence_id)
    if not result["success"]:
        return jsonify({"error": result.get("message", "删除失败")}), 400
    return jsonify({"success": True})


@admin_blue.route('/toggle_permission', methods=['POST'])
def toggle_review_permission():
    """
    管理员切换用户评价权限接口
    请求参数：
    - target_user: 要操作的用户ID
    - enable: true/false 启用/禁用
    """
    # # 验证管理员权限
    # if session.get('role') != '管理员':
    #     return jsonify({"error": "权限不足"}), 403

    data = request.json
    required_fields = ['target_user', 'enable']
    if not all(field in data for field in required_fields):
        return jsonify({"error": "缺少必要参数"}), 400

    try:
        result = ReviewService.toggle_review_permission(
            target_user_id=data['target_user'],
            enable=data.get('enable', 'True')
        )

        if result["success"]:
            return jsonify(result), 200
        return jsonify({"error": result["message"]}), 400

    except Exception as e:
        return jsonify({"error": f"服务器错误: {str(e)}"}), 500

@admin_blue.route('/professor_update', methods=['POST'])
def professor_update():
    """
    导师信息维护接口
    """
    # # 验证管理员权限
    # if session.get('role') != '管理员':
    #     return jsonify({"error": "权限不足"}), 403

    data = request.json
    user_id = '管理员维护'

    # 验证必要字段
    required_fields = ['name', 'university', 'department', 'academic', 'responsibility', 'character', 'professor_url']
    if not all(field in data for field in required_fields):
        return jsonify({"error": "缺少必要参数"}), 400

    result = ReviewService.submit_review(data, user_id)

    if result["success"]:
        return jsonify({"message": "导师信息维护成功"}), 200
    return jsonify({"error": result["message"]}), 400


# 修改路由函数名称和调用方式
@admin_blue.route('/handle_platform_stats', methods=['GET'])
def handle_platform_stats():  # 修改函数名称避免冲突
    """
    平台监控数据接口
    返回：评价总数、学校学院统计、用户总数、内存占用
    """
    # if session.get('role') != '管理员':
    #     return jsonify({"error": "权限不足"}), 403
    try:
        return get_platform_stats()  # 调用模块中的函数
    except Exception as e:
        return jsonify({"error": f"获取统计失败: {str(e)}"}), 500


@admin_blue.route('/handle_user_information', methods=['POST'])
def handle_user_information():
    """
    获取所有用户及其评价信息接口
    返回：包含所有用户及其完整评价信息的嵌套结构
    """
    # if session.get('role') != '管理员':
    #     return jsonify({"error": "权限不足"}), 403

    try:
        data = request.json
        return get_user_information(data['user_id'])
    except Exception as e:
        return jsonify({"error": f"获取数据失败: {str(e)}"}), 500