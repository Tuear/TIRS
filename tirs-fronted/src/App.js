import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { AuthProvider, useAuth } from './context/AuthContext';
import LoginPage from './pages/LoginPage.jsx';
import RegisterPage from './pages/RegisterPage';
import UserHomePage from './pages/UserHomePage';
import AdminHomePage from './pages/AdminHomePage';
// 导入评价页面组件（需确保 SubmitReviewPage 已创建）
import SubmitReviewPage from './pages/SubmitReviewPage';

// 权限保护路由（原有逻辑保留）
const ProtectedRoute = ({ children, requiredRole }) => {
  const { isAuthenticated, role } = useAuth();

  // 未登录 → 重定向到登录页
  if (!isAuthenticated) {
    return <Navigate to="/login" replace />;
  }

  // 角色不匹配 → 重定向到对应角色首页
  if (requiredRole && role !== requiredRole) {
    return <Navigate to={role === 'admin' ? '/admin' : '/user'} replace />;
  }

  return children;
};

function AppRoutes() {
  return (
    <Routes>
      {/* 公共路由：登录/注册 */}
      <Route path="/login" element={<LoginPage />} />
      <Route path="/register" element={<RegisterPage />} />

      {/* 用户私有路由：推荐系统（根路径） + 评价页面（子路径） */}
      <Route path="/user" element={
        <ProtectedRoute>
          <UserHomePage />
        </ProtectedRoute>
      } />
      {/* 🔴 关键修正：给评价页面独立子路径，避免路由重复 */}
      <Route path="/user/submit-review" element={
        <ProtectedRoute>
          <SubmitReviewPage />
        </ProtectedRoute>
      } />

      {/* 管理员私有路由（原有逻辑保留） */}
      <Route path="/admin" element={
        <ProtectedRoute requiredRole="admin">
          <AdminHomePage />
        </ProtectedRoute>
      } />

      {/* 404 兜底：重定向到登录页 */}
      <Route path="*" element={<Navigate to="/login" replace />} />
    </Routes>
  );
}

function App() {
  return (
    <AuthProvider>
      <Router>
        <AppRoutes />
      </Router>
    </AuthProvider>
  );
}

export default App;