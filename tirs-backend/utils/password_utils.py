import bcrypt
from config import Config


# 密码工具类
def hash_password(password: str) -> str:
    """
    使用bcrypt加密密码（设计文档2.4.2）
    """
    salt = bcrypt.gensalt(rounds=Config.BCRYPT_LOG_ROUNDS)
    return bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')


def verify_password(password: str, hashed: str) -> bool:
    """
    验证密码与哈希是否匹配（密码是否正确）
    """
    return bcrypt.checkpw(
        password.encode('utf-8'),
        hashed.encode('utf-8')
    )
