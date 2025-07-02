import axios from 'axios';
import config from '../Config'; // 导入配置文件

// 使用配置中的后端地址
const BASE_URL = config.API_BASE_URL;

/**
 * 获取平台监控数据
 * @returns Promise 包含平台监控数据的对象
 */
export const getPlatformStats = async () => {
  try {
    const response = await axios.get(`${BASE_URL}/admin/handle_platform_stats`);
    
    // 格式化响应数据（根据文档中的响应参数结构）
    return {
      memory_usage: response.data.memory_usage,
      review_count: response.data.review_count,
      schools: {
        departments: response.data.schools.departments,
        total: response.data.schools.total
      },
      user_count: response.data.user_count
    };
  } catch (error) {
    // 根据文档中的异常处理设计
    let errorMessage = '获取平台统计数据失败';
    
    if (error.response) {
      if (error.response.status === 403) {
        errorMessage = '权限不足';
      } else if (error.response.data?.error) {
        // 提取服务器返回的具体错误信息
        errorMessage = error.response.data.error;
      }
    }
    
    throw { error: errorMessage };
  }
};