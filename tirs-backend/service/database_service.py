import sqlite3
import json
from contextlib import closing
from config import Config
from utils.password_utils import hash_password  # 导入密码加密工具


# 多数据库服务类
class DatabaseService:
    def __init__(self, db_type):
        """
        根据类型创建数据库连接
        :param db_type: 'user'/'professor'/'review'
        """
        self.db_type = db_type  # 从参数获取数据库类型
        self.db_path = self._get_db_path()  # 获取数据库路径
        self._init_db()  # 初始化数据库

    def _get_db_path(self):
        """
        获取对应类型的数据库路径
        """
        paths = {
            'user': Config.USER_DB_PATH,
            'professor': Config.PROFESSOR_DB_PATH
        }
        return paths.get(self.db_type, Config.USER_DB_PATH)

    def _init_db(self):
        """
        初始化数据库表结构（设计文档2.4.2）
        """
        with closing(self._get_connection()) as conn:
            cursor = conn.cursor()

            # 用户数据库初始化
            if self.db_type == 'user':
                # 用户表
                cursor.execute('''
                CREATE TABLE IF NOT EXISTS user (
                    user_id TEXT PRIMARY KEY,
                    hashed_password TEXT NOT NULL,
                    role TEXT CHECK(role IN ('学生', '管理员')) DEFAULT '学生',
                    review_allowed TEXT DEFAULT 'True'
                )''')

                # 管理员表
                cursor.execute('''
                CREATE TABLE IF NOT EXISTS admin (
                    admin_id TEXT PRIMARY KEY,
                    admin_name TEXT NOT NULL,
                    password TEXT NOT NULL,
                    rights TEXT DEFAULT '普通管理员'
                )''')

                # 插入初始管理员账户
                # 账号：admin_super
                # 密码：admin123
                cursor.execute('''
                INSERT OR IGNORE INTO admin (admin_id, admin_name, password) 
                VALUES (?, ?, ?)
                ''', (
                    'admin_super',
                    '超级管理员',
                    hash_password('admin123')  # 需要从utils导入
                ))

            # 导师数据库初始化：从上到下依次为：主键、姓名、学校、学院
            elif self.db_type == 'professor':
                # 导师基本信息表
                cursor.execute('''
                CREATE TABLE IF NOT EXISTS professor (
                    tutor_id TEXT PRIMARY KEY,
                    name TEXT NOT NULL,
                    university TEXT,
                    department TEXT
                )''')

                # 导师评价语句表：从上到下依次为：主键、外键、评价语句、键值关联语句（关联导师）、键值关联语句（关联用户）
                cursor.execute('''
                CREATE TABLE IF NOT EXISTS review_sentences (
                    sentence_id TEXT PRIMARY KEY,
                    tutor_id TEXT NOT NULL,
                    review_sentence TEXT NOT NULL,
                    user_id TEXT NOT NULL,
                    FOREIGN KEY (tutor_id) REFERENCES professor(tutor_id),
                    FOREIGN KEY (user_id) REFERENCES user(user_id)
                )''')

                # 导师评价特征表：从上到下依次为：主键、外键、评价特征、键值关联语句（关联导师）
                cursor.execute('''
                CREATE TABLE IF NOT EXISTS review_features (
                    feature_id TEXT PRIMARY KEY,
                    sentence_id TEXT NOT NULL,
                    review_features TEXT NOT NULL,
                    FOREIGN KEY (sentence_id) REFERENCES review_sentences(sentence_id)
                )''')

            conn.commit()

    def _get_connection(self):
        """
        获取数据库连接
        """
        return sqlite3.connect(self.db_path)

    def execute_query(self, query: str, params: tuple = (), fetch_one: bool = False):
        """
        执行SQL语句（查找，更新，删除等），若为查询语句则返回查询结果
        :param query: SQL语句
        :param params: 参数元组
        :param fetch_one: 是否只获取一条记录
        :return: 若执行查询语句则返回查询结果（返回单挑或多条匹配记录）
        """
        with closing(self._get_connection()) as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            conn.commit()
            if fetch_one:
                return cursor.fetchone()
            return cursor.fetchall()

    def user_exists(self, user_id: str) -> bool:
        """
        检查用户是否存在（设计文档2.4.2）
        """
        result = self.execute_query(
            "SELECT 1 FROM user WHERE user_id = ?",
            (user_id,),
            fetch_one=True
        )
        return bool(result)

    def admin_exists(self, admin_id: str) -> bool:
        """
        检查管理员是否存在
        """
        result = self.execute_query(
            "SELECT 1 FROM admin WHERE admin_id = ?",
            (admin_id,),
            fetch_one=True
        )
        return bool(result)

    def create_user(self, user_id: str, hashed_password: str, role: str = '学生') -> None:
        """
        创建新用户
        """
        self.execute_query(
            "INSERT INTO user (user_id, hashed_password, role) VALUES (?, ?, ?)",
            (user_id, hashed_password, role)
        )

    def get_user(self, user_id: str) -> dict:
        """
        获取单个用户信息
        """
        try:
            result = self.execute_query(
                "SELECT * FROM user WHERE user_id = ?",
                (user_id,),
                fetch_one=True
            )
            if result:
                return {
                    'user_id': result[0],
                    'hashed_password': result[1],
                    'role': result[2],
                    'review_allowed': result[3]
                }
            return None

        except Exception as e:
            return {"success": False, "message": f"获取失败: {str(e)}"}

    def get_all_users(self) -> dict:
        """
        获取所有用户信息
        """
        try:
            # 获取所有用户信息
            users = self.execute_query('''
                SELECT user_id, role, review_allowed
                FROM user
            ''')
            # 定义字段索引映射
            FIELD_MAPPING = {
                'user_id': 0,
                'role': 1,
                'review_allowed': 2
            }

            return {
                "success": True,
                "data": [{
                    "user_id": row[FIELD_MAPPING['user_id']],
                    "role": row[FIELD_MAPPING['role']],
                    "review_allowed": row[FIELD_MAPPING['review_allowed']],
                } for row in users]
            }

        except Exception as e:
            return {"success": False, "message": f"获取失败: {str(e)}"}


    def get_admin(self, admin_id: str) -> dict:
        """
        获取管理员信息
        """
        result = self.execute_query(
            "SELECT * FROM admin WHERE admin_id = ?",
            (admin_id,),
            fetch_one=True
        )
        if result:
            return {
                'admin_id': result[0],
                'admin_name': result[1],
                'password': result[2],
                'rights': result[3]
            }
        return None

    def professor_exists(self, tutor_id: str) -> bool:
        """
        检查导师是否存在
        """
        result = self.execute_query(
            "SELECT 1 FROM professor WHERE tutor_id =?",
            (tutor_id,),
            fetch_one=True
        )
        return bool(result)

    def create_professor(self, tutor_id: str, name: str, university: str, department: str) -> None:
        """
        创建新导师记录
        """
        self.execute_query(
     """
            INSERT INTO professor 
            (tutor_id, name, university, department)
            VALUES (?, ?, ?, ?)
            """,
            (tutor_id, name, university, department)
        )

    def create_review_sentence(self, sentence_id: str, tutor_id: str, user_id: str, review_sentence: str) -> None:
        """
        创建评价语句记录
        """
        self.execute_query(
            """
            INSERT INTO review_sentences 
            (sentence_id, tutor_id, user_id, review_sentence)
            VALUES (?, ?, ?, ?)
            """,
            (sentence_id, tutor_id, user_id, review_sentence)
        )

    def create_review_features(self, feature_id: str, sentence_id: str, review_features: str) -> None:
        """
        创建评价特征记录
        """
        self.execute_query(
            """
            INSERT INTO review_features 
            (feature_id, sentence_id, review_features)
            VALUES (?, ?, ?)
            """,
            (feature_id, sentence_id, review_features)
        )

    def delete_review(self, sentence_id) -> None:
        """
        删除评价记录
        """
        # 删除评价语句记录
        self.execute_query(
            """DELETE FROM review_sentences WHERE sentence_id = ?""",
            (sentence_id,)
        )

        # 删除评价特征记录
        self.execute_query(
            """DELETE FROM review_features WHERE sentence_id =?""",
            (sentence_id,)
        )

    def update_review_permission(self,  target_user_id: str, enable: str) -> None:
        """
        更新用户评价权限
        """
        self.execute_query(
            """UPDATE user SET review_allowed = ? WHERE user_id = ?
                """,
            (enable, target_user_id)
        )