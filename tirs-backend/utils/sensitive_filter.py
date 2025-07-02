import re
from config import Config


class SensitiveFilter:
    @classmethod
    def check(cls, text):
        """
        检查用户评价文本是否包含敏感词（针对评价文本优化）

        参数:
            text (str): 用户输入的评价文本

        返回:
            bool: 如果包含敏感词返回True，否则返回False
        """
        if not text or not Config.SENSITIVE_WORDS:
            return False

        # 预处理文本：转换为小写并移除常见干扰字符
        clean_text = re.sub(r'[^\w\u4e00-\u9fff]', '', text.lower())

        # 检查敏感词
        for word in Config.SENSITIVE_WORDS:
            # 检查敏感词
            if word in clean_text:
                return True

        return False
