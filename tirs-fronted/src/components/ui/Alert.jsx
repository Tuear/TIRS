import React from 'react';

const Alert = ({ type, message }) => {
  // 根据类型切换背景色
  const bgClass = {
    error: 'bg-red-100 border-red-400 text-red-700',
    success: 'bg-green-100 border-green-400 text-green-700',
  }[type] || 'bg-blue-100 border-blue-400 text-blue-700';

  return (
    <div className={`border-l-4 p-3 mb-4 ${bgClass}`} role="alert">
      <p className="text-sm font-medium">{message}</p>
    </div>
  );
};

export default Alert;