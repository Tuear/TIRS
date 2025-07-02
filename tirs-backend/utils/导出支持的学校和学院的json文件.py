import json
import os
from collections import defaultdict
from service.database_service import DatabaseService
from config import Config


def export_universities_departments():
    """
    导出所有大学及其学院的JSON文件到指定绝对路径
    格式: {"大学名称": ["学院1", "学院2", ...], ...}
    """
    # 创建数据库服务实例（使用导师数据库）
    db_service = DatabaseService('professor')

    # 执行查询获取所有导师的信息
    print("正在查询数据库...")
    query = "SELECT DISTINCT university, department FROM professor"
    results = db_service.execute_query(query)
    print(f"查询到 {len(results)} 条记录")

    # 处理结果，构建大学-学院字典
    university_data = defaultdict(set)

    for row in results:
        university, department = row
        if university and department:
            # 清洗数据：去除空白
            university = university.strip()
            department = department.strip()

            # 添加到数据结构
            university_data[university].add(department)

    # 将set转换为list并排序
    result = {
        uni: sorted(list(depts))
        for uni, depts in university_data.items()
    }

    # 确保输出目录存在
    output_file = Config.SUPPORTED_UNIVERSITIES_JSON
    os.makedirs(os.path.dirname(output_file), exist_ok=True)

    # 生成JSON文件
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2, sort_keys=True)

    # 统计信息
    universities_count = len(result)
    departments_count = sum(len(depts) for depts in result.values())

    print(f"✅ 成功导出数据到: {output_file}")
    print(f"包含大学数量: {universities_count}")
    print(f"包含学院数量: {departments_count}")

    return result


if __name__ == "__main__":
    export_universities_departments()