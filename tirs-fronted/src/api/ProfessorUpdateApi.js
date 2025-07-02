import axios from 'axios';
import config from '../Config'; // 导入配置文件

// 使用配置中的后端地址
const BASE_URL = config.API_BASE_URL;

/**
 * 导师信息维护（新增/更新）
 * @param {Object} professorData 导师信息 { name: string, university: string, department: string, academic: string, responsibility: string, character: string, professor_url: string }
 * @returns Promise<{ message: string }>
 */
export const updateProfessorInfo = async (professorData) => {
  try {
    const response = await axios.post(`${BASE_URL}/admin/professor_update`, {
      // 严格映射后端要求的请求参数
      name: professorData.name,
      university: professorData.university,
      department: professorData.department,
      academic: professorData.academic,
      responsibility: professorData.responsibility,
      character: professorData.character,
      professor_url: professorData.professor_url
    });
    return response.data; // 响应格式：{ message: "操作成功" }
  } catch (error) {
    // 异常场景处理：优先取后端返回的错误信息，否则兜底
    const errorMessage = error.response?.data?.error || error.response?.data?.message || '提交导师信息失败，请重试';
    throw { error: errorMessage };
  }
};