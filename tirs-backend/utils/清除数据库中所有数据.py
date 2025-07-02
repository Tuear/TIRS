import sqlite3
from config import Config


def clear_professor_database():
    """
    完全清除教授数据库中的所有数据，但保留表和数据库文件
    （相当于将数据库重置为初始空白状态）
    """
    try:
        db_path = Config.PROFESSOR_DB_PATH
        print(f"目标数据库路径: {db_path}")

        # 连接到数据库
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()

            # 禁用外键约束（允许按任意顺序删除数据）
            cursor.execute("PRAGMA foreign_keys = OFF")

            # 获取所有用户表（排除系统表）
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'")
            tables = [row[0] for row in cursor.fetchall()]

            if not tables:
                print("数据库中没有用户表，可能是新数据库")
                return

            print(f"找到的表: {', '.join(tables)}")

            # 清空所有表数据
            for table in tables:
                cursor.execute(f"DELETE FROM {table}")
                print(f"已清空表: {table} (删除了 {cursor.rowcount} 行数据)")

            # 重置自增计数器（仅在表存在时执行）
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='sqlite_sequence'")
            if cursor.fetchone():
                cursor.execute("DELETE FROM sqlite_sequence")

            # 启用外键约束
            cursor.execute("PRAGMA foreign_keys = ON")

            conn.commit()  # 先提交事务
            print("数据库已成功清空，所有表数据已删除")

            # 清理数据库文件空间（必须在事务外执行）
            cursor.execute("VACUUM")

            # 验证清空结果
            for table in tables:
                cursor.execute(f"SELECT COUNT(*) FROM {table}")
                count = cursor.fetchone()[0]
                print(f"表 '{table}' 现在有 {count} 行数据")

    except Exception as e:
        print(f"清空数据库失败: {str(e)}")
        raise RuntimeError(f"清空数据库失败: {str(e)}")


if __name__ == "__main__":
    print("!!! 警告: 此操作将永久删除教授数据库中的所有数据 !!!")
    print("数据库文件将保留，但所有表将被清空")
    print("这是不可逆操作，请确保您已了解后果")

    confirm = input("确定要清空教授数据库吗? (输入 '清空' 确认): ")

    if confirm == "清空":
        clear_professor_database()
        print("操作完成")
    else:
        print("操作已取消")