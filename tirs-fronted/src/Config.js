const config = {
  development: {
    API_BASE_URL: 'http://127.0.0.1:5000',
    // 其他开发环境配置...
  },
  production: {
    API_BASE_URL: 'https://your-production-api.com',
    // 其他生产环境配置...
  }
};

export default config[process.env.NODE_ENV] || config.development;
