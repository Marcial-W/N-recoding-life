import React, { useState, useEffect } from 'react';
import { getRecords, saveRecord } from '../utils/storage';

function CreateRecord() {
  const [formData, setFormData] = useState({
    title: '',
    date: new Date().toISOString().split('T')[0],
    time: new Date().toLocaleTimeString('zh-CN', { hour12: false, hour: '2-digit', minute: '2-digit' }),
    location: '',
    description: '',
    category: '生活'
  });
  
  const [records, setRecords] = useState([]);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [selectedRecord, setSelectedRecord] = useState(null);

  const categories = [
    { name: '生活', icon: 'home', color: 'from-blue-400 to-blue-600' },
    { name: '工作', icon: 'briefcase', color: 'from-green-400 to-green-600' },
    { name: '学习', icon: 'book-open', color: 'from-purple-400 to-purple-600' },
    { name: '旅行', icon: 'map-pin', color: 'from-orange-400 to-orange-600' },
    { name: '美食', icon: 'utensils', color: 'from-red-400 to-red-600' },
    { name: '运动', icon: 'activity', color: 'from-teal-400 to-teal-600' },
    { name: '创作', icon: 'palette', color: 'from-pink-400 to-pink-600' },
    { name: '其他', icon: 'more-horizontal', color: 'from-gray-400 to-gray-600' }
  ];

  useEffect(() => {
    setRecords(getRecords());
  }, []);

  try {
    const handleSubmit = async (e) => {
      e.preventDefault();
      setIsSubmitting(true);
      
      const record = {
        ...formData,
        id: Date.now().toString(),
        createdAt: new Date().toISOString()
      };

      await saveRecord(record);
      setRecords(getRecords());
      
      // 重置表单
      setFormData({
        title: '',
        date: new Date().toISOString().split('T')[0],
        time: new Date().toLocaleTimeString('zh-CN', { hour12: false, hour: '2-digit', minute: '2-digit' }),
        location: '',
        description: '',
        category: '生活'
      });

      setTimeout(() => setIsSubmitting(false), 500);
    };

    const getCategoryIcon = (categoryName) => {
      return categories.find(cat => cat.name === categoryName)?.icon || 'circle';
    };

    const getCategoryColor = (categoryName) => {
      return categories.find(cat => cat.name === categoryName)?.color || 'from-gray-400 to-gray-600';
    };

    return (
      <div className="py-6 space-y-6" data-name="create-record" data-file="components/CreateRecord.js">
        <div className="text-center">
          <div className="inline-flex items-center justify-center w-16 h-16 gradient-primary rounded-3xl mb-4">
            <div className="icon-plus text-2xl text-white"></div>
          </div>
          <h1 className="text-3xl font-bold bg-gradient-to-r from-gray-900 to-gray-600 bg-clip-text text-transparent">
            创建新记录
          </h1>
          <p className="text-gray-500 mt-2">记录生活中的美好瞬间</p>
        </div>
        
        <form onSubmit={handleSubmit} className="card space-y-6">
          <div className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">事件名称</label>
              <input
                type="text"
                placeholder="今天发生了什么有趣的事..."
                className="input-field"
                value={formData.title}
                onChange={(e) => setFormData({...formData, title: e.target.value})}
                required
              />
            </div>
            
            <div className="grid grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">日期</label>
                <input
                  type="date"
                  className="input-field"
                  value={formData.date}
                  onChange={(e) => setFormData({...formData, date: e.target.value})}
                  required
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">时间</label>
                <input
                  type="time"
                  className="input-field"
                  value={formData.time}
                  onChange={(e) => setFormData({...formData, time: e.target.value})}
                  required
                />
              </div>
            </div>
            
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">地点</label>
              <input
                type="text"
                placeholder="在哪里发生的..."
                className="input-field"
                value={formData.location}
                onChange={(e) => setFormData({...formData, location: e.target.value})}
              />
            </div>
            
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">分类</label>
              <div className="grid grid-cols-4 gap-2">
                {categories.map(category => (
                  <button
                    key={category.name}
                    type="button"
                    onClick={() => setFormData({...formData, category: category.name})}
                    className={`p-3 rounded-xl border-2 transition-all ${
                      formData.category === category.name 
                        ? 'border-purple-400 bg-purple-50' 
                        : 'border-gray-200 bg-white hover:border-purple-200'
                    }`}
                  >
                    <div className={`icon-${category.icon} text-lg mb-1 ${formData.category === category.name ? 'text-purple-500' : 'text-gray-500'}`}></div>
                    <div className="text-xs font-medium">{category.name}</div>
                  </button>
                ))}
              </div>
            </div>
            
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">详细描述</label>
              <textarea
                placeholder="详细描述一下发生了什么..."
                className="input-field"
                rows="4"
                value={formData.description}
                onChange={(e) => setFormData({...formData, description: e.target.value})}
              />
            </div>
          </div>
          
          <button
            type="submit"
            disabled={isSubmitting}
            className={`btn btn-primary w-full ${isSubmitting ? 'opacity-60' : ''}`}
          >
            {isSubmitting ? '保存中...' : '保存记录'}
          </button>
        </form>
        
        {records.length > 0 && (
          <div className="card">
            <h3 className="text-lg font-semibold text-gray-800 mb-4 flex items-center">
              <div className="icon-list text-lg mr-2 text-blue-500"></div>
              最近记录
            </h3>
            <div className="space-y-3">
              {records.slice(-3).reverse().map(record => (
                <div
                  key={record.id}
                  className="record-card"
                  onClick={() => setSelectedRecord(record)}
                >
                  <div className="flex items-start justify-between">
                    <div className="flex-1">
                      <div className="flex items-center mb-2">
                        <div className={`w-8 h-8 rounded-lg bg-gradient-to-br ${getCategoryColor(record.category)} flex items-center justify-center mr-3`}>
                          <div className={`icon-${getCategoryIcon(record.category)} text-white text-sm`}></div>
                        </div>
                        <div>
                          <h4 className="font-semibold text-gray-800">{record.title}</h4>
                          <p className="text-sm text-gray-500">{record.date} {record.time}</p>
                        </div>
                      </div>
                      {record.location && (
                        <p className="text-sm text-gray-600 flex items-center">
                          <div className="icon-map-pin text-xs mr-1"></div>
                          {record.location}
                        </p>
                      )}
                      {record.description && (
                        <p className="text-sm text-gray-600 mt-2 line-clamp-2">{record.description}</p>
                      )}
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}
      </div>
    );
  } catch (error) {
    console.error('CreateRecord component error:', error);
    return null;
  }
}

export default CreateRecord;
