import React from 'react';

const DashboardCard = ({ title, description, placeholder }) => {
  return (
    <div className="bg-white rounded-lg shadow-md p-6">
      <h3 className="text-lg font-bold mb-2">{title}</h3>
      <p className="text-gray-600 mb-4">{description}</p>
      <div className="text-sm text-gray-500">{placeholder}</div>
    </div>
  );
};

export default DashboardCard;