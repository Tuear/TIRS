import React, { useState, useEffect } from 'react';
import { Table, Pagination, message } from 'antd'; 
import { getAllUsers, toggleUserPermission } from '../../api/GetAllUserApi'; 
import Button from '../ui/Button'; // 自定义 Button 组件路径（需与实际一致）

const UserManagement = () => {
  const [users, setUsers] = useState([]);
  const [loading, setLoading] = useState(true);
  const [total, setTotal] = useState(0);   
  const [currentPage, setCurrentPage] = useState(1); 
  const pageSize = 10; 

  // 获取用户数据（保持原逻辑）
  const fetchUsers = async (page = 1) => {
    setLoading(true);
    try {
      const res = await getAllUsers(); 
      if (res.success) {
        setUsers(res.data);       
        setTotal(res.total || 0); 
        setCurrentPage(page);    
      } else {
        message.error(res.error || '获取用户信息失败');
      }
    } catch (err) {
      message.error(err.error || '网络错误，请重试');
    } finally {
      setLoading(false);
    }
  };

  // 处理权限更新：点击“启用”传 'True'，点击“禁用”传 'False'
  const handleUpdatePermission = async (targetUserId, enable) => {
    try {
      // 正确传递参数：target_user 和 enable（字符串值）
      await toggleUserPermission({
        target_user: targetUserId,
        enable: enable // 直接使用字符串值 'True' 或 'False'
      });
      
      message.success(`评价权限已${enable === 'True' ? '启用' : '禁用'}`);
      await fetchUsers(currentPage); // 刷新当前页保证数据同步
    } catch (err) {
      message.error(err.error || '切换权限失败');
    }
  };

  
  useEffect(() => {
    fetchUsers();
  }, []);

  const columns = [
    {
      title: '用户ID',        
      dataIndex: 'user_id',  
      key: 'user_id',
      align: 'center',       
    },
    {
      title: '角色',          
      dataIndex: 'role',     
      key: 'role',
      align: 'center',
    },
    {
      title: '评价权限',      
      dataIndex: 'review_allowed', 
      key: 'review_allowed',
      align: 'center',
      render: (text) => (text === 'True' ? '是' : '否'),
    },
    {
      title: '操作',          
      key: 'operation',
      align: 'center',
      // 🔵 用 Tailwind 工具类实现：居中 + 增大间距
      render: (_, record) => (
        <div className="flex justify-center space-x-8"> 
          {/* 启用按钮 - 绿色样式（Tailwind） */}
          <Button 
            className="bg-green-500 hover:bg-green-600" 
            onClick={() => handleUpdatePermission(record.user_id, 'True')}
          >
            启用
          </Button>
          {/* 禁用按钮 - 红色样式（Tailwind） */}
          <Button 
            className="bg-red-500 hover:bg-red-600" 
            onClick={() => handleUpdatePermission(record.user_id, 'False')}
          >
            禁用
          </Button>
        </div>
      ),
    },
  ];

  return (
    <div style={{ padding: '20px' }}>
      <Table
        columns={columns}
        dataSource={users}
        loading={loading}
        bordered          
        rowKey="user_id"   
        pagination={false} 
        style={{ background: '#fff' }} 
      />
      <Pagination
        current={currentPage}
        pageSize={pageSize}
        total={total}
        onChange={(page) => fetchUsers(page)} 
        style={{ marginTop: '16px', textAlign: 'right' }} 
      />
    </div>
  );
};

export default UserManagement;