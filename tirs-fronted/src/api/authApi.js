import axios from 'axios';
import config from '../Config'; // 导入配置文件

// 使用配置中的后端地址
const BASE_URL = config.API_BASE_URL;

/**
 * 用户注册
 * @param {Object} userData 用户数据 { user_id: string, password: string }
 * @returns Promise
 */
export const registerUser = async (userData) => {
  try {
    const response = await axios.post(`${BASE_URL}/auth/register`, {
      user_id: userData.userId,
      password: userData.password
    });
    return response.data;
  } catch (error) {
    // 根据文档中的异常处理设计
    const errorMessage = error.response?.data?.error || error.response?.data?.message || '注册失败，请重试';
    throw { error: errorMessage };
  }
};

/**
 * 用户登录
 * @param {Object} credentials 登录凭证 { user_id: string, password: string }
 * @returns Promise
 */
export const loginUser = async (credentials) => {
  try {
    const response = await axios.post(`${BASE_URL}/auth/login`, {
      user_id: credentials.user_id,
      password: credentials.password
    });
    
    // 根据文档中的响应格式
    return {
      message: response.data.message,
      role: response.data.role || 'user',
      user_id: response.data.user_id
    };
  } catch (error) {
    const errorMessage = error.response?.data?.error || error.response?.data?.message || '登录失败，请检查凭证';
    throw { error: errorMessage };
  }
};

/**
 * 管理员登录
 * @param {Object} credentials 登录凭证 { user_id: string, password: string }
 * @returns Promise
 */
export const loginAdmin = async (credentials) => {
  try {
    const response = await axios.post(`${BASE_URL}/auth/login`, {
      user_id: credentials.user_id,
      password: credentials.password
    });
    
    // 根据文档中的响应格式
    return {
      message: response.data.message,
      role: 'admin',
      admin_id: response.data.admin_id
    };
  } catch (error) {
    const errorMessage = error.response?.data?.error || error.response?.data?.message || '管理员登录失败';
    throw { error: errorMessage };
  }
};

/**
 * 退出登录
 * @returns Promise
 */
export const logout = async () => {
  try {
    const response = await axios.post(`${BASE_URL}/auth/logout`);
    return response.data;
  } catch (error) {
    console.error('退出失败:', error);
    const errorMessage = error.response?.data?.error || error.response?.data?.message || '退出失败';
    throw { error: errorMessage };
  }
};