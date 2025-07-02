import React, { useState } from 'react';
import { updateProfessorInfo } from '../../api/ProfessorUpdateApi'; // 导入后端接口

const ProfessorInfoForm = () => {
  // 表单字段状态（与设计图字段一一对应）
  const [name, setName] = useState('');
  const [university, setUniversity] = useState('');
  const [college, setCollege] = useState('');
  const [academicBackground, setAcademicBackground] = useState('');
  const [responsibility, setResponsibility] = useState('');
  const [teacherEthics, setTeacherEthics] = useState('');
  const [officialUrl, setOfficialUrl] = useState('');
  const [feedback, setFeedback] = useState(''); // 提交结果反馈

  // 表单提交：收集数据 → 调用接口 → 处理响应/错误
  const handleSubmit = async (e) => {
    e.preventDefault();
    setFeedback(''); // 清空历史反馈

    try {
      // 映射后端接口参数（注意字段对应关系）
      const response = await updateProfessorInfo({
        name,
        university,
        department: college, // 「学院」对应后端参数department
        academic: academicBackground, // 「学术履历」对应后端参数academic
        responsibility,
        character: teacherEthics, // 「师德师风」对应后端参数character
        professor_url: officialUrl, // 「导师官网」对应后端参数professor_url
      });
      setFeedback(response.message); // 显示成功提示
      // 提交成功后重置表单
      setName('');
      setUniversity('');
      setCollege('');
      setAcademicBackground('');
      setResponsibility('');
      setTeacherEthics('');
      setOfficialUrl('');
    } catch (error) {
      setFeedback(error.error); // 显示错误原因（如权限不足、参数缺失）
    }
  };

  return (
    <form onSubmit={handleSubmit} className="flex flex-col md:flex-row gap-8">
      {/* 左侧：表单填写区（匹配设计图） */}
      <div className="flex-1 bg-white p-4 rounded-lg border border-blue-500">
        {/* 填写说明模块 */}
        <div className="bg-blue-50 p-3 rounded-md mb-4">
          <p className="text-sm font-medium text-blue-700 mb-1">填写说明：</p>
          <ul className="text-xs text-gray-600 list-disc pl-4">
            <li>请准确填写导师基本信息</li>
            <li>学术履历需包含教育背景、研究方向和重要成果</li>
            <li>官网URL应指向导师个人主页或实验室网站</li>
            <li>评价信息需要实事求是，公正客观</li>
          </ul>
        </div>

        {/* 输入项模块（按设计图顺序） */}
        <div className="space-y-4">
          {/* 姓名 */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">姓名</label>
            <input
              type="text"
              value={name}
              onChange={(e) => setName(e.target.value)}
              placeholder="请输入导师姓名"
              className="w-full px-3 py-2 border border-gray-300 rounded-md 
                         focus:outline-none focus:border-blue-500"
              required
            />
          </div>

          {/* 学校 */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">学校</label>
            <input
              type="text"
              value={university}
              onChange={(e) => setUniversity(e.target.value)}
              placeholder="请输入学校名称"
              className="w-full px-3 py-2 border border-gray-300 rounded-md 
                         focus:outline-none focus:border-blue-500"
              required
            />
          </div>

          {/* 学院 */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">学院</label>
            <input
              type="text"
              value={college}
              onChange={(e) => setCollege(e.target.value)}
              placeholder="请输入学院名称"
              className="w-full px-3 py-2 border border-gray-300 rounded-md 
                         focus:outline-none focus:border-blue-500"
              required
            />
          </div>

          {/* 学术履历与科研资源 */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">学术履历与科研资源</label>
            <input
              type="text"
              value={academicBackground}
              onChange={(e) => setAcademicBackground(e.target.value)}
              placeholder="请输入导师的学术履历与科研资源"
              className="w-full px-3 py-2 border border-gray-300 rounded-md 
                         focus:outline-none focus:border-blue-500"
              required
            />
          </div>

          {/* 责任意识 */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">责任意识</label>
            <input
              type="text"
              value={responsibility}
              onChange={(e) => setResponsibility(e.target.value)}
              placeholder="描述导师的责任意识"
              className="w-full px-3 py-2 border border-gray-300 rounded-md 
                         focus:outline-none focus:border-blue-500"
              required
            />
          </div>

          {/* 师德师风表现 */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">师德师风表现</label>
            <input
              type="text"
              value={teacherEthics}
              onChange={(e) => setTeacherEthics(e.target.value)}
              placeholder="描述导师的师德师风表现"
              className="w-full px-3 py-2 border border-gray-300 rounded-md 
                         focus:outline-none focus:border-blue-500"
              required
            />
          </div>

          {/* 导师官网URL */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">导师官网URL</label>
            <input
              type="url"
              value={officialUrl}
              onChange={(e) => setOfficialUrl(e.target.value)}
              placeholder="请输入导师个人主页或实验室官网URL"
              className="w-full px-3 py-2 border border-gray-300 rounded-md 
                         focus:outline-none focus:border-blue-500"
              required
            />
          </div>

          {/* 提交按钮 */}
          <button
            type="submit"
            className="bg-gradient-to-r from-blue-500 to-blue-700 text-white 
                       px-5 py-3 rounded-md hover:opacity-90 transition-opacity font-medium"
          >
            提交维护信息
          </button>

          {/* 操作反馈 */}
          {feedback && (
            <div className="text-sm text-gray-700 mt-2">
              {feedback}
            </div>
          )}
        </div>
      </div>

      {/* 右侧：信息预览区（实时同步左侧输入内容） */}
      <div className="flex-1 bg-white p-4 rounded-lg border border-gray-200">
        <h3 className="text-lg font-semibold text-gray-800 mb-4">信息预览</h3>
        <p className="text-sm text-gray-600 mb-2">以下为当前填写的导师信息预览：</p>
        <div className="bg-white rounded-lg shadow p-4">
          {/* 头像 + 基本信息 */}
          <div className="flex items-center mb-4">
            <div className="w-12 h-12 bg-blue-500 rounded-full flex items-center justify-center text-white text-xl font-bold">
              {name ? name[0] : '李'} {/* 显示姓名首字，无内容时默认“李” */}
            </div>
            <div className="ml-3">
              <h4 className="text-xl font-semibold text-gray-800">
                {name || '李教授'}
              </h4>
              <p className="text-gray-600">
                {university || '清华大学'} • {college || '计算机科学与技术学院'}
              </p>
            </div>
          </div>

          {/* 学术履历与科研资源 */}
          <div className="mb-4">
            <h5 className="text-base font-semibold text-gray-800 mb-1">学术履历与科研资源</h5>
            <p className="text-gray-600">
              {academicBackground || '计算机视觉领域专家，发表CVPR/ICCV论文30余篇，主持国家自然科学基金重点项目2项'}
            </p>
          </div>

          {/* 责任意识 */}
          <div className="mb-4">
            <h5 className="text-base font-semibold text-gray-800 mb-1">责任意识</h5>
            <p className="text-gray-600">
              {responsibility || '认真负责，每周固定组会，对学生的研究进展非常关心'}
            </p>
          </div>

          {/* 师德师风表现 */}
          <div className="mb-4">
            <h5 className="text-base font-semibold text-gray-800 mb-1">师德师风表现</h5>
            <p className="text-gray-600">
              {teacherEthics || '为人正直，尊重学生，学术严谨，从不要求学生做与学术无关的事务'}
            </p>
          </div>

          {/* 导师官网 */}
          <div>
            <h5 className="text-base font-semibold text-gray-800 mb-1">导师官网</h5>
            <a
              href={officialUrl || 'https://www.university.edu.cn/lab/li-professor'}
              target="_blank"
              rel="noopener noreferrer"
              className="text-blue-500 hover:underline"
            >
              {officialUrl || 'https://www.university.edu.cn/lab/li-professor'}
            </a>
          </div>
        </div>
      </div>
    </form>
  );
};

export default ProfessorInfoForm;