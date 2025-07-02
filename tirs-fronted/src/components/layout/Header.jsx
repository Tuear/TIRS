import React from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../../context/AuthContext';
import Button from '../ui/Button';

const Header = () => {
  const { isAuthenticated, user, role, logout } = useAuth();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  return (
    <header className="bg-gray-800 text-white p-4 flex justify-between items-center shadow-md border-b border-gray-700" >
      <div className="text-xl font-bold">基于学生评价的导师智能推荐系统</div>
      
      {isAuthenticated && (
        <div className="flex items-center space-x-4">
          <span>
            {user?.user_id} {/* 直接显示用户ID */}
            ({role === 'admin' ? '管理员' : role === '学生' ? '学生' : '用户'}) {/* 角色说明 */}
          </span>
          <Button onClick={handleLogout} variant="outline" size="sm">
            退出登录
          </Button>
        </div>
      )}
    </header>
  );
};

export default Header;