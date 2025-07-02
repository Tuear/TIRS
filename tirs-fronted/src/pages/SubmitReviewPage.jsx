import React, { useState } from 'react';
import Layout from '../components/layout/Layout';
import { submitReview } from '../api/submitreviewApi'; // 接口文件路径需与实际一致
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';

const SubmitReviewPage = () => {
  const navigate = useNavigate();
  const { user } = useAuth(); // 获取用户信息（用于传递 user_id）

  // 表单状态：包含接口要求的 7 个字段（新增 user_id）
  const [formData, setFormData] = useState({
    name: '',          // 导师姓名
    university: '',    // 所属院校
    department: '',    // 所属院系
    academic: '',      // 学术风格 → 对应接口 academic
    responsibility: '',// 人品 → 对应接口 responsibility
    character: '',     // 性格 → 对应接口 character
    user_id: user?.user_id, // 可选链避免未登录时报错（权限路由已保障登录态）
  });
  const [isLoading, setIsLoading] = useState(false); // 提交加载态
  const [error, setError] = useState('');            // 错误提示

  // 输入变化处理
  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: value }));
  };

  // 表单提交逻辑（原有逻辑保留）
  const handleSubmit = async (e) => {
    e.preventDefault();
    setIsLoading(true);
    setError('');

    // 非空验证：所有字段必填
    if (Object.values(formData).some(val => val.trim() === '')) {
      setError('请完整填写所有评价项～');
      setIsLoading(false);
      return;
    }

    try {
      await submitReview(formData);
      alert('评价提交成功！');
      navigate('/user'); // 提交后返回用户首页
    } catch (err) {
      setError(err.error || '提交失败，请检查网络或重试～');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <Layout>
      {/* 背景图（与推荐页复用） */}
      <div
        className="min-h-screen bg-cover bg-center"
        style={{ backgroundImage: "url('/images/userhome.jpg')" }}
      >
        <div className="flex justify-center items-center min-h-screen px-4 py-8">
          <div className="w-full max-w-xl bg-white/70 backdrop-blur-sm shadow-md rounded-xl p-6 space-y-4">

            {/* 🔴 标题 + 右上角返回按钮区域 */}
            <div className="flex justify-between items-center">
              <h2 className="text-xl font-semibold text-gray-900">提交导师评价</h2>
              <button
                onClick={() => navigate('/user')}
                className="text-blue-500 hover:text-blue-600 text-sm font-medium"
              >
                返回
              </button>
            </div>

            {/* 错误提示 */}
            {error && <p className="text-red-500 text-sm text-center">{error}</p>}

            {/* 评价表单（原有字段保留） */}
            <form onSubmit={handleSubmit} className="space-y-4">
              {/* 1. 导师姓名 */}
              <div>
                <label
                  htmlFor="name"
                  className="block text-sm font-medium text-gray-700 mb-1"
                >
                  姓名
                </label>
                <input
                  type="text"
                  id="name"
                  name="name"
                  value={formData.name}
                  onChange={handleInputChange}
                  placeholder="请输入导师姓名"
                  className="w-full px-3 py-2 border border-gray-200 rounded-md shadow-sm
                    focus:outline-none focus:ring-blue-400 focus:border-blue-400 text-sm
                    bg-white/90"
                  disabled={isLoading}
                />
              </div>

              {/* 2. 所属院校 */}
              <div>
                <label
                  htmlFor="university"
                  className="block text-sm font-medium text-gray-700 mb-1"
                >
                  学校
                </label>
                <input
                  type="text"
                  id="university"
                  name="university"
                  value={formData.university}
                  onChange={handleInputChange}
                  placeholder="请输入学校名称"
                  className="w-full px-3 py-2 border border-gray-200 rounded-md shadow-sm
                    focus:outline-none focus:ring-blue-400 focus:border-blue-400 text-sm
                    bg-white/90"
                  disabled={isLoading}
                />
              </div>

              {/* 3. 所属院系 */}
              <div>
                <label
                  htmlFor="department"
                  className="block text-sm font-medium text-gray-700 mb-1"
                >
                  学院
                </label>
                <input
                  type="text"
                  id="department"
                  name="department"
                  value={formData.department}
                  onChange={handleInputChange}
                  placeholder="请输入学院名称"
                  className="w-full px-3 py-2 border border-gray-200 rounded-md shadow-sm
                    focus:outline-none focus:ring-blue-400 focus:border-blue-400 text-sm
                    bg-white/90"
                  disabled={isLoading}
                />
              </div>

              {/* 4. 学术风格（对应接口 academic） */}
              <div>
                <label
                  htmlFor="academic"
                  className="block text-sm font-medium text-gray-700 mb-1"
                >
                  学术风格
                </label>
                <input
                  type="text"
                  id="academic"
                  name="academic"
                  value={formData.academic}
                  onChange={handleInputChange}
                  placeholder="请输入导师的学术风格"
                  className="w-full px-3 py-2 border border-gray-200 rounded-md shadow-sm
                    focus:outline-none focus:ring-blue-400 focus:border-blue-400 text-sm
                    bg-white/90"
                  disabled={isLoading}
                />
              </div>

              {/* 5. 人品（对应接口 responsibility） */}
              <div>
                <label
                  htmlFor="responsibility"
                  className="block text-sm font-medium text-gray-700 mb-1"
                >
                  人品
                </label>
                <input
                  type="text"
                  id="responsibility"
                  name="responsibility"
                  value={formData.responsibility}
                  onChange={handleInputChange}
                  placeholder="描述导师的人品"
                  className="w-full px-3 py-2 border border-gray-200 rounded-md shadow-sm
                    focus:outline-none focus:ring-blue-400 focus:border-blue-400 text-sm
                    bg-white/90"
                  disabled={isLoading}
                />
              </div>

              {/* 6. 性格（对应接口 character） */}
              <div>
                <label
                  htmlFor="character"
                  className="block text-sm font-medium text-gray-700 mb-1"
                >
                  性格
                </label>
                <input
                  type="text"
                  id="character"
                  name="character"
                  value={formData.character}
                  onChange={handleInputChange}
                  placeholder="描述导师的性格"
                  className="w-full px-3 py-2 border border-gray-200 rounded-md shadow-sm
                    focus:outline-none focus:ring-blue-400 focus:border-blue-400 text-sm
                    bg-white/90"
                  disabled={isLoading}
                />
              </div>

              {/* 提交按钮（加载态处理） */}
              <button
                type="submit"
                className={`w-full bg-blue-500 hover:bg-blue-600 text-white py-2 px-4 rounded-md
                  transition duration-300 ease-in-out text-sm font-medium
                  ${isLoading ? 'opacity-50 cursor-not-allowed' : ''}`}
                disabled={isLoading}
              >
                {isLoading ? '提交中...' : '提交评价'}
              </button>
            </form>
          </div>
        </div>
      </div>
    </Layout>
  );
};

export default SubmitReviewPage;