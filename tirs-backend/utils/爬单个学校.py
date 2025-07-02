import requests
from bs4 import BeautifulSoup
import random
import hashlib
import time
import logging
import sys
from datetime import datetime
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import urllib3
from urllib.parse import urljoin

# 添加项目根目录到Python路径
sys.path.append('D:/syk/tirs-backend')

# 导入服务模块
from service.review_service import ReviewService

# 禁用SSL警告
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(f"tutor_crawler_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

# 只保留厦门大学
universities = [
    {
        "name": "厦门大学",
        "url": "https://archt.xmu.edu.cn/szdw/qysz.htm",
        "list_selector": ""
    }
]

# 院系列表
departments = ["建筑与土木工程学院"]  # 固定学院名称

# 用户ID池
USER_IDS = ["柒尾", "杨梅", "舒凡", "BR", "姚tt"]

# 设置请求头
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

# 特征列表 - 学术特征
academic_traits = [
    # 基础学术词汇
    "学术", "研究", "论文", "项目", "课题", "实验", "发表", "期刊", "会议", "专利",
    "算法", "模型", "数据", "分析", "理论", "方法", "创新", "成果", "领域", "方向",
    # 研究类型
    "基础研究", "应用研究", "理论研究", "实证研究", "定量研究", "定性研究", "交叉研究",
    # 研究资源
    "经费", "资源", "资金", "实验室", "设备", "数据库", "资料", "文献", "数据集", "计算资源",
    "财力", "资源支持", "经费支持", "经费充足", "经费保障", "资金支持", "资源提供", "资源利用", "资源利用效率",
    "财力雄厚", "资金支持", "资金保障", "资金支持力度", "资金支持力度高", "极速回复",
    # 研究产出
    "发表物", "出版物", "专著", "著作", "报告", "软著", "软件著作权", "技术方案", "解决方案",
    # 学术评价
    "影响因子", "引用", "索引", "顶刊", "顶会", "核心期刊", "SCI", "EI", "SSCI", "CSSCI",
    "高被引", "高影响力", "高水平", "优秀论文",
    # 学术活动
    "学术会议", "研讨会", "工作坊", "讲座", "报告会", "学术交流", "合作研究", "产学研", "校企合作",
    # 学科方向
    "人工智能", "机器学习", "深度学习", "自然语言处理", "计算机视觉", "大数据", "物联网", "区块链",
    "神经网络", "图像处理", "语音识别", "推荐系统", "数据挖掘", "知识图谱", "强化学习", "计算机图形学",
    "网络安全", "云计算", "边缘计算", "生物信息学", "计算生物学", "金融科技", "智慧医疗", "智能交通",
    "机器人", "自动化", "智能制造", "量子计算", "集成电路", "芯片设计",
    # 学术级别
    "国家级", "省级", "市级", "校级", "重点", "重大项目", "面上项目", "青年项目", "创新项目",
    # 学生相关
    "科研训练", "毕设", "毕业论文", "毕业设计", "大创", "创新创业", "科研竞赛", "科研项目", "科研经历",
    # 新增学术能力描述
    "科研能力突出", "学术视野开阔", "理论功底扎实", "实验设计精巧", "数据分析精准", "模型构建能力强",
    "创新思维活跃", "研究视角独特", "学术洞察敏锐", "跨学科融合能力强", "前沿领域深耕",
    "技术转化高效", "科研规划清晰", "研究进度把控好", "学术资源丰富", "国际合作广泛",
    # 新增学术资源描述
    "计算资源充足", "实验设备先进", "数据资源丰富", "学术交流机会多", "国际会议支持足",
    "科研经费充足", "研究团队强大", "学术网络广泛", "数据库访问权限全", "实验材料供应及时",
    # 新增学术态度描述
    "治学严谨", "科研态度端正", "学术诚信高", "追求卓越", "精益求精",
    "开放包容", "鼓励创新", "尊重多元观点", "批判思维培养", "学术热情高",
    # 新增短小口语化表达
    "点子多", "实验溜", "分析准", "模型强",
    "路子野", "眼光毒", "经费足", "装备顶", "数据库全",
    "报销快", "机会多", "资源多", "挂名爽", "大佬带",
    "改文细", "无私教", "文献透", "理论清", "课题多",
    "不差钱", "项目多", "顶会常", "高产王", "卷科研",
    "实验牛", "挖数据", "老司机", "经费足", "硬件好",
    "软件新", "数据足", "眼光准", "设备新", "批钱快",
    "材料足", "算力强", "指导细", "思路清", "一点通",
    "压力小", "节奏稳", "氛围好", "不骂人", "教得细",
    "入门易", "耐心足", "小白友", "零基础", "训练好",
    # 更短的两字表达
    "高产", "点子王", "实验狂", "分析神", "模型神",
    "经费多", "设备好", "报销爽", "挂名多", "带飞",
    "改文细", "教得好", "文献强", "理论神", "项目王",
    "顶会王", "卷王", "数据神", "司机稳", "硬件顶",
    "软件强", "数据多", "眼光毒", "批钱爽", "材料够",
    "算力足", "指导好", "思路好", "反应快", "压力小",
    "节奏好", "氛围棒", "不骂人", "教得透", "入门快",
    "耐心好", "小白好", "零门槛", "训练强", "毕设好",
    "大创全", "竞赛强", "资源多", "合作广", "结合紧",
    "自由高", "方向多", "选题活", "兴趣重",
    # 指导风格
    "悉心指导", "因材施教", "启发思维", "耐心解惑", "及时反馈",
    "定期沟通", "开放包容", "鼓励创新", "尊重自主", "培养独立",
    "论文精修", "实验陪跑", "代码分享", "课题共创", "署名公正",
    "一作支持", "协作共赢", "生涯规划", "资源倾斜", "成长赋能",
    # 团队建设
    "国际交流", "会议支持", "差旅保障", "团队和谐", "互助友爱",
    "跨校合作", "产业联动", "学术沙龙", "技能培训", "资源共享",
    "师兄帮带", "传承有序", "梯队完整", "新生关怀", "团建丰富",
    "零食自由", "导师请客", "节日福利", "健康关怀", "心理支持",
    # 学科热点
    "大模型前沿", "生成式AI", "量子计算", "脑机接口", "智慧医疗",
    "自动驾驶", "生物信息", "金融科技", "芯片设计", "网络安全",
    "元宇宙探索", "区块链+", "物联网+", "碳中和", "智慧城市",
    # 短词精选
    "顶会王", "高产帝", "点子王", "模型神", "分析准",
    "实验牛", "数据神", "理论深", "指导细", "资源皇",
    "设备壕", "报销光速", "署名公道", "推荐有力", "生涯导师",
    "国际视野", "跨域大牛", "创新引擎", "学术灯塔", "团队暖阳",
    # 研究资源
    "经费无忧", "资源充沛", "设备精良", "仪器尖端", "数据库海量",
    "移动工作站", "便携设备", "远程访问", "协同平台", "安全防护",
    "文献直通", "期刊订阅", "专利导航", "标准库全", "知识图谱",
    # 学术能力（60词）
    "领域开拓", "理论奠基", "方法革新", "技术创新", "算法突破",
    "模型精准", "实验精巧", "流程优化", "数据洞察", "分析透彻",
    "可视化优", "写作流畅", "演讲出众", "答辩从容", "评审权威",
    "引用领先", "成果转化", "应用落地", "产品孵化", "标准制定",
    "学科交叉", "跨界融合", "知识迁移", "前沿追踪", "趋势预判",
    "问题定位", "方案设计", "系统架构", "原型实现", "性能优化",
    "代码优雅", "框架清晰", "文档完备", "可复现强", "开源贡献",
    "专利布局", "软著高效", "技术壁垒", "成果保护", "产权管理",
    "项目申报", "标书精炼", "答辩出色", "结题优秀", "延续获批",
    "团队建设", "人才梯队", "国际合作", "产学联动", "平台搭建",
    "学术品牌", "声誉卓著", "奖项收割", "荣誉等身", "头衔丰富",

    # 基础学术词汇与研究类型
    "搞科研的", "做学问的", "写paper", "发文章", "做项目的", "搞课题的", "做实验的", "发paper", "投期刊", "赶会议",
    "申请专利", "设计算法", "建模型", "跑数据", "做分析", "玩理论的", "研究方法论", "搞创新的", "出成果的",
    "研究领域的", "方向选择", "纯理论探索", "偏应用开发的", "理论派研究", "实验验证型", "数据分析型", "访谈调查型",
    "跨学科融合",

    # 研究资源与经费
    "项目预算", "硬件软件资源", "科研资金", "实验场地", "仪器设备", "数据仓库", "参考资料", "文献库", "训练数据集",
    "GPU算力", "经济实力", "资源到位", "经费给力", "预算充足", "经费有保障", "资金到位", "设备管够", "资源共享",
    "高效利用设备", "财大气粗", "资金后盾强", "资金保障足", "资金倾斜多", "资金支持给劲儿", "资金紧张",

    # 学术评价体系
    "期刊影响力指数", "被引次数", "检索收录", "顶级期刊", "顶尖会议", "核心刊物", "SCI期刊", "EI索引", "社科核心",
    "中文核心", "热门论文", "高影响力研究", "高质量成果", "获奖论文",

    # 学术活动形式
    "学术年会", "专题研讨", "技能培训", "专家讲座", "成果汇报", "学术访问", "联合攻关", "产学研结合",
    "企业合作项目",

    # 热门学科方向
    "AI领域", "机器学习方向", "深度神经网络", "NLP方向", "CV视觉方向", "海量数据处理", "物联网技术", "区块链应用",
    "神经网络模型", "图像识别", "语音技术", "推荐算法", "大数据挖掘", "知识图谱构建", "强化学习算法",
    "计算机图形学", "信息安全", "云服务平台", "边缘计算设备", "生物信息分析", "计算生物模型", "金融科技产品",
    "智慧医疗系统", "智能交通方案", "机器人研发", "自动化控制", "智能工厂", "量子计算机", "芯片电路设计",
    "集成电路开发",

    # 项目级别
    "国家重点项目", "省部级课题", "市级课题", "校级课题", "重点攻关项目", "重大专项", "常规项目", "青年基金",
    "创新课题",

    # 学生科研活动
    "科研能力强", "学术视野开阔", "理论功底扎实", "实验设计精巧",
    "数据分析精准", "创新思维活跃", "研究视角独特", "前沿领域",
    "顶刊发文", "高水平论文", "研究资源丰富", "经费充足",
    "硬件设备好", "学术交流多", "产学研结合", "项目经验丰富",
    "科研训练系统", "课题前沿", "算法优化", "模型创新"
]

# 特征列表 - 责任特征
responsibility_traits = [
    # 基本性格特征
    "耐心", "严格", "轻松", "负责任", "友好", "压力大", "氛围", "团队", "指导", "沟通",
    "时间", "自由", "支持", "帮助", "经验", "开放", "鼓励", "要求", "关心", "交流", "佛系",
    # 指导风格
    "散养", "放养", "细致", "系统", "深入", "投入", "时间多", "极速回复", "定期会议", "随时沟通",
    "线上交流", "面对面", "活跃", "严肃", "和谐", "竞争", "合作", "宽松", "严谨", "灵活",
    "个性化", "定制化", "因材施教", "引导式", "启发式", "手把手", "细致入微",
    # 个人特质
    "年轻", "资深", "经验丰富", "有活力", "有耐心", "有责任心", "有热情", "有亲和力", "有领导力",
    "有创造力", "和蔼", "亲切", "严厉", "温和", "理性", "感性", "务实", "理想主义",
    "创新思维", "批判思维", "严谨思维", "逻辑性强", "幽默", "风趣", "平易近人", "高要求", "低要求",
    "不负责",
    # 学生支持
    "经费支持", "实习推荐", "就业帮助", "学术指导", "论文指导", "职业规划", "深造推荐", "出国推荐",
    "资源提供", "机会提供", "项目参与", "论文合作", "署名机会", "奖学金", "补助", "津贴",
    "心理支持", "情感支持", "生活关心", "职业发展", "人脉资源", "行业资源",
    # 团队文化
    "平等", "包容", "多元", "创新", "协作", "互助", "积极", "向上", "学习型", "研究型",
    "高效率", "快节奏", "慢节奏", "成果导向", "过程导向",
    # 新增责任心描述
    "主动关心学生", "及时解决问题", "承诺必兑现", "工作一丝不苟", "跟进学生进展",
    "考虑周到", "细节把控", "责任感强", "守时守信", "言出必行",
    "亲力亲为", "认真负责", "尽职尽责", "传递正能量", "榜样力量",
    "设身处地", "换位思考", "理解学生", "支持学生", "鼓励学生",
    # 耐心程度
    "不厌其烦", "百问不烦", "循循善诱", "循序渐进", "耐心讲解",
    "反复指导", "多次修改", "宽容错误", "允许试错", "鼓励探索",
    # 严格要求
    "高标准", "严要求", "追求完美", "精益求精", "一丝不苟",
    "不容马虎", "注重规范", "把控质量", "严格要求", "把关严格",
    # 关心学生
    "嘘寒问暖", "生活关怀", "身心健康", "情绪关注", "压力疏导",
    "困难帮扶", "节日问候", "生日祝福", "体贴入微", "关怀备至",
    # 团队管理
    "公平公正", "公开透明", "决策民主", "善于倾听", "广纳建议",
    "知人善任", "人尽其才", "分工明确", "协作高效", "氛围融洽"
]

# 特征列表 - 性格特征
character_traits = [
    # 性格描述
    "开朗", "外向", "内向", "沉稳", "活泼", "幽默", "乐观", "积极", "悲观", "消极",
    "严肃", "温和", "急躁", "冷静", "冲动", "理性", "感性", "随和", "固执", "倔强",
    "宽容", "大度", "小气", "计较", "坦诚", "直率", "含蓄", "委婉", "谦虚", "骄傲",
    "自信", "自卑", "谨慎", "大胆", "细心", "粗心", "耐心", "急躁", "热情", "冷淡",
    # 为人处世
    "真诚", "虚伪", "善良", "刻薄", "正直", "圆滑", "世故", "单纯", "成熟", "幼稚",
    "稳重", "轻浮", "可靠", "多变", "守信", "失信", "诚实", "狡诈", "厚道", "刻薄",
    # 工作态度
    "敬业", "懒散", "勤奋", "懈怠", "专注", "分心", "认真", "马虎", "负责", "敷衍",
    "主动", "被动", "进取", "保守", "创新", "守旧", "高效", "拖延", "务实", "务虚",
    # 情绪管理
    "平和", "暴躁", "温和", "易怒", "冷静", "情绪化", "稳定", "波动", "从容", "焦虑",
    # 价值观
    "正直", "功利", "淡泊", "名利", "奉献", "自私", "团队", "个人", "大局观", "本位",
    "长远眼光", "短视", "理想主义", "现实主义", "原则性强", "灵活变通",
    # 社交能力
    "善于沟通", "不善言辞", "人缘好", "孤僻", "亲和力", "距离感", "圆融", "棱角分明",
    "人脉广", "社交圈窄", "八面玲珑", "直来直去",
    # 领导风格
    "民主型", "专制型", "授权型", "控制型", "亲和型", "权威型", "变革型", "服务型",
    # 创新思维
    "思维活跃", "思维僵化", "创意无限", "墨守成规", "好奇心强", "缺乏兴趣", "想象力丰富", "思维局限",
    # 抗压能力
    "抗压强", "抗压弱", "越挫越勇", "容易放弃", "坚韧不拔", "脆弱敏感",
    # 其他特质
    "完美主义", "强迫症", "选择困难", "果断", "优柔寡断", "独立", "依赖", "冒险精神", "谨慎保守"
]


def create_session():
    """创建带有重试机制的会话"""
    session = requests.Session()
    retry_strategy = Retry(
        total=3,
        backoff_factor=1,
        status_forcelist=[429, 500, 502, 503, 504],
        allowed_methods=["GET"]
    )
    adapter = HTTPAdapter(max_retries=retry_strategy)
    session.mount("http://", adapter)
    session.mount("https://", adapter)
    return session


def generate_reviews_for_tutor(tutor_info):
    """为单个导师生成1-5条评价数据"""
    reviews = []
    # 随机生成1-5条评价
    num_reviews = random.randint(1, 5)

    for _ in range(num_reviews):
        try:
            # 对于每条评价，每个特征部分随机抽取1或2个特征
            num_academic = random.choice([1, 2])
            num_responsibility = random.choice([1, 2])
            num_character = random.choice([1, 2])

            # 从特征列表中随机抽取指定数量的特征
            academic_features = random.sample(academic_traits, num_academic)
            responsibility_features = random.sample(responsibility_traits, num_responsibility)
            character_features = random.sample(character_traits, num_character)

            # 组合成评价
            review = {
                "name": tutor_info['name'],
                "university": tutor_info['university'],
                "department": tutor_info['department'],
                "academic": ", ".join(academic_features),
                "responsibility": ", ".join(responsibility_features),
                "character": ", ".join(character_features),
                "user_id": random.choice(USER_IDS),
                "position": tutor_info.get('position', ''),
                "research": tutor_info.get('research', ''),
                "url": tutor_info.get('url', '')
            }
            reviews.append(review)
        except Exception as e:
            logger.error(f"生成单条评价失败: {str(e)}")
            continue

    return reviews


def generate_tutor_id(name, university, department):
    """生成唯一导师ID"""
    try:
        identifier = f"{name}_{university}_{department}"
        return f"tutor_{hashlib.sha256(identifier.encode()).hexdigest()[:16]}"
    except Exception as e:
        logger.error(f"生成导师ID失败: {str(e)}")
        return f"tutor_{random.getrandbits(64):016x}"


def submit_to_database(review_data):
    """提交评价数据到数据库"""
    try:
        # 生成导师ID
        tutor_id = generate_tutor_id(
            review_data['name'],
            review_data['university'],
            review_data['department']
        )

        # 准备提交数据
        review_payload = {
            'name': review_data['name'],
            'university': review_data['university'],
            'department': review_data['department'],
            'academic': review_data['academic'],
            'responsibility': review_data['responsibility'],
            'character': review_data['character'],
            'tutor_id': tutor_id,
            'position': review_data.get('position', ''),
            'research': review_data.get('research', ''),
            'url': review_data.get('url', '')
        }

        # 提交评价
        user_id = review_data['user_id']
        result = ReviewService.submit_review(review_payload, user_id)

        if result.get('success'):
            logger.info(f"✅ 提交成功: {review_data['name']} - {review_data['university']}")
        else:
            logger.error(f"❌ 提交失败: {review_data['name']} - {result.get('message', '未知错误')}")

        return result
    except Exception as e:
        logger.error(f"提交评价到数据库时出错: {str(e)}")
        return {"success": False, "message": str(e)}


def parse_xmu_tutors(soup, base_url):
    """解析厦门大学导师页面"""
    tutor_list = []
    # 查找所有职称分类（教授、副教授等）
    zc_divs = soup.find_all('div', class_='zc')
    for zc_div in zc_divs:
        # 获取职称（如：教授、副教授）
        position = zc_div.text.strip()
        # 找到下一个兄弟节点（包含导师信息的div）
        next_div = zc_div.find_next_sibling('div', class_='clear')
        if next_div:
            # 找到包含导师信息的row div
            row_div = next_div.find_next_sibling('div', class_='row')
            if row_div:
                # 在row div中找到所有导师信息的div
                tutor_divs = row_div.find_all('div', class_='pic-item')
                for tutor_div in tutor_divs:
                    # 获取导师姓名
                    name_tag = tutor_div.find('div', class_='pic-item-title').find('a')
                    name = name_tag.text.strip()
                    # 获取导师个人主页链接
                    url = name_tag.get('href')
                    if url and not url.startswith('http'):
                        url = urljoin(base_url, url)

                    # 将导师信息添加到列表
                    tutor_list.append({
                        'name': name,
                        'position': position,  # 使用职称作为职位信息
                        'url': url,
                        'university': "厦门大学",
                        'department': "建筑与土木工程学院",
                        'research': ''  # 研究方向留空
                    })
    return tutor_list


def get_tutor_info_from_web(url, university_name):
    """获取导师信息（厦门大学）"""
    session = create_session()
    try:
        response = session.get(url, headers=HEADERS, verify=False, timeout=10)
        response.encoding = 'utf-8'
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            # 根据大学名称调用不同的解析函数
            if university_name == "厦门大学":
                return parse_xmu_tutors(soup, url)
            else:
                logger.error(f"未知大学名称: {university_name}")
                return []
        else:
            logger.error(f"请求失败: {url}, 状态码: {response.status_code}")
            return []
    except Exception as e:
        logger.error(f"请求异常: {url}, 错误: {str(e)}")
        return []


def main():
    """主函数"""
    logger.info("开始导师信息爬取和评价生成")
    all_tutors = []

    # 爬取导师信息
    for uni in universities:
        try:
            logger.info(f"爬取 {uni['name']} 导师信息...")
            tutors = get_tutor_info_from_web(uni['url'], uni['name'])

            if tutors:
                sample_names = [t['name'] for t in tutors[:3]]
                logger.info(f"提取到的导师: {', '.join(sample_names)}{'...' if len(tutors) > 3 else ''}")
                all_tutors.extend(tutors)
                logger.info(f"√ 成功爬取 {len(tutors)} 位导师")
            else:
                logger.warning(f"★ 未找到 {uni['name']} 的导师信息")

            time.sleep(1)  # 请求间隔

        except Exception as e:
            logger.error(f"爬取 {uni['name']} 失败: {str(e)}")

    # 生成评价并提交到数据库
    logger.info(f"爬取完成！共获取 {len(all_tutors)} 位导师信息")
    successful_reviews = 0
    failed_reviews = 0

    # 为每位导师生成1-5条评价
    for tutor in all_tutors:
        reviews = generate_reviews_for_tutor(tutor)
        if not reviews:
            logger.warning(f"导师 {tutor['name']} 没有生成任何评价")
            failed_reviews += 1
            continue

        for review in reviews:
            result = submit_to_database(review)
            if result.get('success'):
                successful_reviews += 1
            else:
                failed_reviews += 1

    logger.info(f"所有评价生成完成！成功: {successful_reviews}, 失败: {failed_reviews}")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        logger.info("程序被用户中断")
    except Exception as e:
        logger.critical(f"程序崩溃: {str(e)}\n{traceback.format_exc()}")