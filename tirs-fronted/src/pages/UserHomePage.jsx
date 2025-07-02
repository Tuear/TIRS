import React, { useState } from 'react';
import Layout from '../components/layout/Layout';
import RecommendationForm from '../components/user/RecommendationForm'; 
import RecommendationResult from '../components/user/RecommendationResult'; 

const UserHomePage = () => {
  const [recommendations, setRecommendations] = useState([]);

  // 接收推荐结果并更新状态
  const handleRecommendations = (results) => {
    console.log('父组件收到推荐结果：', results); 
    setRecommendations(Array.isArray(results) ? results : []); 
  };

  // 🔴 新增：「返回推荐」时清空结果，切换回表单
  const handleBackToForm = () => {
    setRecommendations([]); // 清空推荐结果 → 触发组件切换
  };

  return (
    <Layout>
      <div 
        className="min-h-screen bg-cover bg-center" 
        style={{ backgroundImage: "url('/images/userhome.jpg')" }}
      >
        <div className="flex justify-center items-center min-h-screen px-4 py-8">
          <div className="w-full max-w-2xl"> 
            {/** 根据推荐结果长度切换组件 **/}
            {recommendations.length === 0 ? (
              <RecommendationForm onSubmit={handleRecommendations} />
            ) : (
              <RecommendationResult 
                recommendations={recommendations} 
                onBack={handleBackToForm} 
              />
            )}
          </div>
        </div>
      </div>
    </Layout>
  );
};

export default UserHomePage;