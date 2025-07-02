from service.database_service import DatabaseService  # 导入数据库服务类

def get_all_professor_ids():
    """获取教授数据库所有导师ID"""
    ids = []
    professor_db = DatabaseService('professor')
    ids = [row[0] for row in professor_db.execute_query("SELECT tutor_id FROM professor")]
    return ids


if __name__ == "__main__":
    professor_ids = get_all_professor_ids()
    print(f"找到{len(professor_ids)}条导师数据：")
    for pid in professor_ids:
        print(f"- {pid}")