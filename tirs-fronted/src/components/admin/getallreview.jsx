import React, { useState } from 'react';
import { getallreview } from '../../api/reviewmanageApi'; // 替换为实际接口文件路径

const AdminPage = () => {
  const [reviews, setReviews] = useState([]); // 存储评价列表
  const [error, setError] = useState('');      // 存储接口错误信息

  // 点击“评价管理”时执行的逻辑
  const handleEvaluationManage = async () => {
    try {
      const result = await getallreview(); 
      // 确保接口返回数据中包含 `user_id` 字段（需后端配合）
      setReviews(result.data); 
      setError('');            
    } catch (err) {
      setError(err.error);    // 捕获并显示接口错误
      setReviews([]);         // 清空列表（可选，根据需求设计）
    }
  };

  return (
    <div className="admin-layout">
      {/* 左侧功能按钮栏 */}
      <aside className="sidebar">
        <button onClick={handleEvaluationManage}>评价管理</button>
        {/* 其他功能按钮（导师信息维护、用户管理等） */}
      </aside>

      {/* 中间内容区 */}
      <main className="content">
        {error ? (
          <div className="error">{error}</div>
        ) : reviews.length > 0 ? (
          <div className="reviews-list">
            {reviews.map((review) => (
              <div key={review.评价ID} className="review-item">
                <p>评价ID：{review.评价ID}</p>
                {/* 新增：展示用户ID */}
                <p>用户ID：{review.user_id}</p>  
                <p>导师姓名：{review.导师姓名}</p>
                <p>学校：{review.学校}</p>
                <p>学院/系：{review.学院/系}</p>
                <p>评价内容：{review.评价内容}</p>
              </div>
            ))}
          </div>
        ) : (
          <div className="placeholder">请从左侧选择功能进行操作</div>
        )}
      </main>
    </div>
  );
};

export default AdminPage;