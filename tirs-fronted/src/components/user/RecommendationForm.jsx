import React, { useState, useEffect } from 'react';
import { getRecommendations } from '../../api/getcommendApi'; 
// 🔴 新增：导入路由跳转 Hook（基于 React Router v6）
import { useNavigate } from 'react-router-dom';

const RecommendationForm = ({ onSubmit }) => {
  const [formData, setFormData] = useState({
    query: '',
    university: '', // 存储学校 ID（如 "上海交通大学" 或 "qb"）
    department: ''  // 存储学院 ID（如 "化学化工学院" 或 "qb"）
  });
  const [universities, setUniversities] = useState([]); // 学校选项：[{id, name}, ...]
  const [departments, setDepartments] = useState([]);   // 学院选项：[{id, name}, ...]
  const [isLoading, setIsLoading] = useState(false);
  // 🔴 初始化路由跳转实例
  const navigate = useNavigate();

  // 🔴 新增：点击「我要评价」跳转到评论页面（需在路由配置中定义 /rate 路径）
  const handleRateClick = () => {
    navigate('/user/submit-review');
  };

  // 🔴 第一步：加载学校列表（从 public 目录的 JSON 文件读取）
  useEffect(() => {
    const fetchUniversities = async () => {
      try {
        // 读取 public 下的 JSON 文件（React 中根路径即为 public）
        const response = await fetch('/supported_universities.json');
        const data = await response.json();

        // 构造学校选项：[ {id: 'qb', name: '全部'}, {id: '上海交通大学', name: '上海交通大学'}, ... ]
        const universityOptions = [
          { id: 'qb', name: '全部' }, // “全部”学校的 ID 约定为 "qb"
          ...Object.keys(data).map(uniName => ({
            id: uniName,
            name: uniName
          }))
        ];
        setUniversities(universityOptions);
      } catch (error) {
        console.error('加载学校列表失败:', error);
        // 错误兜底：仅保留“全部”选项
        setUniversities([{ id: 'qb', name: '全部' }]);
      }
    };
    fetchUniversities();
  }, []);

  // 🔴 第二步：学校变化时，加载对应院系列表（含“全部”选项）
  useEffect(() => {
    if (formData.university) { // 学校已选择时才加载学院
      const fetchDepartments = async () => {
        setIsLoading(true);
        try {
          const response = await fetch('/supported_universities.json');
          const data = await response.json();
          let deptOptions = [];

          // 处理「全部学校」的情况（学校 ID 为 "qb"）
          if (formData.university === 'qb') {
            deptOptions = [ { id: 'qb', name: '全部' } ]; // 学院也显示“全部”
          } else {
            // 读取 JSON 中对应学校的学院列表，添加“全部”选项
            const targetDepts = data[formData.university] || []; // 如 data["上海交通大学"]
            deptOptions = [
              { id: 'qb', name: '全部' }, // “全部”学院的 ID 约定为 "qb"
              ...targetDepts.map(deptName => ({
                id: deptName,
                name: deptName
              }))
            ];
          }

          setDepartments(deptOptions);
          setIsLoading(false);
        } catch (error) {
          console.error('加载院系列表失败:', error);
          setDepartments([]);
          setIsLoading(false);
        }
      };
      fetchDepartments();
    } else {
      setDepartments([]); // 学校未选择时，清空学院选项
    }
  }, [formData.university]); // 学校变化时重新加载学院

  // 输入变化处理（学校/学院/需求）
  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: value }));
  };

  // 🔴 第三步：表单提交，传递「全部」或具体名称到后端
  const handleSubmit = async (e) => {
    e.preventDefault();
    // 1. 需求描述非空验证（去空）
    if (!formData.query.trim()) {
      alert('请描述您的导师需求（不可为空或仅空格）');
      return;
    }
    // 2. 学校/学院非空验证（下拉框默认选项已控制，可选加强）
    if (!formData.university || !formData.department) {
      alert('请选择目标学校和学院');
      return;
    }

    try {
      setIsLoading(true);
      // 处理学校参数：“全部”或具体学校名称
      const selectedUniversity = formData.university === 'qb'
        ? '全部'
        : universities.find(u => u.id === formData.university)?.name || formData.university;

      // 处理学院参数：“全部”或具体学院名称
      const selectedDepartment = formData.department === 'qb'
        ? '全部'
        : departments.find(d => d.id === formData.department)?.name || formData.department;

      // 调用 API 传递参数
      const recommendations = await getRecommendations({
        query: formData.query,
        university: selectedUniversity,
        department: selectedDepartment
      });
      onSubmit(Array.isArray(recommendations) ? recommendations : []);
    } catch (error) {
      console.error('推荐失败:', error);
      alert(error.error || '获取推荐失败，请重试');
      onSubmit([]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="max-w-2xl w-full bg-white/70 backdrop-blur-sm shadow-md rounded-xl p-5 space-y-4">
      <div className="text-center">
        <h1 className="text-xl font-semibold text-gray-900">智能导师推荐</h1>
        <p className="mt-2 text-sm text-gray-700">
          请描述您期望的导师类型，并选择学校/学院范围<br />
          系统将为您智能匹配理想导师
        </p>
      </div>

      <form onSubmit={handleSubmit} className="space-y-4">
        {/* 需求输入框 */}
        <div>
          <label
            htmlFor="query"
            className="block text-sm font-medium text-gray-700 mb-1"
          >
            描述导师需求
          </label>
          <textarea
            id="query"
            name="query"
            value={formData.query}
            onChange={handleInputChange}
            placeholder="例如：研究人工智能的年轻导师，有海外经历"
            className="w-full min-h-[120px] px-4 py-3 border border-blue-200 rounded-md shadow-sm
              focus:outline-none focus:ring-blue-400 focus:border-blue-400 text-sm
              bg-white/90 resize-none"
            disabled={isLoading}
          />
        </div>

        {/* 学校+学院选择区 */}
        <div className="flex flex-col space-y-3 sm:flex-row sm:space-y-0 sm:space-x-3">
          {/* 学校选择器 */}
          <div className="w-full sm:w-1/2">
            <label
              htmlFor="university"
              className="block text-sm font-medium text-gray-700 mb-1"
            >
              选择目标学校
            </label>
            <select
              id="university"
              name="university"
              value={formData.university}
              onChange={handleInputChange}
              className="w-full px-3 py-2 border border-blue-200 rounded-md shadow-sm
                focus:outline-none focus:ring-blue-400 focus:border-blue-400 text-sm
                bg-white/90"
              disabled={isLoading || universities.length === 0}
            >
              <option value="">请选择学校</option>
              {universities.map(university => (
                <option key={university.id} value={university.id}>
                  {university.name}
                </option>
              ))}
            </select>
          </div>

          {/* 学院选择器 */}
          <div className="w-full sm:w-1/2">
            <label
              htmlFor="department"
              className="block text-sm font-medium text-gray-700 mb-1"
            >
              选择目标学院
            </label>
            <select
              id="department"
              name="department"
              value={formData.department}
              onChange={handleInputChange}
              className="w-full px-3 py-2 border border-blue-200 rounded-md shadow-sm
                focus:outline-none focus:ring-blue-400 focus:border-blue-400 text-sm
                bg-white/90"
              disabled={isLoading || !formData.university || departments.length === 0}
            >
              <option value="">请选择学院</option>
              {departments.map(department => (
                <option key={department.id} value={department.id}>
                  {department.name}
                </option>
              ))}
            </select>
          </div>
        </div>

        {/* 提交按钮（加载态带 Spinner） */}
        <div className="pt-2">
          <button
            type="submit"
            className={`w-full bg-blue-500 hover:bg-blue-600 text-white py-2 px-4 rounded-md
              transition duration-300 ease-in-out text-sm font-medium
              ${isLoading ? 'opacity-50 cursor-not-allowed' : ''}`}
            disabled={isLoading}
          >
            {isLoading ? (
              <span className="flex items-center justify-center">
                <svg className="animate-spin -ml-1 mr-2 h-4 w-4 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                  <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                  <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                </svg>
                推荐中...
              </span>
            ) : '开始推荐'}
          </button>
        </div>
      </form>

      {/* 🔴 新增：「我要评价」按钮（底部居中，绿色视觉突出） */}
      <div className="mt-4 text-center">
        <button
          onClick={handleRateClick}
          className="bg-green-500 hover:bg-green-600 text-white py-2 px-4 rounded-md
            transition duration-300 ease-in-out text-sm font-medium"
        >
          我要评价
        </button>
      </div>
    </div>
  );
};

export default RecommendationForm;