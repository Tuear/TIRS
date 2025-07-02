from utils.sensitive_filter import SensitiveFilter
from service.recommendation_service import RecommendationService
from service.database_service import DatabaseService
from uuid import uuid4
from utils.information_utils import write_professor_info_url



# 评价服务类
class ReviewService:
    @staticmethod
    def submit_review(review_data, user_id, url=''):
        """
        处理评价提交（设计文档用例03）
        """
        # 构建评价语句
        review_sentence = f"{review_data['academic']}，{review_data['responsibility']}，{review_data['character']}"

        # 检查评价内容是否合规
        if SensitiveFilter.check(review_sentence):
            return {"success": False, "message": "评价内容不合规！请重新填写评价内容。"}

        # 合并特征文本（按需求可调整格式）
        review_features = f"学术特征:{review_data['academic']}|responsibility:{review_data['responsibility']}|人品:{review_data['character']}"

        # 调用本类方法生成唯导师一ID
        tutor_id = RecommendationService.generate_professor_id(
            review_data['name'],
            review_data['university'],
            review_data['department']
        )
        tutor_id = f"tutor_{str(tutor_id)}"

        # 生成唯一评价语句ID
        sentence_id = f"sentence_{str(uuid4()).replace('-', '')}"

        # 生成唯一评价特征ID
        feature_id = f"review_{str(uuid4()).replace('-', '')}"

        # 获取数据库服务实例
        professor_db = DatabaseService('professor')

        try:
            # 检查导师是否存在
            existing_professor = professor_db.professor_exists(tutor_id)

            if not existing_professor:
                # 若无该导师记录则创建新导师记录
                professor_db.create_professor(
                    tutor_id,
                    review_data['name'],
                    review_data['university'],
                    review_data['department']
                )

            # 存储review_sentence到review_sentences表
            professor_db.create_review_sentence(sentence_id, tutor_id, user_id, review_sentence)

            # 存储review_features到review_features表
            professor_db.create_review_features(feature_id, sentence_id, review_features)

            # 评价提交成功后写入导师基本信息URL链接
            if user_id == '管理员维护':
                url = review_data['professor_url']
            write_professor_info_url(tutor_id, url)

            return {"success": True, "message": "评价提交成功"}

        except Exception as e:
            return {"success": False, "message": f"数据库写入失败: {str(e)}"}

    @staticmethod
    def get_all_reviews():
        """
        获取所有导师评价信息
        """
        professor_db = DatabaseService('professor')
        try:
            # 获取所有评价语句及关联特征
            reviews = professor_db.execute_query('''
                    SELECT s.sentence_id, p.tutor_id, p.name, p.university, p.department, 
                           s.review_sentence, t.review_features, s.user_id
                    FROM review_sentences s
                    JOIN professor p ON s.tutor_id = p.tutor_id
                    LEFT JOIN review_features t ON s.sentence_id = t.sentence_id
                ''')

            # 定义字段索引映射
            FIELD_MAPPING = {
                'sentence_id': 0,
                'tutor_id': 1,
                'name': 2,
                'university': 3,
                'department': 4,
                'review_sentence': 5,
                'review_features': 6,
                'user_id': 7
            }

            return {
                "success": True,
                "data": [{
                    "sentence_id": row[FIELD_MAPPING['sentence_id']],
                    "tutor_id": row[FIELD_MAPPING['tutor_id']],
                    "name": row[FIELD_MAPPING['name']],
                    "university": row[FIELD_MAPPING['university']],
                    "department": row[FIELD_MAPPING['department']],
                    "review_sentence": row[FIELD_MAPPING['review_sentence']],
                    "review_features": row[FIELD_MAPPING['review_features']],
                    "user_id": row[FIELD_MAPPING['user_id']]
                } for row in reviews]
            }

        except Exception as e:
            return {"success": False, "message": f"获取失败: {str(e)}"}

    @staticmethod
    def delete_review(sentence_id):
        """
        删除评价语句
        """
        professor_db = DatabaseService('professor')
        try:
            professor_db.delete_review(sentence_id)
            return {"success": True}
        except Exception as e:
            return {"success": False, "message": f"删除失败: {str(e)}"}

    @staticmethod
    def toggle_review_permission(target_user_id: str, enable: str):
        """
        切换用户评价权限（管理员功能）
        :param target_user_id: 目标用户ID
        :param enable: True启用权限/False禁用权限
        """
        try:
            user_db = DatabaseService('user')

            # 更新用户权限状态
            user_db.update_review_permission(target_user_id, enable)

            return {"success": True, "message": f"已成功{'启用' if enable == 'True' else '禁用'}用户评价权限"}

        except Exception as e:
            return {"success": False, "message": f"权限更新失败: {str(e)}"}