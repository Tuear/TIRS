import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { registerUser } from '../api/authApi';
import Input from '../components/ui/Input';
import Button from '../components/ui/Button';
import Alert from '../components/ui/Alert';
import Card from '../components/ui/Card';
import { Link } from 'react-router-dom';

const RegisterPage = () => {
  const [formData, setFormData] = useState({
    userId: '',
    password: '',
    confirmPassword: ''
  });
  const [error, setError] = useState('');
  const [success, setSuccess] = useState(false);
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: value }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (formData.password !== formData.confirmPassword) {
      setError('两次输入的密码不一致');
      return;
    }
    
    setLoading(true);
    setError('');
    
    try {
      await registerUser({
        userId: formData.userId,
        password: formData.password
      });
      
      setSuccess(true);
      // 3秒后自动跳转到登录页面
      setTimeout(() => navigate('/login'), 3000);
    } catch (err) {
      setError(err.error || '注册失败，请重试');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-100">
      <Card className="w-full max-w-md">
        <h2 className="text-2xl font-bold text-center mb-6">用户注册</h2>
        
        {success ? (
          <div className="text-center py-8">
            <div className="text-green-600 text-lg mb-4">注册成功！</div>
            <p>即将跳转到登录页面...</p>
          </div>
        ) : (
          <form onSubmit={handleSubmit} className="space-y-4">
            {error && <Alert type="error" message={error} />}
            
            <Input
              label="用户ID"
              name="userId"
              type="text"
              value={formData.userId}
              onChange={handleChange}
              required
            />
            
            <Input
              label="密码"
              name="password"
              type="password"
              value={formData.password}
              onChange={handleChange}
              required
            />
            
            <Input
              label="确认密码"
              name="confirmPassword"
              type="password"
              value={formData.confirmPassword}
              onChange={handleChange}
              required
            />
            
            <Button 
              type="submit" 
              disabled={loading}
              className="w-full"
            >
              {loading ? '注册中...' : '注册'}
            </Button>
          </form>
        )}
        
        <div className="mt-6 text-center">
          <span className="text-gray-600">已有账号？</span>
          <Link to="/login" className="text-blue-600 hover:underline ml-1">
            立即登录
          </Link>
        </div>
      </Card>
    </div>
  );
};

export default RegisterPage;