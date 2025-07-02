本平台的核心功能是帮助用户根据自身的个性化需求选择心仪的导师，示例如下：
![image](https://github.com/user-attachments/assets/35d310e9-ffd9-4a11-b11a-791ff2dbae28)
![image](https://github.com/user-attachments/assets/97eecb8d-b70b-48db-838d-a69182579114)

此外，本平台还提供留下评价以及管理员操作等相关功能

### 项目结构
基于评价的导师智能推荐系统/
├── .git/                    # 版本控制
├── LICENSE.txt              # MIT 许可证
├── README.md                # 项目说明文档
│
├── tirs-backend/            # Flask 后端服务
│   ├── config.py            # 系统配置（NLP词典/数据库路径/密钥）
│   ├── main.py              # 服务启动入口
│   ├── requirements.txt     # Python 依赖清单
│   │
│   ├── server/              # 服务核心模块
│   │   ├── app.py           # Flask 应用初始化
│   │   └── handler/        # API 路由控制器
│   │       ├── auth_handler.py   # 认证相关接口
│   │       ├── user_handler.py   # 推荐/评价功能
│   │       └── admin_handler.py # 管理员功能
│   │
│   ├── service/            # 业务逻辑层
│   │   ├── database_service.py  # 多数据库操作
│   │   ├── nlp_service.py       # 自然语言处理
│   │   ├── recommendation_service.py # 推荐算法
│   │   └── review_service.py    # 评价管理
│   │
│   ├── utils/               # 工具类
│   │   ├── password_utils.py     # 密码加密
│   │   ├── status_monitor.py    # 系统监控
│   │   └── information_utils.py  # 数据导入导出
│   │
│   └── database/           # 数据存储
│       ├── professor_info_urls.jsonl  # 导师信息源
│       ├── supported_universities.json # 院校数据
│       ├── professor_db.sqlite  # 导师数据库
│       └── user_db.sqlite       # 用户数据库
│
└── tirs-fronted/            # React 前端工程
    ├── public/              # 静态资源
    │   ├── supported_universities.json # 院校数据
    │   └── images/         # 图片资源
    │
    ├── src/                # 前端源码
    │   ├── api/            # 接口封装
    │   │   ├── authApi.js       # 认证接口 
    │   │   ├── getcommendApi.js # 推荐接口
    │   │   └── reviewmanageApi.js # 评价管理
    │   │
    │   ├── components/     # 组件库
    │   │   ├── admin/       # 管理组件
    │   │   ├── auth/        # 认证组件  
    │   │   ├── user/        # 用户组件
    │   │   └── layout/      # 布局组件
    │   │
    │   ├── pages/          # 页面组件
    │   │   ├── AdminHomePage.jsx  # 管理后台
    │   │   ├── UserHomePage.jsx   # 用户主页
    │   │   └── SubmitReviewPage.jsx # 评价页
    │   │
    │   ├── context/        # 全局状态
    │   │   └── AuthContext.js # 认证上下文
    │   │
    │   ├── App.js          # 根组件
    │   └── index.js       # 入口文件
    │
    ├── tailwind.config.js  # Tailwind CSS 配置
    └── package.json        # 前端依赖配置

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
