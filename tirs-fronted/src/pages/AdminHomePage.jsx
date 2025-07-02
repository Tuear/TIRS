// AdminHomePage.jsx
import React, { useState } from 'react';
import Layout from '../components/layout/Layout';
import ProfessorInfoForm from '../components/admin/ProfessorInfoForm'; // 导入表单组件
import PlatformMonitor from '../components/admin/PlatformMonitor'; // 🔴 导入平台监控组件
import UserManagement from '../components/admin/UserManagement'; // 🔴 导入用户管理组件
import EvaluationManagement from '../components/admin/EvaluationManagement'; // 🔴 导入评价管理组件

const AdminHomePage = () => {
  // 状态：标记当前激活的功能面板（null表示默认占位）
  const [currentPanel, setCurrentPanel] = useState(null);  

  // 点击左侧按钮时，切换当前面板
  const handlePanelSwitch = (panelKey) => {
    setCurrentPanel(panelKey);
  };

  return (
    <Layout>
      <div className="flex flex-row min-h-[calc(100vh-120px)]"> 
        {/* 左侧导航栏：按钮绑定切换事件 */}
        <aside className="w-72 bg-gray-100 p-5 space-y-4">
          <button 
            className="w-full px-5 py-3 rounded-lg bg-white shadow-sm 
                       hover:bg-gray-50 transition-colors text-base font-medium"
            onClick={() => handlePanelSwitch('professor')}
          >
            导师信息维护
          </button>
          <button 
            className="w-full px-5 py-3 rounded-lg bg-white shadow-sm 
                       hover:bg-gray-50 transition-colors text-base font-medium"
            onClick={() => handlePanelSwitch('evaluation')}
          >
            评价管理
          </button>
          <button 
            className="w-full px-5 py-3 rounded-lg bg-white shadow-sm 
                       hover:bg-gray-50 transition-colors text-base font-medium"
            onClick={() => handlePanelSwitch('user')}
          >
            用户管理
          </button>
          <button 
            className="w-full px-5 py-3 rounded-lg bg-white shadow-sm 
                       hover:bg-gray-50 transition-colors text-base font-medium"
            onClick={() => handlePanelSwitch('monitor')}
          >
            平台监控
          </button>
        </aside>

         {/* 右侧内容区：根据 currentPanel 渲染组件 */}
        <main className="flex-1 p-8">
          <div className="bg-white border border-gray-200 rounded-lg shadow-md p-6 h-full">
            {currentPanel === 'professor' ? ( // 🔴 导师信息维护的条件渲染
              <ProfessorInfoForm />
            ) : currentPanel === 'monitor' ? ( // 🔴 平台监控的条件渲染
              <PlatformMonitor />
            ) : currentPanel === 'user' ? ( // 🔴 用户管理的条件渲染
              <UserManagement />
            ) : currentPanel === 'evaluation' ? ( // 🔴 评价管理的条件渲染
              <EvaluationManagement />
            ) : (
              <div className="flex items-center justify-center h-full">
                <div className="text-center text-gray-500">
                  <svg xmlns="http://www.w3.org/2000/svg" className="h-16 w-16 mx-auto mb-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                  </svg>
                  <p className="text-lg font-medium">请从左侧选择功能进行操作</p>
                  <p className="mt-2">当前选择：{currentPanel ? `${currentPanel}功能` : '未选择任何功能'}</p>
                </div>
              </div>
            )}
          </div>
        </main>
      </div>
    </Layout>
  );
};

export default AdminHomePage;