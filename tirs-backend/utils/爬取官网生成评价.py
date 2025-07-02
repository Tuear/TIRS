import requests
from bs4 import BeautifulSoup
import random
import hashlib
import time
from urllib.parse import urljoin
import re
import logging
import traceback
import sys
from datetime import datetime
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import urllib3

# 禁用SSL警告
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# 添加项目根目录到Python路径
sys.path.append('D:/syk/tirs-backend')

# 导入服务模块
from service.database_service import DatabaseService
from service.review_service import ReviewService

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

# 用户ID池
USER_IDS = ["柒尾", "杨梅", "舒凡", "BR", "姚tt"]

# 扩展大学列表（114所）
universities = [
    # {"name": "中国科学技术大学", "url": "https://cs.ustc.edu.cn/js_23235/list.htm", "list_selector": ".teachers-list .teacher-item"},
    # {"name": "北京大学", "url": "https://cs.pku.edu.cn/szdw/jyxl/amz/ALL.htm", "list_selector": ".faculty-item"},
    # {"name": "清华大学", "url": "https://www.cs.tsinghua.edu.cn/szdw/jzgml.htm", "list_selector": ".teacher-list li"},
    # {"name": "复旦大学", "url": "https://cs.fudan.edu.cn/24269/list.htm", "list_selector": ".teacher-item"},
    # {"name": "上海交通大学", "url": "https://www.cs.sjtu.edu.cn/Faculty.aspx", "list_selector": ".teacher-item"},
    # {"name": "浙江大学", "url": "https://person.zju.edu.cn/csen", "list_selector": ""},
    # {"name": "南京大学", "url": "https://cs.nju.edu.cn/1651/listm.htm", "list_selector": ".teacher-list li"},
    # {"name": "中国科学技术大学", "url": "https://cs.ustc.edu.cn/js_23235/listm.htm", "list_selector": ".teachers-list .teacher-item"},
    # {"name": "哈尔滨工业大学", "url": "https://www.icourses.cn/web/sword/portal/teacherTeam?courseId=6011", "list_selector": ".teacher-list li"},
    # {"name": "西安交通大学", "url": "http://www.cs.xjtu.edu.cn/szdw/jsml/jsjqt.htm", "list_selector": ".teacher-list li"},
    # {"name": "中国人民大学", "url": "https://gsai.ruc.edu.cn/szdw/szml.htm", "list_selector": ".teacher-list li"},
    # {"name": "北京航空航天大学", "url": "https://scse.buaa.edu.cn/szdw/jsml.htm", "list_selector": ".teacher-list li"},
    # {"name": "北京师范大学", "url": "https://ai.bnu.edu.cn/szdw/szll/jsml.htm", "list_selector": ".teacher-list li"},
    # {"name": "南开大学", "url": "https://cs.nankai.edu.cn/teachers", "list_selector": ".teacher-list li"},
    # {"name": "天津大学", "url": "https://cs.tju.edu.cn/faculty/list.htm", "list_selector": ".teacher-item"},
    # {"name": "中山大学", "url": "https://cse.sysu.edu.cn/teachers", "list_selector": ".teacher-list li"},
    # {"name": "山东大学", "url": "https://cs.sdu.edu.cn/teachers", "list_selector": ".teacher-item"},
    # {"name": "华中科技大学", "url": "https://cs.hust.edu.cn/szdw/jsml.htm", "list_selector": ".teachers-list li"},
    # {"name": "吉林大学", "url": "https://cs.jlu.edu.cn/teachers", "list_selector": ".teacher-list li"},
    # {"name": "厦门大学", "url": "https://cs.xmu.edu.cn/szdw/list.htm", "list_selector": ".teacher-item"},
    # {"name": "武汉大学", "url": "https://cs.whu.edu.cn/szdw/szll.htm", "list_selector": ".teacher-item"},
    # {"name": "东南大学", "url": "https://cse.seu.edu.cn/szdw/list.htm", "list_selector": ".teacher_list li"},
    # {"name": "中南大学", "url": "https://cse.csust.edu.cn/szdw/jsml.htm", "list_selector": ".teacher-list li"},
    # {"name": "大连理工大学", "url": "https://cs.dlut.edu.cn/faculty/list.htm", "list_selector": ".teacher-list li"},
    # {"name": "西北工业大学", "url": "https://cs.nwpu.edu.cn/faculty/list.htm", "list_selector": ".teacher-item"},
    # {"name": "同济大学", "url": "https://cs.tongji.edu.cn/szdw/list.htm", "list_selector": ".teacher-box"},
    # {"name": "华南理工大学", "url": "https://cs.scut.edu.cn/szdw/jsml.htm", "list_selector": ".teacher-item"},
    # {"name": "重庆大学", "url": "https://cs.cqu.edu.cn/szdw/jsml.htm", "list_selector": ".teacher-item"},
    # {"name": "兰州大学", "url": "https://cs.lzu.edu.cn/teachers", "list_selector": ".teacher-list li"},
    # {"name": "华东师范大学", "url": "https://cs.ecnu.edu.cn/szdw/list.htm", "list_selector": ".teacher-item"},
    # {"name": "中国农业大学", "url": "https://cs.cau.edu.cn/szdw/jsml.htm", "list_selector": ".teacher-item"},
    # {"name": "电子科技大学", "url": "https://www.cs.uestc.edu.cn/faculty/list.htm", "list_selector": ".teacher-item"},
    # {"name": "中央民族大学", "url": "https://cs.muc.edu.cn/szdw/jsml.htm", "list_selector": ".teacher-list li"},
    # {"name": "西北农林科技大学", "url": "https://cs.nwsuaf.edu.cn/szdw/jsml.htm", "list_selector": ".teacher-item"},
    # {"name": "四川大学", "url": "https://cs.scu.edu.cn/szdw/jsml.htm", "list_selector": ".teacher-item"},
    # {"name": "湖南大学", "url": "https://cs.hnu.edu.cn/szdw/jsml.htm", "list_selector": ".teacher-list li"},
    # {"name": "东北大学", "url": "https://cs.neu.edu.cn/faculty/list.htm", "list_selector": ".teacher-item"},
    # {"name": "中国海洋大学", "url": "https://cs.ouc.edu.cn/szdw/jsml.htm", "list_selector": ".teacher-list li"},
    # {"name": "北京理工大学", "url": "https://cs.bit.edu.cn/szdw/jsml.htm", "list_selector": ".teacher-list li"},
    # {"name": "北京交通大学", "url": "https://cs.bjtu.edu.cn/szdw/jsml.htm", "list_selector": ".teacher-item"},
    # {"name": "北京工业大学", "url": "https://cs.bjut.edu.cn/szdw/jsml.htm", "list_selector": ".teacher-list li"},
    # {"name": "北京科技大学", "url": "https://cs.ustb.edu.cn/szdw/jsml.htm", "list_selector": ".teacher-item"},
    # {"name": "北京化工大学", "url": "https://cs.buct.edu.cn/szdw/jsml.htm", "list_selector": ".teacher-list li"},
    # {"name": "北京邮电大学", "url": "https://cs.bupt.edu.cn/szdw/jsml.htm", "list_selector": ".teacher-item"},
    # {"name": "北京林业大学", "url": "https://cs.bjfu.edu.cn/szdw/jsml.htm", "list_selector": ".teacher-list li"},
    # {"name": "北京中医药大学", "url": "https://cs.bucm.edu.cn/szdw/jsml.htm", "list_selector": ".teacher-item"},
    # {"name": "北京外国语大学", "url": "https://cs.bfsu.edu.cn/szdw/jsml.htm", "list_selector": ".teacher-list li"},
    # {"name": "中国传媒大学", "url": "https://cs.cuc.edu.cn/szdw/jsml.htm", "list_selector": ".teacher-item"},
    # {"name": "对外经济贸易大学", "url": "https://cs.uibe.edu.cn/szdw/jsml.htm", "list_selector": ".teacher-list li"},
    # {"name": "中央音乐学院", "url": "https://cs.ccom.edu.cn/szdw/jsml.htm", "list_selector": ".teacher-item"},
    # {"name": "中国政法大学", "url": "https://cs.cupl.edu.cn/szdw/jsml.htm", "list_selector": ".teacher-list li"},
    # {"name": "华北电力大学", "url": "https://cs.ncepu.edu.cn/szdw/jsml.htm", "list_selector": ".teacher-item"},
    # {"name": "中国石油大学（北京）", "url": "https://cs.cup.edu.cn/szdw/jsml.htm", "list_selector": ".teacher-list li"},
    # {"name": "中国地质大学（北京）", "url": "https://cs.cugb.edu.cn/szdw/jsml.htm", "list_selector": ".teacher-item"},
    # {"name": "天津医科大学", "url": "https://cs.tmu.edu.cn/szdw/jsml.htm", "list_selector": ".teacher-list li"},
    # {"name": "河北工业大学", "url": "https://cs.hebut.edu.cn/szdw/jsml.htm", "list_selector": ".teacher-item"},
    # {"name": "太原理工大学", "url": "https://cs.tyut.edu.cn/szdw/jsml.htm", "list_selector": ".teacher-list li"},
    # {"name": "内蒙古大学", "url": "https://cs.imu.edu.cn/szdw/jsml.htm", "list_selector": ".teacher-item"},
    # {"name": "辽宁大学", "url": "https://cs.lnu.edu.cn/szdw/jsml.htm", "list_selector": ".teacher-list li"},
    # {"name": "大连海事大学", "url": "https://cs.dlmu.edu.cn/szdw/jsml.htm", "list_selector": ".teacher-item"},
    # {"name": "延边大学", "url": "https://cs.ybu.edu.cn/szdw/jsml.htm", "list_selector": ".teacher-list li"},
    # {"name": "东北师范大学", "url": "https://cs.nenu.edu.cn/szdw/jsml.htm", "list_selector": ".teacher-item"},
    # {"name": "哈尔滨工程大学", "url": "https://cs.hrbeu.edu.cn/szdw/jsml.htm", "list_selector": ".teacher-item"},
    # {"name": "东北农业大学", "url": "https://cs.neau.edu.cn/szdw/jsml.htm", "list_selector": ".teacher-list li"},
    # {"name": "东北林业大学", "url": "https://cs.nefu.edu.cn/szdw/jsml.htm", "list_selector": ".teacher-item"},
    # {"name": "华东理工大学", "url": "https://cs.ecust.edu.cn/szdw/jsml.htm", "list_selector": ".teacher-list li"},
    # {"name": "东华大学", "url": "https://cs.dhu.edu.cn/szdw/jsml.htm", "list_selector": ".teacher-item"},
    # {"name": "上海大学", "url": "https://cs.shu.edu.cn/szdw/jsml.htm", "list_selector": ".teacher-list li"},
    # {"name": "上海外国语大学", "url": "https://cs.shisu.edu.cn/szdw/jsml.htm", "list_selector": ".teacher-item"},
    # {"name": "苏州大学", "url": "https://cs.suda.edu.cn/szdw/jsml.htm", "list_selector": ".teacher-item"},
    # {"name": "南京航空航天大学", "url": "https://cs.nuaa.edu.cn/szdw/jsml.htm", "list_selector": ".teacher-item"},
    # {"name": "南京理工大学", "url": "https://cs.njust.edu.cn/szdw/jsml.htm", "list_selector": ".teacher-list li"},
    # {"name": "中国矿业大学", "url": "https://cs.cumt.edu.cn/szdw/jsml.htm", "list_selector": ".teacher-item"},
    # {"name": "河海大学", "url": "https://cs.hhu.edu.cn/szdw/jsml.htm", "list_selector": ".teacher-list li"},
    # {"name": "江南大学", "url": "https://cs.jiangnan.edu.cn/szdw/jsml.htm", "list_selector": ".teacher-item"},
    # {"name": "南京农业大学", "url": "https://cs.njau.edu.cn/szdw/jsml.htm", "list_selector": ".teacher-list li"},
    # {"name": "中国药科大学", "url": "https://cs.cpu.edu.cn/szdw/jsml.htm", "list_selector": ".teacher-list li"},
    # {"name": "安徽大学", "url": "https://cs.ahu.edu.cn/szdw/jsml.htm", "list_selector": ".teacher-item"},
    # {"name": "合肥工业大学", "url": "https://cs.hfut.edu.cn/szdw/jsml.htm", "list_selector": ".teacher-list li"},
    # {"name": "福州大学", "url": "https://cs.fzu.edu.cn/szdw/jsml.htm", "list_selector": ".teacher-item"},
    # {"name": "南昌大学", "url": "https://cs.ncu.edu.cn/szdw/jsml.htm", "list_selector": ".teacher-list li"},
    # {"name": "郑州大学", "url": "https://cs.zzu.edu.cn/szdw/jsml.htm", "list_selector": ".teacher-item"},
    # {"name": "武汉理工大学", "url": "https://cs.whut.edu.cn/szdw/jsml.htm", "list_selector": ".teacher-list li"},
    # {"name": "华中农业大学", "url": "https://cs.hzau.edu.cn/szdw/jsml.htm", "list_selector": ".teacher-item"},
    # {"name": "华中师范大学", "url": "https://cs.ccnu.edu.cn/szdw/jsml.htm", "list_selector": ".teacher-list li"},
    # {"name": "中南财经政法大学", "url": "https://cs.zuel.edu.cn/szdw/jsml.htm", "list_selector": ".teacher-item"},
    # {"name": "湖南师范大学", "url": "https://cs.hunnu.edu.cn/szdw/jsml.htm", "list_selector": ".teacher-list li"},
    # {"name": "暨南大学", "url": "https://cs.jnu.edu.cn/szdw/jsml.htm", "list_selector": ".teacher-item"},
    # {"name": "华南师范大学", "url": "https://cs.scnu.edu.cn/szdw/jsml.htm", "list_selector": ".teacher-list li"},
    # {"name": "广西大学", "url": "https://cs.gxu.edu.cn/szdw/jsml.htm", "list_selector": ".teacher-item"},
    # {"name": "海南大学", "url": "https://cs.hainanu.edu.cn/szdw/jsml.htm", "list_selector": ".teacher-list li"},
    # {"name": "西南交通大学", "url": "https://cs.swjtu.edu.cn/szdw/jsml.htm", "list_selector": ".teacher-item"},
    # {"name": "西南石油大学", "url": "https://cs.swpu.edu.cn/szdw/jsml.htm", "list_selector": ".teacher-list li"},
    # {"name": "四川农业大学", "url": "https://cs.sicau.edu.cn/szdw/jsml.htm", "list_selector": ".teacher-item"},
    # {"name": "西南大学", "url": "https://cs.swu.edu.cn/szdw/jsml.htm", "list_selector": ".teacher-list li"},
    # {"name": "西南财经大学", "url": "https://cs.swufe.edu.cn/szdw/jsml.htm", "list_selector": ".teacher-item"},
    # {"name": "贵州大学", "url": "https://cs.gzu.edu.cn/szdw/jsml.htm", "list_selector": ".teacher-list li"},
    # {"name": "云南大学", "url": "https://cs.ynu.edu.cn/szdw/jsml.htm", "list_selector": ".teacher-item"},
    # {"name": "西藏大学", "url": "https://cs.utibet.edu.cn/szdw/jsml.htm", "list_selector": ".teacher-list li"},
    # {"name": "西北大学", "url": "https://cs.nwu.edu.cn/szdw/jsml.htm", "list_selector": ".teacher-item"},
    # {"name": "西安电子科技大学", "url": "https://cs.xidian.edu.cn/szdw/jsml.htm", "list_selector": ".teacher-list li"},
    # {"name": "长安大学", "url": "https://cs.chd.edu.cn/szdw/jsml.htm", "list_selector": ".teacher-item"},
    # {"name": "陕西师范大学", "url": "https://cs.snnu.edu.cn/szdw/jsml.htm", "list_selector": ".teacher-list li"},
    # {"name": "广州大学", "url": "https://wyy.gzhu.edu.cn/szdw/shuo_shi_shen.htm", "list_selector": ".teacher-item"},
    # {"name": "青海大学", "url": "https://cs.qhu.edu.cn/szdw/jsml.htm", "list_selector": ".teacher-list li"},
    # {"name": "宁夏大学", "url": "https://cs.nxu.edu.cn/szdw/jsml.htm", "list_selector": ".teacher-item"},
    # {"name": "新疆大学", "url": "https://cs.xju.edu.cn/szdw/jsml.htm", "list_selector": ".teacher-list li"},
    # {"name": "石河子大学", "url": "https://cs.shzu.edu.cn/szdw/jsml.htm", "list_selector": ".teacher-item"},
    # {"name": "首都医科大学", "url": "https://cs.ccmu.edu.cn/szdw/jsml.htm", "list_selector": ".teacher-list li"},
    # {"name": "南方医科大学", "url": "https://cs.smu.edu.cn/szdw/jsml.htm", "list_selector": ".teacher-item"},
    # {"name": "中国科学院大学", "url": "https://cs.ucas.ac.cn/szdw/jsml.htm", "list_selector": ".teacher-list li"},
    # {"name": "中国社会科学院大学", "url": "https://cs.ucass.edu.cn/szdw/jsml.htm", "list_selector": ".teacher-item"},
    # {"name": "江苏大学", "url": "https://cs.ujs.edu.cn/szdw/jsml.htm", "list_selector": ".teacher-list li"},
    # {"name": "南京医科大学", "url": "https://cs.njmu.edu.cn/szdw/jsml.htm", "list_selector": ".teacher-item"},
    # {"name": "浙江工业大学", "url": "https://cs.zjut.edu.cn/szdw/jsml.htm", "list_selector": ".teacher-list li"},
    # {"name": "杭州电子科技大学", "url": "https://cs.hdu.edu.cn/szdw/jsml.htm", "list_selector": ".teacher-item"},
    # {"name": "上海理工大学", "url": "https://cs.usst.edu.cn/szdw/jsml.htm", "list_selector": ".teacher-list li"},
    # {"name": "燕山大学", "url": "https://cs.ysu.edu.cn/szdw/jsml.htm", "list_selector": ".teacher-item"},
    # {"name": "山西大学", "url": "https://cs.sxu.edu.cn/szdw/jsml.htm", "list_selector": ".teacher-list li"},
    # {"name": "河南大学", "url": "https://cs.henu.edu.cn/szdw/jsml.htm", "list_selector": ".teacher-item"},
    # {"name": "宁波大学", "url": "https://cs.nbu.edu.cn/szdw/jsml.htm", "list_selector": ".teacher-list li"},
    # {"name": "扬州大学", "url": "https://cs.yzu.edu.cn/szdw/jsml.htm", "list_selector": ".teacher-item"},
    # {"name": "湘潭大学", "url": "https://cs.xtu.edu.cn/szdw/jsml.htm", "list_selector": ".teacher-list li"},
    # {"name": "深圳大学", "url": "https://cs.szu.edu.cn/szdw/jsml.htm", "list_selector": ".teacher-item"},
    # {"name": "华南农业大学", "url": "https://cs.scau.edu.cn/szdw/jsml.htm", "list_selector": ".teacher-list li"},
    # {"name": "福建师范大学", "url": "https://cs.fjnu.edu.cn/szdw/jsml.htm", "list_selector": ".teacher-item"},
    # {"name": "上海师范大学", "url": "https://cs.shnu.edu.cn/szdw/jsml.htm", "list_selector": ".teacher-list li"},
    # {"name": "首都师范大学", "url": "https://cs.cnu.edu.cn/szdw/jsml.htm", "list_selector": ".teacher-item"},
    # {"name": "北京语言大学", "url": "https://cs.blcu.edu.cn/szdw/jsml.htm", "list_selector": ".teacher-list li"},
    # {"name": "国际关系学院", "url": "https://cs.uir.edu.cn/szdw/jsml.htm", "list_selector": ".teacher-item"},
    # {"name": "西南政法大学", "url": "https://cs.swupl.edu.cn/szdw/jsml.htm", "list_selector": ".teacher-list li"},
    # {"name": "东北财经大学", "url": "https://cs.dufe.edu.cn/szdw/jsml.htm", "list_selector": ".teacher-item"},
    # {"name": "江西财经大学", "url": "https://cs.jxufe.edu.cn/szdw/jsml.htm", "list_selector": ".teacher-list li"},
    # {"name": "南京邮电大学", "url": "https://cs.njupt.edu.cn/szdw/jsml.htm", "list_selector": ".teacher-item"},
    # {"name": "重庆邮电大学", "url": "https://cs.cqupt.edu.cn/szdw/jsml.htm", "list_selector": ".teacher-list li"},
    # {"name": "长沙理工大学", "url": "https://cs.csust.edu.cn/szdw/jsml.htm", "list_selector": ".teacher-item"},
    # {"name": "昆明理工大学", "url": "https://cs.kmust.edu.cn/szdw/jsml.htm", "list_selector": ".teacher-list li"},
    # {"name": "上海中医药大学", "url": "https://cs.shutcm.edu.cn/szdw/jsml.htm", "list_selector": ".teacher-item"},
]

# 院系列表
departments = [
    "计算机科学与技术学院", "电子工程学院", "机械工程学院",
    "材料科学与工程学院", "经济管理学院", "医学院",
    "人工智能学院", "软件学院", "网络空间安全学院",
    "数据科学学院", "自动化学院", "信息工程学院"
]

# 特征列表
academic_traits = [
            # 基础学术词汇
        "学术", "研究", "论文", "项目", "课题", "实验", "发表", "期刊", "会议", "专利",
        "算法", "模型", "数据", "分析", "理论", "方法", "创新", "成果", "领域", "方向",
        # 研究类型
        "基础研究", "应用研究", "理论研究", "实证研究", "定量研究", "定性研究", "交叉研究",
        # 研究资源
        "经费", "资源", "资金", "实验室", "设备", "数据库", "资料", "文献", "数据集", "计算资源",
        "财力", "资源支持", "经费支持", "经费充足", "经费保障", "资金支持", "资源提供", "资源利用", "资源利用效率",
        "财力雄厚", "资金支持", "资金保障", "资金支持力度", "资金支持力度高", "资金支持力度低",
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

        #基础学术词汇与研究类型
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

responsibility_traits = [
        # 基本性格特征
        "耐心", "严格", "轻松", "负责任", "友好", "压力大", "氛围", "团队", "指导", "沟通",
        "时间", "自由", "支持", "帮助", "经验", "开放", "鼓励", "要求", "关心", "交流", "佛系",
        # 指导风格
        "散养", "放养", "细致", "系统", "深入", "投入", "时间多", "时间少", "定期会议", "随时沟通",
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
        "心理支持", "情感支持", "生活关心", "职业发展", "人脉资源", "行业资源","对学生好","对学生要求高",
        # 团队文化
        "平等", "包容", "多元", "创新", "协作", "互助", "积极", "向上", "学习型", "研究型",
        "高效率", "快节奏", "慢节奏", "成果导向", "过程导向",
        # 新增责任心描述
        "主动关心学生", "及时解决问题", "承诺必兑现", "工作一丝不苟", "跟进学生进展",
        "保护学生权益", "维护学术诚信", "尊重学生时间", "危机处理能力强", "支持学生决定",
        # 新增人品特征描述
        "待人真诚", "处事公正", "尊重差异", "富有同理心", "谦虚低调",
        "乐于分享", "信守承诺", "保护隐私", "尊重学生选择", "学术道德高尚",
        # 新增指导风格描述
        "个性化指导", "启发式教学", "鼓励独立思考", "培养自主能力", "提供发展空间",
        "目标导向明确", "反馈具体实用", "鼓励团队协作", "培养领导能力", "注重实践应用",
        # 新增学生支持描述
        "职业发展指导", "实习推荐积极", "就业资源丰富", "深造支持有力", "心理支持到位",
        "生活关怀细致", "困难时期陪伴", "资源分配合理", "机会提供公平", "人脉资源分享",
        # 新增沟通风格描述
        "沟通高效直接", "倾听耐心细致", "表达清晰明确", "反馈建设性强", "讨论氛围开放",
        "尊重不同意见", "批评方式得当", "鼓励自由表达", "定期一对一交流", "线上线下结合",
        # 新增团队氛围描述
        "团队凝聚力强", "互助氛围浓厚", "学术氛围自由", "创新氛围浓厚", "竞争氛围健康",
        "跨学科交流多", "师生关系平等", "经验传承良好", "新成员融入快", "成果共享公平",
        "人超好", "脾气好", "没架子", "像朋友", "能扛事",
        "护学生", "不压榨", "不抢功", "不画饼", "说到做",
        "好商量", "接地气", "回复快", "不拖堂", "反馈快",
        "不消失", "放养型", "管得松", "不压力", "心态好",
        "开玩笑", "请客多", "福利多", "关心人", "帮解决",
        "帮找对象", "氛围好", "师兄好", "师弟好", "像家庭",
        "不抢一作", "署名公", "推荐强", "帮工作", "实习强",
        "熬夜陪", "不骂人", "不甩锅", "不施压", "真帮忙",
        # 品格特质
        "治学严谨", "待人真诚", "尊重包容", "公正无私", "谦逊有礼",
        "耐心细致", "热情洋溢", "乐观积极", "同理心强", "责任心重",
        "信守承诺", "师德高尚", "保护学生", "鼓励探索", "支持自主",
        # 指导方式
        "循循善诱", "手把手教", "启发引导", "因势利导", "个性化培养",
        "目标明确", "节奏合理", "张弛有度", "沟通顺畅", "反馈及时",
        "会议高效", "尊重时间", "周末免扰", "假期自由", "灵活管理",
        "信任授权", "培养领导力", "激发潜能", "成长型思维",
        # 团队文化
        "平等开放", "互帮互助", "创新包容", "温暖如家", "积极向上",
        "快乐科研", "协作高效", "成果共享", "经验传承", "多元融合",
        "跨学科交流", "国际互动", "业界联动", "师生融洽", "尊师爱生",
        # 短词精选
        "人超好", "没架子", "像朋友", "护学生", "不压榨",
        "真帮忙", "好商量", "接地气", "回复快", "反馈光速",
        "关怀暖", "支持强", "推荐牛", "资源神", "业界通",
        "学术父", "团队母", "生涯师", "成长伴", "指路灯",
        # 品格修养（60词）
        "德高望重", "虚怀若谷", "光明磊落", "言行一致", "表里如一",
        "宽厚仁爱", "古道热肠", "雪中送炭", "成人之美", "甘为人梯",
        "谦谦君子", "温润如玉", "彬彬有礼", "不矜不伐", "低调务实",
        "诚实守信", "一诺千金", "守时如金", "言出必行", "使命必达",
        "公正廉明", "一视同仁", "利益回避", "程序正义", "规则至上",
        "学术纯粹", "求真务实", "专注执着", "精益求精", "止于至善",
        "开放包容", "尊重多元", "求同存异", "兼容并蓄", "海纳百川",
        "乐观向上", "积极进取", "永不言弃", "逆商卓越", "抗压强韧",
        "情绪稳定", "心态平和", "处变不惊", "化险为夷", "定力非凡",
        # 指导艺术（50词）
        "慧眼识珠", "因势利导", "循序渐进", "张弛有度", "宽严相济",
        "鼓励探索", "包容试错", "启发思考", "激发潜能", "唤醒内驱",
        "授人以渔", "思维锻造", "方法论授", "认知升级", "视野开拓",
        "及时反馈", "精准点拨", "一针见血", "对症下药", "醍醐灌顶",
        "换位思考", "将心比心", "倾听共情", "理解尊重", "平等对话",
        "灵活变通", "因地制宜", "个性定制", "因材施教", "量体裁衣",
        "信任授权", "大胆放手", "关键把控", "保驾护航", "全程守护",
        "教学相长", "亦师亦友", "共同成长", "成就彼此", "互相照亮",
]

character_traits = [
        #基本性格特征与指导风格
        "特别有耐心", "脾气很好", "不急不躁", "要求挺严格的", "比较较真", "规矩比较多", "氛围比较轻松", "不会太紧张",
        "挺随和的", "超级负责任", "做事很靠谱", "交给ta很放心", "人很友好", "很好相处", "没什么架子", "感觉压力有点大",
        "节奏比较紧张", "挺push的", "整个氛围很好", "氛围比较严肃", "氛围挺自由的", "团队感很强", "团队合作挺好的",
        "团队人不多但很精", "指导得很到位", "给的建议很中肯", "很会带学生", "沟通起来很顺畅", "有什么说什么",
        "交流很直接", "时间安排挺紧的", "时间上比较自由", "时间观念很强", "自由度很高", "不太管细节", "主要靠自己发挥",
        "非常支持学生", "有求必应（在合理范围内）", "是学生的后盾", "很乐意帮助学生", "有问题找ta准没错", "帮人很热心",
        "经验非常丰富", "老江湖了", "懂得很多", "思想很开放", "接受新事物", "愿意听不同声音", "经常鼓励学生",
        "多表扬少批评", "很会激励人", "要求比较高", "要求比较明确", "没什么硬性要求", "很关心学生", "交流起来很舒服",
        "交流没啥障碍", "交流不多但很有效", "比较佛系", "不怎么催", "顺其自然", "基本放养", "自己摸索", "导师管得少",
        "指导特别细致", "连标点符号都管", "抠细节", "指导很系统", "有章法", "一步步来", "研究做得很深入", "要求深挖",
        "不浮于表面", "对指导学生很投入", "花很多精力", "导师时间比较多", "能经常讨论", "导师比较忙",
        "能分给学生的时间有限", "有固定的组会，每周一次", "有事随时可以找", "微信/电话基本都回",
        "主要通过微信/邮件/线上会议交流", "更喜欢当面讨论", "经常约办公室聊", "组里气氛很活跃", "大家爱讨论",
        "组会/讨论比较严肃", "不太开玩笑", "组里关系很和谐", "没啥矛盾", "组里有点竞争氛围", "大家暗自较劲", "鼓励合作",
        "经常一起做项目", "管理比较宽松", "deadline可以商量", "治学非常严谨", "要求一丝不苟", "方式比较灵活",
        "看情况调整", "会根据每个人的特点定制培养方案", "很懂学生", "知道怎么教不同的人", "主要是引导你思考",
        "不给现成答案", "擅长启发", "能点醒你", "初期会手把手教", "带着做", "关注到每一个小点", "指导无微不至",

        #个人特质
        "导师比较年轻", "思想前卫", "没什么代沟", "导师是大牛", "在领域里很有名", "经验老丰富了", "啥都见过",
        "精力充沛", "充满干劲", "非常有耐心", "不厌其烦", "责任心爆棚", "对学生很上心", "对科研充满热情",
        "很有感染力", "很有亲和力", "让人想亲近", "很有领导魅力", "能服众", "想法天马行空", "很有创意",
        "为人特别和蔼可亲", "像长辈一样", "要求严厉", "批评起来不留情面", "性格温和", "说话轻声细语", "非常理性",
        "讲逻辑不讲情面", "比较感性", "注重感受和人情", "很务实", "看重实际产出和结果", "有点理想主义", "追求完美",
        "思维很创新", "总想打破常规", "善于批判性思考", "爱质疑", "思维极其严谨", "逻辑严密", "逻辑超强", "条理清晰",
        "说话很幽默风趣", "组会不无聊", "一点架子都没有", "很好说话", "对学生要求很高", "期望值大", "要求不高",
        "能毕业就行", "有点不负责任", "不太管学生",

        #学生支持
        "经费比较充足", "出差开会报销爽快", "会帮忙推荐实习", "人脉广", "很关心学生就业", "会帮忙内推",
        "学术上指导很给力", "能学到真东西", "改论文很认真", "能提升很多", "会和你聊职业规划", "给建议", "想读博的话",
        "推荐信", "支持出国交流", "帮忙联系，写推荐信", "能提供各种资源",
        "经常给学生创造机会", "鼓励甚至要求参与项目", "锻炼人", "有机会和导师合作发论文", "只要贡献够",
        "署名比较公平", "给的补助挺不错", "比较慷慨", "会关心学生心理状态", "压力大时能聊聊", "像朋友一样",
        "给予情感支持", "不仅关心学习", "也关心生活状况", "很注重学生长远的职业发展", "导师人脉很广", "能介绍不少牛人",
        "和业界联系紧密", "有行业资源", "对学生是真的好", "处处为学生着想", "对学生要求很高", "期望也高",

        #团队文化
        "组里很平等", "学生敢和导师争论", "氛围很包容", "允许犯错", "尊重多样性", "组员背景多元", "想法也多元",
        "鼓励创新", "不怕试错", "特别强调协作", "互帮互助", "师兄师姐很热心", "乐于助人", "大家都很积极向上",
        "充满正能量", "整体是积极进取的状态", "组里学习氛围浓", "经常分享", "专注研究", "学术氛围浓厚", "做事效率很高",
        "不拖沓", "节奏很快", "项目一个接一个", "节奏比较慢", "可以慢慢琢磨", "非常看重最终成果/产出", "更看重研究过程中的学习和成长",
        "耐心指导", "认真负责", "及时回复", "定期会议",
        "关心学生", "支持发展", "就业帮助", "实习推荐",
        "资源提供", "论文指导", "职业规划", "学术支持",
        "心理关怀", "生活关心", "团队建设", "氛围和谐",
        "要求合理", "时间自由", "鼓励创新", "因材施教",
        "人品好", "和蔼可亲", "平易近人", "尊重学生",
        "公平公正", "信守承诺", "乐于助人", "待人真诚",
        "亲和力强", "幽默风趣", "团队合作", "包容多元",
        "不抢功劳", "保护学生", "不压榨", "关心成长",
        "热心肠", "责任心强", "学术道德高", "生活简朴"
]
# 设置请求头
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
}

# 无效名称关键词列表（严格过滤）
INVALID_NAME_KEYWORDS = [
    "提示", "访问", "找不到", "404", "错误", "网站", "链接", "地址",
    "科研", "平台", "成果", "师生", "出访", "国际", "会议", "政策",
    "查询", "学生", "工作", "博士后", "招募", "关工委", "简介", "实验室",
    "学院", "学校", "大学", "系", "专业", "团队", "课题组", "教授组",
    "概况", "新闻", "公告", "通知", "下载", "文件", "资料", "系统", "首页",
    "登录", "注册", "管理", "后台", "友情链接", "版权所有", "地址", "电话",
    # 新增无效关键词
    "下一页", "更多", "学生工作", "联系我们", "关于我们", "首页", "导航", "帮助",
    "搜索", "设为首页", "加入收藏", "版权", "邮箱", "电话", "传真", "地图",
    "招生", "就业", "校友", "捐赠", "招聘", "新闻动态", "学术活动", "专题",
    "更多>>", "更多>", "更多", ">>", ">", "【", "】", "（", "）", "《", "》"
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


def get_tutor_info_from_web(url, university_name, list_selector=""):
    """从大学官网获取导师信息（多重策略）"""
    try:
        logger.info(f"正在爬取 [{university_name}] : {url}")

        session = create_session()

        # 发送请求
        response = session.get(
            url,
            headers=HEADERS,
            timeout=30,
            verify=False  # 忽略SSL证书验证
        )

        if response.status_code != 200:
            logger.warning(f"访问失败，状态码: {response.status_code}")
            return []

        # 检测编码
        response.encoding = response.apparent_encoding or 'utf-8'

        # 解析HTML或JSON
        if "api" in url:  # 处理API接口
            tutor_list = parse_api_response(response.json(), university_name)
            if tutor_list:
                logger.info(f"从API接口提取到 {len(tutor_list)} 位导师")
                return tutor_list
        else:  # 处理HTML页面
            soup = BeautifulSoup(response.text, 'html.parser')

            # 策略1: 尝试使用预定义的选择器
            if list_selector:
                tutor_list = extract_with_custom_selector(soup, list_selector, url, university_name)
                if tutor_list:
                    logger.info(f"使用自定义选择器提取到 {len(tutor_list)} 位导师")
                    return tutor_list

            # 策略2: 尝试结构化提取
            tutor_list = extract_tutors_from_html(soup, url, university_name)
            if tutor_list:
                logger.info(f"成功提取 {len(tutor_list)} 位导师")
                return tutor_list

            # 策略3: 尝试备用方法
            logger.info("结构化提取失败，尝试备用方法")
            tutor_list = extract_with_backup_method(soup, url, university_name)

            if tutor_list:
                logger.info(f"从备用方法提取到 {len(tutor_list)} 位导师")
                return tutor_list

        logger.warning(f"★ 未找到 {university_name} 的导师信息")
        return []

    except Exception as e:
        logger.error(f"获取导师信息出错: {str(e)}\n{traceback.format_exc()}")
        return []


def parse_api_response(data, university_name):
    """解析API返回的JSON数据（针对浙江大学）"""
    tutor_list = []
    if not isinstance(data, dict) or "data" not in data:
        return []

    for item in data.get("data", []):
        try:
            name = item.get("fullName", "")
            position = item.get("title", "")
            research = item.get("directions", "")
            link = f"https://person.zju.edu.cn/#/people/{item.get('id', '')}"

            if not is_valid_name(name):
                logger.debug(f"过滤无效姓名: {name}")
                continue

            tutor_info = {
                'name': name,
                'position': position,
                'research': research,
                'url': link,
                'university': university_name
            }
            tutor_list.append(tutor_info)
        except Exception as e:
            logger.debug(f"处理API数据出错: {str(e)}")
            continue

    return tutor_list


def extract_with_custom_selector(soup, selector, base_url, university_name):
    """使用预定义的选择器提取导师信息"""
    tutor_list = []
    try:
        items = soup.select(selector)
        if not items:
            return []

        logger.info(f"使用自定义选择器找到 {len(items)} 个元素")

        for item in items:
            try:
                # 尝试提取姓名
                name_element = item.select_one('.name, h3, h4, .teacher-name, .faculty-name, .person-name')
                if not name_element:
                    name_element = item.find(['h3', 'h4', 'h2'])
                name = name_element.get_text(strip=True) if name_element else "未知"

                # 过滤无效名称
                if not is_valid_name(name):
                    logger.debug(f"过滤无效姓名: {name}")
                    continue

                # 尝试提取职位
                position_element = item.select_one('.position, .title, .job-title, .faculty-title')
                position = position_element.get_text(strip=True)[:30] if position_element else ""

                # 尝试提取研究方向
                research_element = item.select_one('.research, .field, .direction')
                research = research_element.get_text(strip=True)[:100] if research_element else ""

                # 尝试提取详情页链接
                link_element = item.find('a', href=True)
                link = link_element['href'] if link_element and 'href' in link_element.attrs else ""
                if link and not link.startswith('http'):
                    link = urljoin(base_url, link)

                tutor_info = {
                    'name': name,
                    'position': position,
                    'research': research,
                    'url': link,
                    'university': university_name
                }
                tutor_list.append(tutor_info)

            except Exception as e:
                logger.debug(f"处理元素出错: {str(e)}")
                continue

    except Exception as e:
        logger.error(f"自定义选择器提取出错: {str(e)}")

    return tutor_list


def extract_tutors_from_html(soup, base_url, university_name):
    """从HTML结构中提取导师信息（改进版）"""
    tutor_list = []

    # 常见的选择器模式（按优先级排序）
    selectors = [
        '.teacher-item',  # 华中科技大学
        '.teacher_list li',  # 东南大学
        '.teacher-item',  # 复旦大学
        '.teacher-item',  # 中国科学技术大学
        '.teacher-list li',  # 哈尔滨工业大学
        '.faculty-item',  # 浙江大学
        '.teachers-container .teacher',
        '.faculty-container',
        '.teacher-box',
        '.staff-item',
        '.teacher-info',
        '.view-content .views-row',
        'table.teacher-table tbody tr',
        '.teacher',
        '.faculty-member',
        '.person-card',
        '.teacher-list > div',
        '.teacher-list > li',
        '.faculty-list > li',
        '.teachers-list li',
        '.faculty-list .faculty-member'
    ]

    for selector in selectors:
        try:
            tutors = soup.select(selector)
            if tutors:
                logger.info(f"尝试HTML选择器: '{selector}' 找到 {len(tutors)} 个元素")

                for tutor in tutors:
                    try:
                        name = "未知"
                        position = ""
                        research = ""
                        link = ""

                        # 1. 尝试获取姓名
                        name_selectors = ['.name', 'h3', 'h4', 'h2', '.title', '.teacher-name', '.name a', 'strong',
                                          'a > h3', '.faculty-name']
                        for ns in name_selectors:
                            name_element = tutor.select_one(ns)
                            if name_element:
                                name_text = name_element.get_text(strip=True)
                                if is_valid_name(name_text):
                                    name = name_text
                                    break

                        # 跳过无效名称
                        if name == "未知":
                            continue

                        # 2. 获取职位
                        position_selectors = ['.position', '.title', '.job-title', '.zhicheng', '.professor-title',
                                              'p.position']
                        for ps in position_selectors:
                            position_element = tutor.select_one(ps)
                            if position_element:
                                position = position_element.get_text(strip=True)[:30]
                                break

                        # 3. 获取研究方向
                        research_selectors = ['.research', '.field', '.direction', '.yanjiu', '.research-field',
                                              'p.research']
                        for rs in research_selectors:
                            research_element = tutor.select_one(rs)
                            if research_element:
                                research = research_element.get_text(strip=True)[:100]
                                break

                        # 4. 获取详情页链接
                        link_element = tutor.find('a', href=True)
                        if link_element and link_element.get('href'):
                            link = link_element['href']
                            if not link.startswith('http'):
                                link = urljoin(base_url, link)

                        tutor_info = {
                            'name': name,
                            'position': position,
                            'research': research,
                            'url': link,
                            'university': university_name
                        }

                        tutor_list.append(tutor_info)

                    except Exception as e:
                        logger.debug(f"解析单个导师出错: {str(e)}")
                        continue

                if tutor_list:
                    logger.info(f"使用选择器 '{selector}' 成功提取 {len(tutor_list)} 位导师")
                    break

        except Exception as e:
            logger.debug(f"HTML选择器 '{selector}' 出错: {str(e)}")
            continue

    return tutor_list


def extract_with_backup_method(soup, base_url, university_name):
    """备份提取方法（优化版）- 只提取链接中的姓名"""
    tutor_list = []

    # 查找可能的导师列表区域
    possible_sections = soup.find_all(['div', 'section', 'article', 'main'],
                                      class_=re.compile(r'(teacher|faculty|staff|member|person|team)', re.I))
    if not possible_sections:
        possible_sections = [soup.find('body')]

    # 处理每个可能区域
    for section in possible_sections:
        # 只提取<a>标签中的中文姓名（2-4个字符）
        name_elements = section.find_all('a', string=re.compile(r'[\u4e00-\u9fa5]{2,4}'))

        for element in name_elements:
            try:
                name = element.get_text(strip=True)
                logger.debug(f"备用方法找到姓名: {name}")

                # 过滤无效名称
                if not is_valid_name(name):
                    logger.debug(f"过滤无效姓名: {name}")
                    continue

                # 尝试获取职位和研究方向
                position = ""
                research = ""
                link = element.get('href', '')
                if link and not link.startswith('http'):
                    link = urljoin(base_url, link)

                # 向上查找包含更多信息的父容器
                container = element.find_parent(['div', 'li', 'tr', 'section', 'td', 'article'])
                if not container:
                    container = element.parent

                # 尝试提取职位
                position_elements = container.find_all(['p', 'div', 'span', 'td'],
                                                       string=re.compile(r'(教授|副教授|讲师|研究员|工程师|导师|博导)',
                                                                         re.I))
                if position_elements:
                    position = position_elements[0].get_text(strip=True)[:30]
                else:
                    # 尝试在链接文本前后提取职位
                    container_text = container.get_text()
                    position_match = re.search(r'[\u4e00-\u9fa5]{2,6}(教授|副教授|讲师|研究员|工程师|导师|博导)',
                                               container_text)
                    if position_match:
                        position = position_match.group(0)

                # 尝试提取研究方向
                research_elements = container.find_all(['p', 'div', 'span', 'td'],
                                                       string=re.compile(r'(研究|方向|领域|兴趣)', re.I))
                if research_elements:
                    # 尝试获取相邻的文本
                    next_sibling = research_elements[0].find_next_sibling()
                    if next_sibling:
                        research = next_sibling.get_text(strip=True)[:100]
                    else:
                        research = research_elements[0].get_text(strip=True)[:100]

                # 创建导师信息字典
                tutor_info = {
                    'name': name,
                    'position': position,
                    'research': research,
                    'url': link,
                    'university': university_name
                }

                tutor_list.append(tutor_info)
                logger.debug(f"提取导师: {name} - {position} - {research}")

            except Exception as e:
                logger.debug(f"处理元素出错: {str(e)}")
                continue

    # 过滤重复姓名
    unique_tutors = []
    seen_names = set()
    for tutor in tutor_list:
        if tutor['name'] not in seen_names:
            unique_tutors.append(tutor)
            seen_names.add(tutor['name'])

    return unique_tutors


def is_valid_name(name):
    """
    检查是否为有效的导师姓名（严格条件）
    :param name: 待检查的姓名
    :return: 如果是有效姓名返回True，否则False
    """
    # 检查长度
    if not name or len(name) < 2 or len(name) > 5:
        return False

    # 检查是否包含无效关键词
    for keyword in INVALID_NAME_KEYWORDS:
        if keyword in name:
            return False

    # 检查是否包含数字、英文字母或特殊符号（除中文和职称后缀外）
    if re.search(r'[0-9a-zA-Z]', name):
        return False

    # 检查是否为纯中文（允许职称后缀）
    chinese_count = sum(1 for char in name if '\u4e00' <= char <= '\u9fff')
    if chinese_count < 2:
        return False

    # 特殊过滤条件（排除常见无效名称）
    if re.search(r'科研|工作|会议|查询|平台|成果|学生|招生|招聘', name):
        return False

    # 允许职称后缀（教授、副教授等）
    if re.search(r'教授|副教授|讲师|研究员|工程师|导师|博导', name):
        # 确保名字部分至少两个中文字符
        name_part = re.split(r'教授|副教授|讲师|研究员|工程师|导师|博导', name)[0]
        return len(name_part) >= 2

    return True


def generate_review_for_tutor(tutor_info):
    """为单个导师生成评价数据"""
    try:
        # 随机选择特征数量（1或2个）
        num_features = random.choice([1, 2])

        # 随机选择特征（每个特征列表独立随机选择1或2个）
        academic_features = random.sample(academic_traits, num_features)
        responsibility_features = random.sample(responsibility_traits, num_features)
        character_features = random.sample(character_traits, num_features)

        return {
            "name": tutor_info['name'],
            "university": tutor_info['university'],
            "department": random.choice(departments),
            "academic": ", ".join(academic_features),
            "responsibility": ", ".join(responsibility_features),
            "character": ", ".join(character_features),
            "user_id": random.choice(USER_IDS),
            "position": tutor_info.get('position', ''),
            "research": tutor_info.get('research', ''),
            "url": tutor_info.get('url', '')
        }
    except Exception as e:
        logger.error(f"生成评价失败: {str(e)}")
        return None

def generate_tutor_id(name, university, department):
    """生成唯一导师ID"""
    try:
        identifier = f"{name}_{university}_{department}"
        return f"tutor_{hashlib.sha256(identifier.encode()).hexdigest()}"
    except Exception as e:
        logger.error(f"生成导师ID失败: {str(e)}")
        return f"tutor_{random.getrandbits(128):032x}"  # 备用ID生成


def main():
    logger.info("开始导师信息爬取和评价生成")

    all_tutors = []
    success_count = 0
    failed_count = 0

    # 爬取各大学的导师信息
    for uni in universities:
        try:
            logger.info(f"爬取 {uni['name']} 导师信息...")

            # 提取自定义选择器
            custom_selector = uni.get("list_selector", "")

            tutors = get_tutor_info_from_web(uni['url'], uni['name'], list_selector=custom_selector)

            if not tutors:
                logger.warning(f"★ 未找到 {uni['name']} 的导师信息")
                failed_count += 1
                continue

            # 记录提取的导师信息
            sample_names = [t['name'] for t in tutors[:min(5, len(tutors))]]
            logger.info(f"提取到的导师姓名: {', '.join(sample_names)}{'...' if len(tutors) > 5 else ''}")

            all_tutors.extend(tutors)
            success_count += 1
            logger.info(f"√ 成功爬取 {uni['name']} {len(tutors)} 位导师")

            # 随机延迟，避免请求过快
            delay = random.uniform(1.0, 3.0)
            time.sleep(delay)

        except Exception as e:
            logger.error(f"爬取 {uni['name']} 失败: {str(e)}")
            failed_count += 1

    logger.info(f"爬取完成！成功: {success_count}/{len(universities)}, 失败: {failed_count}/{len(universities)}")
    logger.info(f"总共获取到 {len(all_tutors)} 位导师信息")

    # 为每位导师生成评价并存入数据库
    successful_reviews = 0
    failed_reviews = 0

    # 检查是否有有效的导师数据
    if not all_tutors:
        logger.error("没有获取到任何有效的导师信息，跳过评价生成")
        return

    for tutor in all_tutors:
        try:
            # 为每位导师生成1-2条评价
            num_reviews = random.randint(1, 2)

            for idx in range(num_reviews):
                review_data = generate_review_for_tutor(tutor)
                if not review_data:
                    failed_reviews += 1
                    logger.error("生成评价数据失败")
                    continue

                # 生成导师ID
                try:
                    review_data["tutor_id"] = generate_tutor_id(
                        review_data["name"],
                        review_data["university"],
                        review_data["department"]
                    )
                except Exception as e:
                    logger.error(f"生成导师ID失败: {str(e)}")
                    failed_reviews += 1
                    continue

                # 调用ReviewService写入数据库
                try:
                    # 准备提交数据
                    review_payload = {
                        'name': review_data['name'],
                        'university': review_data['university'],
                        'department': review_data['department'],
                        'academic': review_data['academic'],
                        'responsibility': review_data['responsibility'],
                        'character': review_data['character'],
                        'tutor_id': review_data["tutor_id"],
                        'position': review_data.get('position', ''),
                        'research': review_data.get('research', ''),
                        'url': review_data.get('url', '')
                    }

                    logger.info(f"提交评价数据: {review_data['name']} - {review_data['university']}")

                    result = ReviewService.submit_review(review_payload, review_data['user_id'])

                    if result.get("success"):
                        successful_reviews += 1
                        logger.info(f"✅ 提交成功: {review_data['name']} - {review_data['university']}")
                    else:
                        failed_reviews += 1
                        error_msg = result.get("message", "未知错误")
                        logger.error(f"❌ 提交失败: {review_data['name']} - {error_msg}")
                except Exception as e:
                    logger.error(f"提交评价失败: {str(e)}\n{traceback.format_exc()}")
                    failed_reviews += 1

                # 写入后短暂暂停
                time.sleep(0.05)

        except Exception as e:
            logger.error(f"处理导师 {tutor.get('name', '未知')} 失败: {str(e)}\n{traceback.format_exc()}")
            failed_reviews += 1

    logger.info(f"数据处理完成！成功评价: {successful_reviews}, 失败: {failed_reviews}")
    logger.info(f"总共生成评价: {successful_reviews + failed_reviews} 条")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        logger.info("程序被用户中断")
    except Exception as e:
        logger.critical(f"程序崩溃: {str(e)}\n{traceback.format_exc()}")