from flask import Flask, send_from_directory, jsonify
from flask_cors import CORS
from config import Config


# 导入API蓝图
from server.handler.auth_handler import auth_blue
from server.handler.user_handler import user_blue
from server.handler.admin_handler import admin_blue

# 注册Flask应用
app = Flask(__name__)
app.secret_key = Config.SECRET_KEY  # 配置session密钥


# 允许跨域请求
CORS(app)

# 注册API蓝图
app.register_blueprint(auth_blue)  # 注册认证功能API
app.register_blueprint(user_blue)  # 注册用户功能API
app.register_blueprint(admin_blue)  # 注册管理员功能API

