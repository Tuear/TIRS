"""
用户功能接口，存放用户可使用的功能接口
"""
from flask import Blueprint, request, jsonify
from service.recommendation_service import RecommendationService
from flask import session
from service.database_service import DatabaseService
from service.review_service import ReviewService

# 创建推荐引擎蓝图
user_blue = Blueprint('user_function', __name__, url_prefix='/user')


@user_blue.route('/get_recommendations', methods=['POST'])
def get_recommendations():
    """
    获取推荐结果接口
    功能：接收用户输入的查询文本，解析需求并返回推荐结果
    """
    data = request.json
    query = data.get('query', '').strip()  # 查询语句
    university = data.get('university', '').strip()  # 学校
    department = data.get('department', '').strip()  # 学院/系

    # 检查输入是否为空
    if not query:
        return jsonify({"error": "请输入查询内容"}), 400
    if not university:
        return jsonify({"error": "请输入学校"}), 400
    if not department:
        return jsonify({"error": "请输入学院/系"}), 400

    # 调用推荐服务获取结果（包含解析和推荐两个步骤）
    query_result = RecommendationService.get_recommendations(query, university, department)
    # 失败返回错误信息
    if not query_result["success"]:
        return jsonify({"error": query_result["message"]}), 400

    # 成功返回推荐结果
    return jsonify({"commend_result": query_result["message"]}), 200


@user_blue.route('/submit_review', methods=['POST'])
def submit_review():
    """
    提交评价接口
    功能：接收用户提交的评价信息，保存到数据库
    """
    data = request.json
    user_id = data.get('user_id')

    # 权限校验
    user_db = DatabaseService('user')
    user_info = user_db.get_user(user_id)
    review_allowed = user_info.get('review_allowed', 'True')  # 默认允许提交
    if review_allowed == 'False':
        return jsonify({"error": "你已暂时被限制提交评价"}), 403

    # 原有参数校验保持不变
    required_fields = ['name', 'university', 'department', 'academic', 'responsibility', 'character']
    if not all(field in data for field in required_fields):
        return jsonify({"error": "缺少必要参数"}), 400

    result = ReviewService.submit_review(data, user_id)

    if result["success"]:
        return jsonify({"message": result["message"]}), 200
    return jsonify({"error": result["message"]}), 400


@user_blue.route('/show_information', methods=['POST'])
def show_information():
    """
       查看导师信息接口
       功能：根据导师ID返回基本信息连接及评价内容
    """
    data = request.json
    tutor_id = data.get('tutor_id')

    if not tutor_id:
        return jsonify({"error": "缺少导师ID参数"}), 400

    result = RecommendationService.show_professor_information(tutor_id)

    if result["success"]:
        return jsonify(result["data"]), 200
    return jsonify({"error": result["message"]}), 400
