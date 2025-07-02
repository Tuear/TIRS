import axios from 'axios';
import config from '../Config'; // 导入项目配置文件（与原代码保持一致的路径逻辑）

// 使用配置中的后端基础地址
const BASE_URL = config.API_BASE_URL;

/**
 * 查看指定导师评价
 * @param {string} tutorId 导师 ID（需传递给后端的 tutor_id 参数）
 * @returns Promise<{ 
 *   department: string, 
 *   name: string, 
 *   review_features: Array, 
 *   review_sentences: Array, 
 *   tutor_id: string, 
 *   university: string 
 * } | { error: string }>
 *  - 成功：返回后端定义的导师评价信息结构
 *  - 失败：抛出 { error: "错误信息" }（包含后端返回或兜底的错误文案）
 */
export const getTutorInformation = async (tutorId) => {
  try {
    // 发起 POST 请求，严格映射后端要求的参数格式
    const response = await axios.post(
      `${BASE_URL}/user/show_information`, 
      { tutor_id: tutorId } // 请求体参数：{ "tutor_id": "string" }
    );
    return response.data; // 成功时直接返回后端响应的导师信息
  } catch (error) {
    // 异常处理：优先取后端返回的 error 信息，否则用兜底文案
    const errorMessage = 
      error.response?.data?.error || 
      error.response?.data?.message || 
      '查看导师评价失败，请重试';
    throw { error: errorMessage };
  }
};