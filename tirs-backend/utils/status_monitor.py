import os
import psutil
from service.database_service import DatabaseService
from flask import jsonify
from collections import defaultdict
from collections import OrderedDict


def get_platform_stats():
    """
    获取平台统计信息
    返回：评价总数、学校总数、学院总数、用户总数、内存占用
    """
    # 1. 获取评价总数
    review_db = DatabaseService('professor')
    review_count = review_db.execute_query(
        "SELECT COUNT(*) FROM review_sentences",
        fetch_one=True
    )[0]

    # 2. 获取学校/学院统计（并计算聚合值）
    school_stats = review_db.execute_query('''
        SELECT university, department, COUNT(*) as count 
        FROM professor 
        GROUP BY university, department
    ''')

    # 处理成层级结构（保留原逻辑，用于后续聚合）
    school_data = defaultdict(lambda: {"departments": {}, "total": 0})
    for uni, dept, count in school_stats:
        school_data[uni]["departments"][dept] = count
        school_data[uni]["total"] += count

    # 🔴 新增：计算“学校总数”和“学院总数”
    schools_total = len(school_data)  # 不同大学的数量
    departments_total = sum(
        len(school["departments"]) for school in school_data.values()
    )  # 所有大学的学院数量之和

    # 3. 获取用户总数
    user_db = DatabaseService('user')
    user_count = user_db.execute_query(
        "SELECT COUNT(*) FROM user",
        fetch_one=True
    )[0]

    # 4. 获取内存占用（单位：MB）
    process = psutil.Process(os.getpid())
    memory_usage = round(process.memory_info().rss / 1024 / 1024, 2)

    # 🔴 调整返回结构：让 schools 包含 total（学校总数）和 departments（学院总数）
    return jsonify({
        "review_count": review_count,
        "schools": {
            "total": schools_total,        # 学校总数
            "departments": departments_total  # 学院总数
        },
        "user_count": user_count,
        "memory_usage": f"{memory_usage} MB"
    })


from collections import OrderedDict


def get_user_information(user_id):
    """
    获取指定用户的相关信息
    返回结构：
    {
        "user": {
            "user_id": "用户ID",
            "role": "角色",
            "review_allowed": "是否允许评价",
            "reviews": [ ... ]
        }
    }
    """
    try:
        user_db = DatabaseService('user')
        professor_db = DatabaseService('professor')

        # 获取指定用户基本信息
        user_info = user_db.execute_query(
            '''
            SELECT u.user_id, u.role, u.review_allowed 
            FROM user u
            WHERE u.user_id = ?
            ''',
            (user_id,),
            fetch_one=True  # 只获取一条记录
        )

        # 如果用户不存在
        if not user_info:
            return jsonify({"error": "用户不存在"}), 404

        # 构建用户基本信息
        user_id = user_info[0]
        role = user_info[1]
        review_allowed = user_info[2]

        # 获取该用户的所有评价
        reviews = professor_db.execute_query(
            '''
            SELECT s.sentence_id, p.name, p.university, p.department, 
                   s.review_sentence
            FROM review_sentences s
            JOIN professor p ON s.tutor_id = p.tutor_id
            WHERE s.user_id = ?
            ''',
            (user_id,)
        )

        # 使用OrderedDict确保字段顺序
        user_obj = OrderedDict()
        user_obj["user_id"] = user_id
        user_obj["role"] = role
        user_obj["review_allowed"] = review_allowed

        # 创建review列表
        review_list = []
        for row in reviews:
            review_dict = OrderedDict([
                ("sentence_id", row[0]),
                ("tutor_name", row[1]),
                ("university", row[2]),
                ("department", row[3]),
                ("review_sentence", row[4])
            ])
            review_list.append(review_dict)

        user_obj["reviews"] = review_list

        # 返回单个用户对象
        return jsonify({"user": user_obj})

    except Exception as e:
        return jsonify({"error": str(e)}), 500