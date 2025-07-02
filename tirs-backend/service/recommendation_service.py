from service.nlp_service import nlp_processor
from service.database_service import DatabaseService
import hashlib
import random

# 推荐引擎类
class RecommendationService:
    @staticmethod
    def generate_professor_id(name, university, department):
        """
        使用 “姓名+学校+学院” 生成导师唯一ID (SHA256哈希值)
        """
        unique_string = f"{name}_{university}_{department}"
        return hashlib.sha256(unique_string.encode()).hexdigest()

    @staticmethod
    def parse_query(text):
        """
        解析用户查询（设计文档用例02）
        """
        # 调用NLP服务解析查询
        answer, success = nlp_processor.parse_query(text)
        # 失败返回错误信息
        if not success:
            return {"success": False, "message": answer}

        # 成功返回解析得到的特征
        else:
            return {"success": True, "message": answer}

    @staticmethod
    def get_professor_url(tutor_id):
        """根据导师ID获取信息URL"""
        import json
        import os
        from config import Config

        try:
            if not os.path.exists(Config.PROFESSOR_INFO_URLS_JSONL):
                return ""

            with open(Config.PROFESSOR_INFO_URLS_JSONL, 'r', encoding='utf-8') as f:
                for line in f:
                    try:
                        record = json.loads(line)
                        if record.get('tutor_id') == tutor_id:
                            return record.get('url', "")
                    except json.JSONDecodeError:
                        continue
            return ""
        except Exception as e:
            print(f"获取URL失败: {str(e)}")
            return ""

    @staticmethod
    def get_recommendations(text, university, department):
        """
        获取推荐结果（实现完整推荐逻辑）
        :param text: 用户查询文本
        :param university: 用户选择的学校
        :param department: 用户选择的学院
        """
        query_result = RecommendationService.parse_query(text)
        if not query_result["success"]:
            return {"success": False, "message": query_result["message"]}

        NLP_result = query_result["message"]
        print(f"用户输入语义解析结果为{NLP_result}")

        # 获取积极特征
        positive_features = query_result["message"]["positive"]
        academic_features = positive_features["academic"]
        personality_features = positive_features["personality"]

        # 合并"responsibility"和"人品"到性格特征
        combined_personality_features = personality_features

        # 获取所有符合条件的导师ID
        professor_db = DatabaseService('professor')
        if university == "全部" and department == "全部":
            tutor_ids = [row[0] for row in professor_db.execute_query(
                "SELECT tutor_id FROM professor"
            )]
        elif department == "全部":
            tutor_ids = [row[0] for row in professor_db.execute_query(
                "SELECT tutor_id FROM professor WHERE university = ?",
                (university,)
            )]
        else:
            tutor_ids = [row[0] for row in professor_db.execute_query(
                "SELECT tutor_id FROM professor WHERE university = ? AND department = ?",
                (university, department)
            )]

        tutor_scores = []
        for tutor_id in tutor_ids:
            # 获取导师信息和特征
            tutor_info = RecommendationService.show_professor_information(tutor_id)
            if not tutor_info["success"]:
                continue

            review_features = tutor_info["data"]["review_features"]
            tutor_academic_features = []
            tutor_personality_features = []
            for feature_str in review_features:
                parts = feature_str.split('|')
                for part in parts:
                    if part.startswith("学术特征:"):
                        tutor_academic_features.extend(part[5:].split("，"))
                    elif part.startswith("responsibility:") or part.startswith("人品:"):
                        tutor_personality_features.extend(part.split(":")[1].split("，"))

            # 计算学术特征匹配分数
            academic_matches = len(set(academic_features) & set(tutor_academic_features))
            print(f"学术特征匹配数量: {academic_matches}")

            # 计算性格特征匹配分数
            personality_matches = len(set(combined_personality_features) & set(tutor_personality_features))
            print(f"性格特征匹配数量: {personality_matches}")

            # 1. 计算学术匹配度百分比
            academic_match_percent = 0
            if academic_features:
                academic_match_percent = academic_matches / len(academic_features)

            # 2. 计算性格匹配度百分比
            personality_match_percent = 0
            if combined_personality_features:
                personality_match_percent = personality_matches / len(combined_personality_features)

            # 3. 计算总体匹配度加权平均值（学术50%，性格50%）
            total_match_percent = (academic_match_percent * 0.5) + (personality_match_percent * 0.5)

            # 4. 转换为80-100范围内的分数
            # 基础分80 + 匹配度贡献20（匹配度100%时得到20分）
            base_score = 85  # 提高基础分数
            match_bonus = 20 * total_match_percent
            total_score = base_score + match_bonus

            # 5. 确保分数在80-100之间
            total_score = min(max(total_score, 80), 100)

            # 6. 转换为整数百分比
            total_score = int(round(total_score))

            # 将分数添加到导师信息
            tutor_data = tutor_info["data"]
            tutor_data["match_score"] = total_score
            tutor_scores.append((tutor_data, total_score))

        # 按综合分数从高到低排序 - 确保使用正确的排序键
        tutor_scores.sort(key=lambda x: x[1], reverse=True)  # 按分数降序排序

        # 取前5个导师
        top_5_tutors = [tutor[0] for tutor in tutor_scores[:5]]

        # 处理最终结果
        processed_tutors = []
        for tutor in top_5_tutors:
            # 添加URL信息
            tutor_data = {
                "tutor_id": tutor["tutor_id"],
                "name": tutor["name"],
                "university": tutor["university"],
                "department": tutor["department"],
                "match_score": tutor["match_score"],
                "url": RecommendationService.get_professor_url(tutor["tutor_id"])
            }
            processed_tutors.append(tutor_data)

        return {"success": True, "message": processed_tutors}


    @staticmethod
    def show_professor_information(tutor_id):
        """
        信息展示(评价+基本信息) - 适配新表结构
        """
        professor_db = DatabaseService('professor')

        try:
            # 1. 查询导师基本信息
            basic_info = professor_db.execute_query(
                "SELECT tutor_id, name, university, department "
                "FROM professor WHERE tutor_id = ?",
                (tutor_id,),
                fetch_one=True
            )

            if not basic_info:
                return {"success": False, "message": "未找到该导师基本信息"}

            # 2. 查询导师的所有评价语句
            review_sentences = professor_db.execute_query(
                "SELECT s.review_sentence "
                "FROM review_sentences s "
                "WHERE s.tutor_id = ?",
                (tutor_id,),
            )

            # 3. 查询导师的所有评价特征（如果需要）
            review_features = professor_db.execute_query(
                "SELECT t.review_features "
                "FROM review_features t "
                "JOIN review_sentences s ON t.sentence_id = s.sentence_id "
                "WHERE s.tutor_id = ?",
                (tutor_id,),
            )

            # 3. 构造返回数据结构
            return {
                "success": True,
                "data": {
                    "tutor_id": basic_info[0],
                    "name": basic_info[1],
                    "university": basic_info[2],
                    "department": basic_info[3],
                    "review_sentences": [s[0] for s in review_sentences] if review_sentences else [],
                    "review_features": [f[0] for f in review_features] if review_features else []
                }
            }

        except Exception as e:
            return {"success": False, "message": f"查询失败: {str(e)}"}