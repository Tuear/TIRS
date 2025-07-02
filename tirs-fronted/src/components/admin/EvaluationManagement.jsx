import React, { useEffect, useState } from 'react';
import { Table, Pagination, Button, message, Input } from 'antd'; // 新增导入 Input
import { getAllReviews, deleteReview } from '../../api/reviewmanageApi'; // 接口路径

const EvaluationManagement = () => {
  const [reviews, setReviews] = useState([]); // 原始全部评价数据
  const [filteredReviews, setFilteredReviews] = useState([]); // 筛选后的评价数据
  const [loading, setLoading] = useState(false); // 加载状态
  const [currentPage, setCurrentPage] = useState(1); // 当前页码
  const [searchKeyword, setSearchKeyword] = useState(''); // 搜索的用户名
  const [isSearching, setIsSearching] = useState(false); // 是否处于搜索状态
  const pageSize = 10; // 每页显示条数

  // ========== 1. 数据获取逻辑 ==========
  const fetchReviews = async () => {
    setLoading(true);
    try {
      const res = await getAllReviews();
      if (res.success) {
        setReviews(res.data); // 存储原始全量数据
        setFilteredReviews(res.data); // 初始为全量数据（未筛选）
        message.success('评价列表获取成功');
      } else {
        message.error(res.error || '获取评价列表失败');
        setReviews([]);
        setFilteredReviews([]);
      }
    } catch (error) {
      message.error(error.error || '网络请求失败');
      setReviews([]);
      setFilteredReviews([]);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchReviews();
  }, []); // 组件挂载时自动加载全量评价


  // ========== 2. 搜索与筛选逻辑 ==========
  /**
   * 点击“搜索”时：
   * 1. 过滤原始数据中 user_id 包含关键词的评价
   * 2. 重置分页到第1页
   */
  const handleSearch = () => {
    const keyword = searchKeyword.trim();
    if (!keyword) {
      message.warning('请输入有效的用户名');
      return;
    }
    // 前端过滤：保留 user_id 包含关键词的评价（可根据需求改为全等匹配）
    const filtered = reviews.filter(review => 
      review.user_id.includes(keyword)
    );
    setFilteredReviews(filtered);
    setIsSearching(true);
    setCurrentPage(1); // 搜索后回到第1页
  };

  /**
   * 点击“重置”时：
   * 1. 恢复为全量评价数据
   * 2. 清空搜索关键词、重置分页
   */
  const handleResetSearch = () => {
    setFilteredReviews(reviews); // 恢复全量数据
    setSearchKeyword('');
    setIsSearching(false);
    setCurrentPage(1); // 重置后回到第1页
  };


  // ========== 3. 删除操作逻辑（需兼容搜索状态） ==========
  const handleDelete = async (sentenceId) => {
    try {
      await deleteReview(sentenceId);
      message.success('评价删除成功');
      await fetchReviews(); // 重新拉取全量数据（确保数据最新）
      setIsSearching(false); // 重置搜索状态（回到全量数据）
      setFilteredReviews(reviews); // 恢复为全量数据
      setCurrentPage(1); // 回到第1页
    } catch (error) {
      message.error(error.error || '删除评价失败');
    }
  };


  // ========== 4. 分页逻辑（基于筛选后的数据） ==========
  const handlePageChange = (newPage) => {
    setCurrentPage(newPage);
  };

  // 前端模拟分页：从「筛选后的数据」中截取当前页内容
  const startIdx = (currentPage - 1) * pageSize;
  const endIdx = startIdx + pageSize;
  const currentPageData = filteredReviews.slice(startIdx, endIdx);


  // ========== 5. 表格列配置（保持原有列 + 新增“用户ID”列） ==========
  const columns = [
    {
      title: '评价ID',
      dataIndex: 'sentence_id',
      key: 'sentence_id',
      align: 'center',
    },
    {
      title: '评价用户ID', // 展示评价对应的用户名（依赖后端返回的 user_id 字段）
      dataIndex: 'user_id',
      key: 'user_id',
      align: 'center',
    },
    {
      title: '导师姓名',
      dataIndex: 'name',
      key: 'name',
      align: 'center',
    },
    {
      title: '学校',
      dataIndex: 'university',
      key: 'university',
      align: 'center',
    },
    {
      title: '学院/系',
      dataIndex: 'department',
      key: 'department',
      align: 'center',
    },
    {
      title: '评价内容',
      dataIndex: 'review_sentence',
      key: 'review_sentence',
      align: 'center',
    },
    {
      title: '操作',
      key: 'action',
      align: 'center',
      render: (_, record) => (
        <Button type="danger" onClick={() => handleDelete(record.sentence_id)}>
          删除
        </Button>
      ),
    },
  ];


  // ========== 6. 页面渲染（新增搜索区域） ==========
  return (
    <div style={{ padding: 24 }}>
      {/* 搜索区域：输入框 + 搜索按钮 + 重置按钮 */}
      <div style={{ marginBottom: 16, display: 'flex', gap: 8 }}>
        <Input 
          placeholder="请输入用户名筛选" 
          value={searchKeyword} 
          onChange={(e) => setSearchKeyword(e.target.value)} 
          allowClear // 显示“清空”按钮，提升体验
        />
        <Button type="primary" onClick={handleSearch}>搜索</Button>
        {isSearching && ( // 仅在搜索状态下显示“重置”按钮
          <Button onClick={handleResetSearch}>重置</Button>
        )}
      </div>

      {/* 评价表格（基于筛选后的数据渲染） */}
      <Table
        columns={columns}
        dataSource={currentPageData}
        loading={loading}
        rowKey="sentence_id"
        bordered
        pagination={false} // 关闭内置分页，用外部Pagination
        size="middle"
      />

      {/* 分页组件（总条数为「筛选后的数据长度」） */}
      <Pagination
        current={currentPage}
        pageSize={pageSize}
        total={filteredReviews.length} // 筛选后的数据总条数
        onChange={handlePageChange}
        style={{ marginTop: 16, textAlign: 'right' }}
        showQuickJumper // 快速跳转页码
      />
    </div>
  );
};

export default EvaluationManagement;