import React, { createContext, useState, useContext, useEffect } from 'react';

const AuthContext = createContext(null);

export const AuthProvider = ({ children }) => {
  const [authState, setAuthState] = useState({
    isAuthenticated: false,
    user: null,
    role: null
  });

  useEffect(() => {
    const storedAuth = localStorage.getItem('auth');
    if (storedAuth) {
      setAuthState(JSON.parse(storedAuth));
    }
  }, []);

const login = (userData) => {
  // 1. 提取后端返回的「唯一标识」（用户取 user_id / 管理员取 admin_id）
  const uniqueId = userData.user_id || userData.admin_id;  

  // 2. 构造与原逻辑完全一致的认证状态
  const newAuthState = {
    isAuthenticated: true,
    user: {
      user_id: userData.user_id,  // 改为使用后端返回的user_id字段
      role: userData.role
    },
    role: userData.role // 外层 role 字段也保持原逻辑
  };

  // 3. 保持原有状态更新+LocalStorage 存储逻辑
  setAuthState(newAuthState);
  localStorage.setItem('auth', JSON.stringify(newAuthState));
};

  const logout = () => {
    setAuthState({ isAuthenticated: false, user: null, role: null });
    localStorage.removeItem('auth');
  };

  return (
    <AuthContext.Provider value={{ ...authState, login, logout }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => useContext(AuthContext);