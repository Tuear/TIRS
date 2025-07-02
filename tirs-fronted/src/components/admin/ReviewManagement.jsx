import React, { useState, useEffect } from 'react';
import { Table, Spin, Alert } from 'antd'; // 需确保已安装 antd
import { getAllReviews } from '../../api/reviewmanageApi'; // 替换为实际接口文件路径

const ReviewManagement = () => {
  const [reviews, setReviews] = useState([]); // 存储评价列表（含 user_id 字段）
  const [loading, setLoading] = useState(true); // 加载状态
  const [error, setError] = useState(''); // 错误信息

  // 组件挂载时自动获取评价数据（含用户ID）
  useEffect(() => {
    const fetchReviews = async () => {
      setLoading(true);
      setError('');
      try {
        const res = await getAllReviews(); 
        // 假设接口返回格式：{ data: 评价数组, message: "提示" }，数组元素需包含 `user_id` 字段
        setReviews(res.data || []); 
        setLoading(false);
      } catch (err) {
        // 捕获接口抛出的错误（格式：{ error: "错误信息" }）
        setError(err.error || '获取评价失败，请重试');
        setLoading(false);
      }
    };
    fetchReviews();
  }, []); // 仅在组件挂载时执行一次


  // 定义表格列（新增「用户ID」列，与接口返回的 `user_id` 字段对应）
  const columns = [
    {
      title: '用户ID',
      dataIndex: 'user_id', // 对应接口返回的 `user_id` 字段
      key: 'user_id',
      width: 120, // 可根据需求调整列宽
    },
    {
      title: '评价ID',
      dataIndex: '评价ID', // 与接口返回的「评价ID」字段名保持一致（若接口返回是 sentence_id，需改为 sentence_id）
      key: '评价ID',
      width: 180,
    },
    {
      title: '导师姓名',
      dataIndex: '导师姓名',
      key: '导师姓名',
    },
    {
      title: '学校',
      dataIndex: '学校',
      key: '学校',
    },
    {
      title: '学院/系',
      dataIndex: '学院/系',
      key: '学院/系',
    },
    {
      title: '评价内容',
      dataIndex: '评价内容',
      key: '评价内容',
      width: 300, // 长文本列可适当加宽
    },
    {
      title: '操作', // 保留截图中的「删除」操作列（示例）
      key: 'operation',
      render: (text, record) => (
        <button 
          type="button" 
          style={{ color: '#f5222d', border: '1px solid #f5222d' }}
          // 此处可绑定删除逻辑（如调用 deleteReview 接口）
          onClick={() => handleDelete(record)} 
        >
          删除
        </button>
      ),
    },
  ];

  // 「删除」操作逻辑（示例，需结合实际接口实现）
  const handleDelete = (record) => {
    // 示例：调用删除接口
    // deleteReview(record.评价ID).then(() => fetchReviews()); 
    console.log('待删除的评价ID：', record.评价ID);
  };


  // 根据状态渲染不同 UI
  return (
    <div style={{ padding: 20 }}>
      {loading ? (
        // 加载中状态
        <Spin tip="加载评价数据中...">
          <div style={{ height: 200 }} /> {/* 占位防止页面跳动 */}
        </Spin>
      ) : error ? (
        // 错误状态
        <Alert message="获取失败" description={error} type="error" showIcon />
      ) : reviews.length === 0 ? (
        // 无数据状态
        <Alert message="提示" description="当前暂无评价数据" type="info" showIcon />
      ) : (
        // 数据展示：Ant Design Table 组件
        <Table
          columns={columns}
          dataSource={reviews}
          rowKey="评价ID" // 用「评价ID」作为行唯一标识（需与接口返回的主键字段一致）
          bordered // 带边框表格
          pagination={{ pageSize: 10 }} // 分页配置（每页10条）
          scroll={{ x: 1200 }} // 若列过多，可开启横向滚动
        />
      )}
    </div>
  );
};

export default ReviewManagement;