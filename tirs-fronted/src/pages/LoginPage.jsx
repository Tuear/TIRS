import React from 'react';
import LoginForm from '../components/auth/LoginForm';
import Card from '../components/ui/Card';

const LoginPage = () => {
  return (
    <div className="flex flex-col min-h-screen bg-gray-50 lg:flex-row">
    {/* 全屏弹性容器：大屏左右分栏，小屏上下堆叠 */}
      {/* 左侧背景区（使用 public 目录图片） */}
      <div 
        className="relative w-full lg:w-1/2 bg-cover bg-center" 
        style={{ backgroundImage: "url('/images/login-bg.jpg')" }} 
      >
        {/* 渐变遮罩增强文字可读性 */}
        <div className="absolute inset-0 bg-gradient-to-r from-cyan-500 to-blue-500 opacity-75" />
        <div className="relative flex flex-col items-start justify-end h-full p-6 text-white">
          <h1 className="text-2xl font-bold">欢迎使用智能导师推荐系统</h1>
          <p className="mt-2 text-base">安全、稳定、高效的导师推荐平台</p>
        </div>
      </div>

      {/* 右侧表单区（纯白背景+参考图布局） */}
      <div className="flex flex-col items-center justify-center w-full lg:w-1/2 p-8 bg-white">
        <div className="w-full max-w-xs space-y-4">
          {/* 顶部图标+欢迎文案 */}
          <div className="text-center">
            {/* 锁形图标（SVG 内联，无需额外资源） */}
            <svg 
              className="mx-auto h-10 w-10 text-blue-600" 
              fill="currentColor" 
              viewBox="0 0 24 24"
            >
              <path d="M12 2a10 10 0 0 1 10 10v7a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2v-7a10 10 0 0 1 10-10zm0 12a2 2 0 1 0 0-4 2 2 0 0 0 0 4zm0-7a5 5 0 0 0-5 5v2h10v-2a5 5 0 0 0-5-5z" />
            </svg>
            <h2 className="mt-2 text-xl font-semibold text-gray-800">欢迎回来</h2>
            <p className="mt-1 text-sm text-gray-500">请登录您的账户继续使用</p>
          </div>

          {/* 登录表单卡片 */}
          <Card className="p-4 bg-white shadow sm:rounded-md">
            <LoginForm />
          </Card>

          {/* 注册引导 */}
          <p className="text-center text-sm text-gray-500">
            还没有账户？ 
            <a 
              href="/register" 
              className="font-medium text-blue-600 hover:text-blue-700"
            >
              立即注册
            </a>
          </p>

          {/* 底部版权（与参考图一致） */}
          <p className="text-center text-xs text-gray-400">
            © 2025 智能导师推荐系统. 保留所有权利 made by fsr lqw
          </p>
        </div>
      </div>
    </div>
  );
};

export default LoginPage;