// components/admin/PlatformMonitor.jsx（完整代码）
import React, { useState, useEffect } from 'react';
import ReactECharts from 'echarts-for-react'; 
import { getPlatformStats } from '../../api/platformmonitorApi'; 

const PlatformMonitor = () => {
  const [stats, setStats] = useState(null);  
  const [loading, setLoading] = useState(false); 
  const [error, setError] = useState(null);  

  useEffect(() => {
    const fetchData = async () => {
      setLoading(true);
      setError(null);
      try {
        const data = await getPlatformStats();
        setStats(data);
      } catch (err) {
        setError(err.error);
      } finally {
        setLoading(false);
      }
    };
    fetchData();
  }, []);

  // 加载中状态
  if (loading) {
    return (
      <div className="p-4">
        <div className="flex items-center justify-center h-48">
          <div className="animate-spin rounded-full h-10 w-10 border-t-2 border-b-2 border-blue-500"></div>
        </div>
        <p className="text-center text-gray-500">加载平台数据中...</p>
      </div>
    );
  }

  // 错误状态
  if (error) {
    return (
      <div className="p-4">
        <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-4">
          <p>{error}</p>
        </div>
      </div>
    );
  }

  // 数据未加载完成（兜底）
  if (!stats) {
    return (
      <div className="p-4">
        <p className="text-center text-gray-500">数据加载中，请稍候...</p>
      </div>
    );
  }

  // 🔴 解析已用内存 + 计算总内存（512MB）、剩余内存
  const memoryUsed = stats?.memory_usage 
    ? parseInt(stats.memory_usage.match(/\d+/)[0], 10) 
    : 0;  
  const totalMemory = 512;  
  const memoryFree = totalMemory - memoryUsed;  


  // 🔴 饼图 ECharts 配置
  const chartOption = {
    tooltip: {
      trigger: 'item',
      formatter: '{a} <br/>{b}: {c} MB ({d}%)',
    },
    series: [
      {
        name: '内存占用',
        type: 'pie',
        radius: ['35%', '65%'],
        center: ['50%', '50%'],
        data: [
          { value: memoryUsed, name: '已使用' },
          { value: memoryFree, name: '剩余' },
        ],
        label: {
          show: true,
          formatter: '{b}: {d}%',
        },
        labelLine: {
          show: true,
        },
        itemStyle: {
          borderRadius: 8,
          borderColor: '#fff',
          borderWidth: 2,
        },
      },
    ],
  };  


  // 数据渲染：统计信息 + 饼图
  return (
    <div className="p-4">
      <h2 className="text-xl font-semibold mb-4">平台监控数据</h2>
      {/* 文本统计信息（网格布局） */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        <div className="bg-white p-4 rounded shadow">
          <p className="text-gray-700">评价总数</p>
          <p className="text-xl font-bold">{stats.review_count}</p>
        </div>
        <div className="bg-white p-4 rounded shadow">
          <p className="text-gray-700">学校总数</p>
          <p className="text-xl font-bold">{stats.schools.total}</p>
        </div>
        <div className="bg-white p-4 rounded shadow">
          <p className="text-gray-700">学院数量</p>
          <p className="text-xl font-bold">{stats.schools.departments}</p>
        </div>
        <div className="bg-white p-4 rounded shadow">
          <p className="text-gray-700">用户总数</p>
          <p className="text-xl font-bold">{stats.user_count}</p>
        </div>
      </div>

      {/* 🔴 内存占用饼图（调整高度） */}
      <div className="mt-8 bg-white p-4 rounded shadow">
        <h3 className="text-lg font-semibold mb-2">内存占用</h3>
        <div style={{ height: 300 }}>
          <ReactECharts 
            option={chartOption} 
            style={{ width: '100%', height: '100%' }} 
          />
        </div>
      </div>
    </div>
  );
};

export default PlatformMonitor;