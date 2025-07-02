import React, { useState } from 'react';
import TutorReview from './TutorReview'; // 确保组件路径正确

const RecommendationResult = ({ recommendations, onBack }) => {
  const [activeReviewTutorId, setActiveReviewTutorId] = useState(null);

  // 「查看详情」逻辑（保留原有交互）
  const handleViewDetails = (url) => {
    if (!url || url.trim() === '') {
      alert('暂无该导师详情信息');
      return;
    }
    window.open(url, '_blank');
  };

  // 「查看评价」：切换到评价组件
  const handleShowReview = (tutorId) => {
    setActiveReviewTutorId(tutorId);
  };

  // 「返回卡片」：切回导师列表
  const handleBackToCard = () => {
    setActiveReviewTutorId(null);
  };

  return (
    <div
      className="bg-gradient-to-b from-white/60 to-white/80
        backdrop-blur-md border border-gray-100 rounded-xl shadow-md
        p-4 space-y-4"
    >
      {/* 标题区：文字居中 + 返回推荐按钮 */}
      <div className="flex justify-between items-center">
        <div className="flex flex-col flex-1 items-center justify-center">
          <h2 className="text-base font-semibold text-gray-900">推荐导师</h2>
          <p className="mt-1 text-xs text-gray-700">
            为您智能匹配到以下导师，点击按钮查看详情或评价
          </p>
        </div>
        <button
          onClick={onBack}
          className="px-2 py-1 rounded bg-gray-200 text-gray-700
            hover:bg-gray-300 transition text-xs"
        >
          返回推荐
        </button>
      </div>

      {/* 导师列表：动态切换「卡片」/「评价组件」 */}
      <div className="space-y-4">
        {recommendations.map((professor) => {
          // 解构后端返回字段（含 match_score）
          const {
            name,
            university,
            department,
            url,
            tutor_id: tutorId,
            match_score: matchScore // 提取匹配度数值
          } = professor;

          // 若当前导师是「活跃评价」状态 → 渲染 TutorReview
          if (activeReviewTutorId === tutorId) {
            return (
              <TutorReview
                key={tutorId}
                tutorId={tutorId}
                onBack={handleBackToCard}
              />
            );
          }

          // 否则渲染「导师卡片」，优化匹配度展示
          return (
            <div
              key={tutorId}
              className="flex items-center justify-between
                p-3 bg-white/80 border border-gray-100 rounded-md
                hover:bg-white/90 transition-colors"
            >
              {/* 左侧信息区：姓名 + 匹配度 + 学校/院系 */}
              <div className="flex-1 space-y-1">
                {/* 姓名与匹配度一行展示（Flex 布局） */}
                <div className="flex items-center justify-between">
                  <h3 className="text-base font-semibold text-gray-900">
                    {name || '未知姓名'}
                  </h3>
                  {/* 🔴 匹配度标签样式优化：绿色背景 + 更大文字 + 加粗 + 饱满内边距 */}
                  <span
                    className="px-3 py-1 bg-green-500 text-white text-sm font-medium rounded-md"
                  >
                    匹配度：{matchScore || 0}
                  </span>
                </div>
                {/* 学校与院系信息 */}
                <p className="text-xs text-gray-500">
                  {university || '未知大学'} · {department || '未知院系'}
                </p>
              </div>

              {/* 右侧操作按钮区 */}
              <div className="flex flex-col space-y-2 ml-4">
                <button
                  onClick={() => handleViewDetails(url)}
                  className="px-2 py-1 rounded border border-blue-500 text-blue-500 
                    hover:bg-blue-500 hover:text-white transition text-xs"
                >
                  查看详情
                </button>
                <button
                  onClick={() => handleShowReview(tutorId)}
                  className="px-2 py-1 rounded bg-blue-500 text-white 
                    hover:bg-blue-600 transition text-xs"
                >
                  查看评价
                </button>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
};

export default RecommendationResult;