import axios from 'axios';
import config from '../Config'; 

const BASE_URL = config.API_BASE_URL;
// ==== 管理员评价管理接口 ====

/**
 * 获取所有用户评价
 * @returns Promise 返回评价列表数据
 */
export const getAllReviews = async () => {
  try {
    const response = await axios.get(`${BASE_URL}/admin/get_all_reviews`, {
      // 发送管理员凭证（根据后端要求可能需要）
      //withCredentials: true 
    });
    return response.data;
  } catch (error) {
    const errorMessage = error.response?.data?.error || '获取评价失败';
    throw { error: errorMessage };
  }
};

/**
 * 删除指定评价
 * @param {string} sentenceId 要删除的评价ID
 * @returns Promise
 */
export const deleteReview = async (sentenceId) => {
  try {
    const response = await axios.post(`${BASE_URL}/admin/delete_review`, 
      { sentence_id: sentenceId },
      //{ withCredentials: true }
    );
    return response.data;
  } catch (error) {
    let errorMessage = '删除评价失败';
    if (error.response?.data?.error) {
      errorMessage = error.response.data.error;
      // 处理特定错误类型
      if (errorMessage.includes("缺少评价ID参数")) {
        errorMessage = "请选择要删除的评价";
      }
    }
    throw { error: errorMessage };
  }
};

/**
 * 获取指定用户的完整信息及评价
 * @param {string} userId 要查询的用户ID
 * @returns Promise
 */
export const getUserInfoWithReviews = async (userId) => {
  try {
    const response = await axios.post(`${BASE_URL}/admin/handle_user_information`, 
      { user_id: userId },
      //{ withCredentials: true }
    );
    return response.data.user;
  } catch (error) {
    let errorMessage = '获取用户数据失败';
    
    // 处理特定错误类型
    if (error.response?.status === 403) {
      errorMessage = "权限不足，无法查看用户信息";
    } else if (error.response?.data?.error) {
      errorMessage = `获取数据失败: ${error.response.data.error}`;
    }
    
    throw { error: errorMessage };
  }
};