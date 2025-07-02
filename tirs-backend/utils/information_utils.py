import json
import os
import tempfile
import shutil
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

    print(f"✅ 成功导出数据到: {output_file}")

    return result


def write_professor_info_url(tutor_id: str, url: str):
    """
    写入或更新导师基本信息URL链接

    规则:
    - 如果tutor_id不存在，则直接写入新记录（即使url为空）
    - 如果tutor_id存在且传入的url不为空字符串("")，则更新url
    - 如果tutor_id存在且传入的url为空字符串("")，则不执行操作

    参数:
        tutor_id (str): 导师的唯一标识符
        url (str): 导师信息的URL
    """
    output_file = Config.PROFESSOR_INFO_URLS_JSONL

    # 确保目录存在
    os.makedirs(os.path.dirname(output_file), exist_ok=True)

    # 准备要写入的数据
    new_data = {'tutor_id': tutor_id, 'url': url}

    # 如果文件不存在，直接写入
    if not os.path.exists(output_file):
        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(json.dumps(new_data, ensure_ascii=False) + '\n')
            print(f"文件创建成功: tutor_id={tutor_id}, url={url}")
            return
        except Exception as e:
            print(f"文件创建失败: {str(e)}")
            return

    # 读取现有数据
    records = []
    tutor_id_exists = False
    update_needed = False

    try:
        # 读取现有数据并检查tutor_id是否存在
        with open(output_file, 'r', encoding='utf-8') as f:
            for line in f:
                try:
                    record = json.loads(line)
                    # 检查是否找到匹配的tutor_id
                    if record.get('tutor_id') == tutor_id:
                        tutor_id_exists = True
                        # 如果传入的URL不为空，则更新记录
                        if url != "":
                            record['url'] = url
                            update_needed = True
                            print(f"更新URL: tutor_id={tutor_id}, 新url={url}")
                    records.append(record)
                except json.JSONDecodeError:
                    # 跳过无效行但保留它们
                    records.append({'raw_line': line.strip()})

        # 如果tutor_id不存在，添加新记录（无论URL是否为空）
        if not tutor_id_exists:
            records.append(new_data)
            print(f"添加新记录: tutor_id={tutor_id}, url={url}")

        # 使用临时文件安全写入（仅在需要更新时）
        if update_needed or not tutor_id_exists:
            temp_file = tempfile.NamedTemporaryFile(
                mode='w',
                encoding='utf-8',
                delete=False,
                dir=os.path.dirname(output_file)
            )

            with temp_file as tf:
                for record in records:
                    # 处理原始行数据
                    if 'raw_line' in record:
                        tf.write(record['raw_line'] + '\n')
                    else:
                        tf.write(json.dumps(record, ensure_ascii=False) + '\n')

            # 用临时文件替换原文件
            shutil.move(temp_file.name, output_file)

            # 根据操作类型输出结果
            if tutor_id_exists and update_needed:
                print(f"成功更新URL: tutor_id={tutor_id}, url={url}")
            elif not tutor_id_exists:
                print(f"成功添加新记录: tutor_id={tutor_id}, url={url}")
            return
        else:
            print(f"记录已存在且无需更新: tutor_id={tutor_id}")
            return

    except Exception as e:
        print(f"操作失败: {str(e)}")
        # 清理临时文件
        if 'temp_file' in locals() and os.path.exists(temp_file.name):
            os.remove(temp_file.name)
        return