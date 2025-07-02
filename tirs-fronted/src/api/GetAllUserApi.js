import axios from 'axios';
import config from '../Config'; 

const BASE_URL = config.API_BASE_URL;

/**
 * 获取所有用户信息（打开 withCredentials 确保会话验证）
 * @returns Promise 包含用户列表数据的对象
 */
export const getAllUsers = async () => {
  try {
    const response = await axios.get(`${BASE_URL}/admin/get_all_users`, {
      //withCredentials: true, // 必须打开！管理员权限验证依赖会话 Cookie
    });
    return response.data;
  } catch (error) {
    const errorMessage = error.response?.data?.error ||
                         error.response?.data?.message ||
                         '获取用户信息失败，请稍后重试';
    throw { error: errorMessage };
  }
};

/**
 * 切换用户评价权限
 * @param {Object} data 请求参数 {
 *   target_user: string  // 目标用户名
 * }
 * @returns Promise 返回操作结果消息
 * @throws 抛出包含错误信息的对象
 */
export const toggleUserPermission = async (data) => {
  try {
    const response = await axios.post(`${BASE_URL}/admin/toggle_permission`, {
      target_user: data.target_user,
      enable: data.enable,
    });
    return response.data.message; // 返回成功消息
  } catch (error) {
    // 统一错误处理
    let errorMessage = '切换权限失败，请稍后重试';
    
    if (error.response) {
      // 根据状态码处理不同错误类型
      switch (error.response.status) {
        case 400:
          errorMessage = error.response.data.error || '请求参数错误';
          break;
        case 403:
          errorMessage = '权限不足';
          break;
        case 500:
          errorMessage = `服务器错误: ${error.response.data.error?.split(':')[1] || '未知错误'}`;
          break;
        default:
          errorMessage = error.response.data.error || `请求失败: ${error.response.status}`;
      }
    } else if (error.request) {
      errorMessage = '请求未响应，请检查网络连接';
    }
    
    throw { error: errorMessage };
  }
};