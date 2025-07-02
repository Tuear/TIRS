import React from 'react';
import Header from './Header';

const Layout = ({ children }) => {
  return (
    <div className="flex flex-col min-h-screen">
      <Header />
      <main className="flex-grow p-4">
        {children}
      </main>
      <footer className="bg-gray-800 text-white p-4">
        <div className="container mx-auto text-center">
          © 2025 基于评价的导师智能推荐系统
        </div>
      </footer>
    </div>
  );
};

export default Layout;