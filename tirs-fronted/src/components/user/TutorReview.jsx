import React, { useState, useEffect } from 'react';
import { getTutorInformation } from '../../api/show_informationApi'; 

const TutorReview = ({ tutorId, onBack }) => {
  const [reviewData, setReviewData] = useState({}); 
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    const fetchReviews = async () => {
      try {
        const response = await getTutorInformation(tutorId); 
        setReviewData(response || {}); 
        setIsLoading(false);
      } catch (error) {
        console.error('获取导师评价失败:', error);
        setReviewData({});
        setIsLoading(false);
      }
    };
    fetchReviews();
  }, [tutorId]);

  const { 
    name = '未知导师',        
    review_sentences = []    
  } = reviewData;

  return (
    <div 
      className="bg-gradient-to-b from-white/60 to-white/80 
        backdrop-blur-md border border-gray-100 rounded-xl shadow-md 
        p-4 space-y-4 relative"
    >
      <div className="flex justify-between items-center mb-3">
        <h3 className="text-base font-semibold text-gray-900">
          {name} 导师评价
        </h3>
        <button
          onClick={onBack} 
          className="px-2 py-1 rounded bg-gray-200 text-gray-700 
            hover:bg-gray-300 transition text-xs"
        >
          返回卡片
        </button>
      </div>

      {isLoading && (
        <div className="flex items-center justify-center h-20">
          <svg className="animate-spin h-6 w-6 text-gray-700" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
            <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
            <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
          </svg>
        </div>
      )}

      {!isLoading && review_sentences.length === 0 && (
        <div className="text-center text-xs text-gray-600">
          暂无该导师的公开评价
        </div>
      )}

      {!isLoading && review_sentences.length > 0 && (
        <div className="space-y-2 max-h-64 overflow-y-auto px-1"> 
        {/* 👇 核心调整：添加 max-h-64（最大高度256px） + overflow-y-auto（溢出滚动） */}
          {review_sentences.map((sentence, index) => (
            <div 
              key={index} 
              className="p-3 bg-white/80 border border-gray-100 rounded-md 
                hover:bg-white/90 transition-colors"
            >
              <p className="text-xs text-gray-700">
                评价 {index + 1}：{sentence}
              </p>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default TutorReview;