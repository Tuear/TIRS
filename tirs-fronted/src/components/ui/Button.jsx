import React from 'react';

const Button = ({ children, className, disabled, ...props }) => {
  return (
    <button
      disabled={disabled}
      // 合并内部基础样式 + 外部传入的 className
      className={`
        px-4 py-2 
        bg-blue-600 hover:bg-blue-700 
        text-white font-bold 
        rounded transition-colors 
        ${disabled ? 'bg-gray-400 cursor-not-allowed' : ''} 
        ${className}
      `}
      {...props}
    >
      {children}
    </button>
  );
};

export default Button;