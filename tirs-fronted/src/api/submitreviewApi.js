import axios from 'axios';
import config from '../Config'; // 复用项目配置文件（与原接口保持相同路径逻辑）

// 复用配置中的后端基础地址
const BASE_URL = config.API_BASE_URL;

/**
 * 学生提交导师评价
 * @param {Object} reviewData 评价信息（需严格匹配后端请求参数格式）
 *  @param {string} reviewData.name - 导师姓名
 *  @param {string} reviewData.university - 所属院校
 *  @param {string} reviewData.department - 所属院系
 *  @param {string} reviewData.academic - 学术方向
 *  @param {string} reviewData.responsibility - 指导职责
 *  @param {string} reviewData.character - 个人特质
 *  @param {string} reviewData.user_id - 当前用户ID
 * @returns Promise<{ message: string }>
 *  - 成功：返回后端响应的 { message: "提交成功" } 格式数据
 *  - 失败：抛出 { error: "错误信息" }（包含后端返回或兜底文案）
 */
export const submitReview = async (reviewData) => {
  try {
    // 发起 POST 请求，严格映射后端要求的请求体参数
    const response = await axios.post(
      `${BASE_URL}/user/submit_review`,
      {
        name: reviewData.name,
        university: reviewData.university,
        department: reviewData.department,
        academic: reviewData.academic,
        responsibility: reviewData.responsibility,
        character: reviewData.character,
        user_id: reviewData.user_id
      }
    );
    return response.data; // 成功时返回后端响应的 message
  } catch (error) {
    // 异常处理：优先读取后端返回的 error/message，否则兜底
    const errorMessage =
      error.response?.data?.error ||
      error.response?.data?.message ||
      '提交评价失败，请重试';
    throw { error: errorMessage };
  }
};