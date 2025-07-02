import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../../context/AuthContext';
import { loginUser, loginAdmin } from '../../api/authApi';
import Alert from '../ui/Alert';

const LoginForm = () => {
  const [formData, setFormData] = useState({ id: '', password: '' });
  const [isAdminLogin, setIsAdminLogin] = useState(false); 
  const [rememberMe, setRememberMe] = useState(false);     
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const { login } = useAuth();
  const navigate = useNavigate();

  // 输入/记住我/提交逻辑 保留原有功能
  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };
  const handleRemember = (e) => {
    setRememberMe(e.target.checked);
  };
  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');
    try {
      const response = isAdminLogin 
        ? await loginAdmin({ user_id: formData.id, password: formData.password })
        : await loginUser({ user_id: formData.id, password: formData.password });
      login({
        user_id: isAdminLogin ? response.admin_id : response.user_id,
        role: response.role  
      });
      if (rememberMe) localStorage.setItem('rememberedUser', JSON.stringify(formData.id));
      else localStorage.removeItem('rememberedUser');
      navigate(response.role === 'admin' ? '/admin' : '/user');
    } catch (err) {
      setError(err.error || '登录失败，请重试');
    } finally {
      setLoading(false);
    }
  };

  return (

    <div className="w-full max-w-sm mx-auto"> 
        {/* 🔴 容器改为「自适应高度+水平居中」，去掉强制满屏 */}
      {/* 🔴 卡片缩小宽度+压缩内边距+紧凑间距 */}
      <div className="bg-white/20 backdrop-blur-md border border-gray-100 rounded-xl shadow-md p-4 space-y-3">
        <form onSubmit={handleSubmit} className="space-y-3">
          {/* 错误提示（保留） */}
          {error && <Alert type="error" message={error} />}

          {/* 🔴 用户名输入组：缩小标签间距+紧凑布局 */}
          <div>
            <label 
              htmlFor="id" 
              className="block text-sm font-medium text-gray-900 mb-0.5" // 缩小标签下边距
            >
              {isAdminLogin ? "管理员ID" : "用户ID"}
            </label>
            <div className="relative">
              <input
                type="text"
                name="id"
                value={formData.id}
                onChange={handleChange}
                required
                className="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-blue-500 focus:border-blue-500 text-sm"
              />
              <span className="absolute inset-y-0 left-0 flex items-center pl-3 text-gray-400">
                {isAdminLogin ? (
                  <svg className="h-5 w-5" fill="currentColor" viewBox="0 0 20 20">
                    <path d="M10 2a5 5 0 0 1 5 5v2a2 2 0 0 1-2 2h-1v3a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2v-3H5a2 2 0 0 1-2-2V7a5 5 0 0 1 5-5zm0 4a3 3 0 0 0-3 3v2h6V9a3 3 0 0 0-3-3zm-1 8v3h2v-3H9z" />
                  </svg>
                ) : (
                  <svg className="h-5 w-5" fill="currentColor" viewBox="0 0 20 20">
                    <path d="M10 2a8 8 0 0 1 8 8v6a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2v-6a8 8 0 0 1 8-8zm0 10a2 2 0 1 0 0-4 2 2 0 0 0 0 4zm0-6a4 4 0 1 0 0 8 4 4 0 0 0 0-8z" />
                  </svg>
                )}
              </span>
            </div>
          </div>

          {/* 🔴 密码输入组：同用户名组逻辑，缩小间距 */}
          <div>
            <label 
              htmlFor="password" 
              className="block text-sm font-medium text-gray-900 mb-0.5"
            >
              {isAdminLogin ? "管理员密码" : "登录密码"}
            </label>
            <div className="relative">
              <input
                type="password"
                name="password"
                value={formData.password}
                onChange={handleChange}
                required
                className="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-blue-500 focus:border-blue-500 text-sm"
              />
              <span className="absolute inset-y-0 left-0 flex items-center pl-3 text-gray-400">
                <svg className="h-5 w-5" fill="currentColor" viewBox="0 0 20 20">
                  <path d="M10 2a5 5 0 0 1 5 5v2a2 2 0 0 1-2 2h-1v3a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2v-3H5a2 2 0 0 1-2-2V7a5 5 0 0 1 5-5zm0 4a3 3 0 0 0-3 3v2h6V9a3 3 0 0 0-3-3zm-1 8v3h2v-3H9z" />
                </svg>
              </span>
            </div>
          </div>

          {/* 🔴 记住我 + 管理员切换：紧凑行布局 */}
          <div className="flex items-center justify-between text-sm">
            <label className="flex items-center space-x-2"> {/* 缩小checkbox与文字间距 */}
              <input
                type="checkbox"
                className="h-4 w-4 text-blue-600 border-gray-300 rounded"
                checked={rememberMe}
                onChange={handleRemember}
              />
              记住我
            </label>
            <button
              type="button"
              onClick={() => setIsAdminLogin(!isAdminLogin)}
              className="px-2 py-1 border border-blue-500 text-blue-500 rounded-md hover:bg-blue-500 hover:text-white transition-colors text-xs" // 缩小按钮尺寸
            >
              {isAdminLogin ? '切换为用户登录' : '管理员登录'}
            </button>
          </div>

          {/* 🔴 登录按钮：保留原有样式，压缩高度 */}
          <button
            type="submit"
            disabled={loading}
            className="w-full py-2 px-4 bg-blue-600 hover:bg-blue-700 text-white font-medium rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 text-sm"
          >
            {loading ? '登录中...' : '登录'}
          </button>
        </form>
      </div>
    </div>
  );
};

export default LoginForm;