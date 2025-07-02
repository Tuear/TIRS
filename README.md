本平台的核心功能是帮助用户根据自身的个性化需求选择心仪的导师，示例如下：
![image](https://github.com/user-attachments/assets/35d310e9-ffd9-4a11-b11a-791ff2dbae28)
![image](https://github.com/user-attachments/assets/97eecb8d-b70b-48db-838d-a69182579114)

此外，本平台还提供留下评价以及管理员操作等相关功能

## 🚀 快速启动

### 环境要求
- Python 3.8+
- Node.js 16.14+
- npm 8.19+

### 后端启动
```bash
# 进入后端目录
cd tirs-backend

# 安装依赖
pip install -r requirements.txt

# 下载中文NLP模型
python -m spacy download zh_core_web_sm

# 启动后端服务
python main.py
```

### 前端启动
```bash
# 进入前端目录
cd tirs-fronted

# 安装依赖
npm install

# 启动前端服务
npm start
