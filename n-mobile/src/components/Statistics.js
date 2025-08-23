import React, { useState, useEffect } from 'react';
import { getRecords } from '../utils/storage';

function Statistics() {
  const [records, setRecords] = useState([]);
  const [timeRange, setTimeRange] = useState('month');
  const [chartData, setChartData] = useState(null);

  useEffect(() => {
    setRecords(getRecords());
  }, []);

  useEffect(() => {
    if (records.length > 0) {
      generateChartData();
    }
  }, [records, timeRange]);

  const generateChartData = () => {
    const now = new Date();
    const filteredRecords = records.filter(record => {
      const recordDate = new Date(record.date);
      
      switch (timeRange) {
        case 'week':
          return (now - recordDate) / (1000 * 60 * 60 * 24) <= 7;
        case 'month':
          return recordDate.getMonth() === now.getMonth() && recordDate.getFullYear() === now.getFullYear();
        case 'year':
          return recordDate.getFullYear() === now.getFullYear();
        default:
          return true;
      }
    });

    // 按分类统计
    const categoryStats = {};
    filteredRecords.forEach(record => {
      categoryStats[record.category] = (categoryStats[record.category] || 0) + 1;
    });

    setChartData({
      categories: Object.keys(categoryStats),
      counts: Object.values(categoryStats),
      total: filteredRecords.length
    });
  };

  const getCategoryColor = (index) => {
    const colors = [
      '#6366f1', '#10b981', '#f59e0b', '#ef4444', 
      '#8b5cf6', '#06b6d4', '#f97316', '#84cc16'
    ];
    return colors[index % colors.length];
  };

  const getMaxCount = () => {
    if (!chartData || chartData.counts.length === 0) return 1;
    return Math.max(...chartData.counts);
  };

  return (
    <div className="py-6 space-y-6">
      <div className="text-center">
        <div className="inline-flex items-center justify-center w-16 h-16 gradient-primary rounded-3xl mb-4">
          <div className="icon-bar-chart-3 text-2xl text-white"></div>
        </div>
        <h1 className="text-3xl font-bold bg-gradient-to-r from-gray-900 to-gray-600 bg-clip-text text-transparent">
          数据统计
        </h1>
        <p className="text-gray-500 mt-2">查看你的生活记录分析</p>
      </div>

      <div className="card">
        <div className="flex items-center justify-between mb-6">
          <h3 className="text-lg font-semibold text-gray-800 flex items-center">
            <div className="icon-calendar text-lg mr-2 text-blue-500"></div>
            时间范围
          </h3>
          <div className="flex bg-gray-100 rounded-xl p-1">
            {[
              { value: 'week', label: '本周' },
              { value: 'month', label: '本月' },
              { value: 'year', label: '今年' }
            ].map(range => (
              <button
                key={range.value}
                onClick={() => setTimeRange(range.value)}
                className={`px-4 py-2 rounded-lg text-sm font-medium transition-all ${
                  timeRange === range.value
                    ? 'bg-white text-blue-600 shadow-sm'
                    : 'text-gray-600 hover:text-gray-800'
                }`}
              >
                {range.label}
              </button>
            ))}
          </div>
        </div>

        <div className="grid grid-cols-3 gap-4 mb-6">
          <div className="stats-metric">
            <div className="text-2xl font-bold text-blue-500 mb-1">{chartData?.total || 0}</div>
            <div className="text-sm text-gray-500">记录数</div>
          </div>
          <div className="stats-metric">
            <div className="text-2xl font-bold text-green-500 mb-1">{chartData?.categories.length || 0}</div>
            <div className="text-sm text-gray-500">类别数</div>
          </div>
          <div className="stats-metric">
            <div className="text-2xl font-bold text-purple-500 mb-1">{records.length}</div>
            <div className="text-sm text-gray-500">总计</div>
          </div>
        </div>

        {chartData && chartData.categories.length > 0 ? (
          <div>
            <h4 className="text-lg font-semibold text-gray-800 mb-4 flex items-center">
              <div className="icon-pie-chart text-lg mr-2 text-purple-500"></div>
              分类分布
            </h4>
            
            {/* 简化的柱状图 */}
            <div className="space-y-3 mb-6">
              {chartData.categories.map((category, index) => {
                const count = chartData.counts[index];
                const percentage = (count / chartData.total * 100).toFixed(1);
                const barWidth = (count / getMaxCount() * 100).toFixed(1);
                
                return (
                  <div key={category} className="space-y-2">
                    <div className="flex items-center justify-between text-sm">
                      <div className="flex items-center">
                        <div 
                          className="w-3 h-3 rounded-full mr-2"
                          style={{backgroundColor: getCategoryColor(index)}}
                        ></div>
                        <span className="text-gray-600 font-medium">{category}</span>
                      </div>
                      <div className="flex items-center space-x-2">
                        <span className="text-gray-800 font-medium">{count}</span>
                        <span className="text-gray-500 text-xs">({percentage}%)</span>
                      </div>
                    </div>
                    <div className="w-full bg-gray-200 rounded-full h-2">
                      <div 
                        className="h-2 rounded-full transition-all duration-500"
                        style={{
                          width: `${barWidth}%`,
                          backgroundColor: getCategoryColor(index)
                        }}
                      ></div>
                    </div>
                  </div>
                );
              })}
            </div>

            {/* 饼图效果 */}
            <div className="grid grid-cols-2 gap-4">
              {chartData.categories.map((category, index) => (
                <div key={category} className="flex items-center p-3 bg-gray-50 rounded-xl">
                  <div 
                    className="w-4 h-4 rounded-full mr-3"
                    style={{backgroundColor: getCategoryColor(index)}}
                  ></div>
                  <div className="flex-1">
                    <div className="text-sm font-medium text-gray-800">{category}</div>
                    <div className="text-xs text-gray-500">{chartData.counts[index]} 条记录</div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        ) : (
          <div className="text-center py-12">
            <div className="icon-bar-chart-3 text-6xl text-gray-300 mb-4"></div>
            <p className="text-gray-500 text-lg">暂无数据</p>
            <p className="text-gray-400 text-sm">快去创建你的第一条记录吧！</p>
          </div>
        )}
      </div>

      <div className="card">
        <h3 className="text-lg font-semibold text-gray-800 mb-4 flex items-center">
          <div className="icon-map-pin text-lg mr-2 text-red-500"></div>
          热门地点
        </h3>
        {records.length > 0 ? (
          <div className="space-y-3">
            {Object.entries(
              records.reduce((acc, record) => {
                if (record.location) {
                  acc[record.location] = (acc[record.location] || 0) + 1;
                }
                return acc;
              }, {})
            )
            .sort(([,a], [,b]) => b - a)
            .slice(0, 5)
            .map(([location, count], index) => (
              <div key={location} className="flex items-center justify-between p-3 bg-gradient-to-r from-gray-50 to-white rounded-xl border border-gray-100">
                <div className="flex items-center">
                  <div className="w-8 h-8 rounded-lg bg-red-100 flex items-center justify-center mr-3">
                    <span className="text-red-500 font-bold text-sm">#{index + 1}</span>
                  </div>
                  <span className="text-gray-800 font-medium">{location}</span>
                </div>
                <div className="flex items-center">
                  <span className="text-gray-500 text-sm mr-2">{count}次</span>
                  <div className="w-2 h-2 rounded-full bg-red-400"></div>
                </div>
              </div>
            ))}
          </div>
        ) : (
          <div className="text-center py-8">
            <div className="icon-map-pin text-4xl text-gray-300 mb-2"></div>
            <p className="text-gray-500">暂无地点数据</p>
          </div>
        )}
      </div>

      <div className="card">
        <h3 className="text-lg font-semibold text-gray-800 mb-4 flex items-center">
          <div className="icon-clock text-lg mr-2 text-blue-500"></div>
          记录趋势
        </h3>
        {records.length > 0 ? (
          <div className="space-y-4">
            {/* 最近7天的记录趋势 */}
            <div>
              <h4 className="text-sm font-medium text-gray-700 mb-3">最近7天</h4>
              <div className="flex items-end space-x-1 h-20">
                {Array.from({length: 7}, (_, i) => {
                  const date = new Date();
                  date.setDate(date.getDate() - (6 - i));
                  const dateStr = date.toISOString().split('T')[0];
                  const dayRecords = records.filter(r => r.date === dateStr);
                  const height = dayRecords.length > 0 ? (dayRecords.length / Math.max(...Array.from({length: 7}, (_, j) => {
                    const d = new Date();
                    d.setDate(d.getDate() - (6 - j));
                    return records.filter(r => r.date === d.toISOString().split('T')[0]).length;
                  })) * 100) : 0;
                  
                  return (
                    <div key={i} className="flex-1 flex flex-col items-center">
                      <div 
                        className="w-full bg-blue-500 rounded-t transition-all duration-300"
                        style={{height: `${Math.max(height, 5)}%`}}
                      ></div>
                      <div className="text-xs text-gray-500 mt-1">
                        {date.getDate()}
                      </div>
                    </div>
                  );
                })}
              </div>
            </div>
          </div>
        ) : (
          <div className="text-center py-8">
            <div className="icon-clock text-4xl text-gray-300 mb-2"></div>
            <p className="text-gray-500">暂无趋势数据</p>
          </div>
        )}
      </div>
    </div>
  );
}

export default Statistics;
