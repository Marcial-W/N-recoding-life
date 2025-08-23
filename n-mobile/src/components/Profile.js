import React, { useState, useEffect } from 'react';
import { getRecords, clearAllRecords } from '../utils/storage';

function Profile() {
  const [records, setRecords] = useState([]);
  const [showExportData, setShowExportData] = useState(false);
  const [exportType, setExportType] = useState('json');
  const [isExporting, setIsExporting] = useState(false);

  useEffect(() => {
    setRecords(getRecords());
  }, []);

  const handleExportData = () => {
    setShowExportData(true);
  };

  const downloadBlob = (blob, filename) => {
    const url = URL.createObjectURL(blob);
    const linkElement = document.createElement('a');
    linkElement.href = url;
    linkElement.download = filename;
    document.body.appendChild(linkElement);
    linkElement.click();
    document.body.removeChild(linkElement);
    URL.revokeObjectURL(url);
  };

  const exportAsJSON = () => {
    const dataStr = JSON.stringify(records, null, 2);
    const blob = new Blob([dataStr], { type: 'application/json;charset=utf-8' });
    const filename = `生活记录_${new Date().toISOString().split('T')[0]}.json`;
    downloadBlob(blob, filename);
  };

  const escapeCSV = (value) => {
    if (value === null || value === undefined) return '';
    const str = String(value);
    if (/[",\n]/.test(str)) {
      return '"' + str.replace(/"/g, '""') + '"';
    }
    return str;
  };

  const convertToCSV = (rows) => {
    const headers = ['id','title','date','time','location','description','category','createdAt'];
    const csvRows = [headers.join(',')];
    rows.forEach(r => {
      const line = [
        r.id,
        r.title,
        r.date,
        r.time,
        r.location,
        r.description,
        r.category,
        r.createdAt
      ].map(escapeCSV).join(',');
      csvRows.push(line);
    });
    return csvRows.join('\n');
  };

  const exportAsCSV = () => {
    const csv = convertToCSV(records);
    const blob = new Blob([csv], { type: 'text/csv;charset=utf-8' });
    const filename = `生活记录_${new Date().toISOString().split('T')[0]}.csv`;
    downloadBlob(blob, filename);
  };

  const exportAsZIP = async () => {
    const JSZipLib = window.JSZip || window.jszip || window.JSZipLib;
    if (!JSZipLib) {
      alert('未找到 JSZip 库，无法导出 ZIP');
      return;
    }
    const zip = new JSZipLib();
    const jsonContent = JSON.stringify(records, null, 2);
    const csvContent = convertToCSV(records);
    const dateStr = new Date().toISOString().split('T')[0];
    zip.file(`records_${dateStr}.json`, jsonContent);
    zip.file(`records_${dateStr}.csv`, csvContent);
    const blob = await zip.generateAsync({ type: 'blob' });
    const filename = `生活记录_${dateStr}.zip`;
    downloadBlob(blob, filename);
  };

  const confirmExport = async () => {
    if (!records || records.length === 0) {
      alert('当前没有可导出的数据');
      return;
    }
    setIsExporting(true);
    try {
      if (exportType === 'json') {
        exportAsJSON();
      } else if (exportType === 'csv') {
        exportAsCSV();
      } else if (exportType === 'zip') {
        await exportAsZIP();
      }
    } catch (e) {
      console.error('导出失败:', e);
      alert('导出失败，请重试');
    } finally {
      setIsExporting(false);
      setShowExportData(false);
    }
  };

  const handleClearData = () => {
    if (window.confirm('确定要清除所有数据吗？此操作不可恢复！')) {
      clearAllRecords();
      setRecords([]);
      alert('数据已清除');
    }
  };

  const getFirstRecordDate = () => {
    if (records.length === 0) return '暂无记录';
    const sortedRecords = [...records].sort((a, b) => new Date(a.date) - new Date(b.date));
    return sortedRecords[0].date;
  };

  const getTotalDays = () => {
    if (records.length === 0) return 0;
    const dates = [...new Set(records.map(r => r.date))];
    return dates.length;
  };

  return (
    <div className="py-6 space-y-6">
      <div className="text-center">
        <div className="inline-flex items-center justify-center w-16 h-16 gradient-primary rounded-3xl mb-4">
          <div className="icon-user text-2xl text-white"></div>
        </div>
        <h1 className="text-3xl font-bold bg-gradient-to-r from-gray-900 to-gray-600 bg-clip-text text-transparent">
          个人中心
        </h1>
        <p className="text-gray-500 mt-2">管理你的应用设置</p>
      </div>

      <div className="card">
        <div className="flex items-center mb-6">
          <div className="w-20 h-20 gradient-primary rounded-3xl flex items-center justify-center mr-4 shadow-lg">
            <div className="icon-book-open text-3xl text-white"></div>
          </div>
          <div className="flex-1">
            <h3 className="text-xl font-bold text-gray-800">N - 生活记录</h3>
            <div className="text-gray-500 text-sm flex items-center mt-1">
              <div className="icon-calendar text-xs mr-1"></div>
              开始记录：{getFirstRecordDate()}
            </div>
            <div className="flex items-center mt-1">
              <div className="w-2 h-2 bg-green-400 rounded-full mr-2 animate-pulse"></div>
              <span className="text-green-600 text-xs font-medium">正在记录中</span>
            </div>
          </div>
        </div>

        <div className="grid grid-cols-3 gap-4">
          <div className="stats-metric">
            <div className="text-2xl font-bold text-purple-500 mb-1">{records.length}</div>
            <div className="text-sm text-gray-500">总记录</div>
            <div className="w-full bg-purple-100 rounded-full h-1 mt-2">
              <div className="bg-purple-500 h-1 rounded-full" style={{width: '75%'}}></div>
            </div>
          </div>
          <div className="stats-metric">
            <div className="text-2xl font-bold text-blue-500 mb-1">{getTotalDays()}</div>
            <div className="text-sm text-gray-500">记录天数</div>
            <div className="w-full bg-blue-100 rounded-full h-1 mt-2">
              <div className="bg-blue-500 h-1 rounded-full" style={{width: '60%'}}></div>
            </div>
          </div>
          <div className="stats-metric">
            <div className="text-2xl font-bold text-green-500 mb-1">
              {records.length > 0 ? (records.length / getTotalDays()).toFixed(1) : '0'}
            </div>
            <div className="text-sm text-gray-500">日均记录</div>
            <div className="w-full bg-green-100 rounded-full h-1 mt-2">
              <div className="bg-green-500 h-1 rounded-full" style={{width: '85%'}}></div>
            </div>
          </div>
        </div>
      </div>

      {showExportData && (
        <div className="card bg-gradient-to-br from-white to-gray-50">
          <div className="mb-3 font-semibold text-gray-800">选择导出类型</div>
          <div className="grid grid-cols-3 gap-3">
            <button
              type="button"
              onClick={() => setExportType('json')}
              className={`p-3 rounded-2xl border-2 transition-all ${exportType === 'json' ? 'border-purple-400 bg-purple-50' : 'border-gray-200 bg-white hover:border-purple-200'}`}
            >
              <div className="icon-file-text text-lg mb-1 text-purple-500"></div>
              <div className="text-sm">JSON</div>
            </button>
            <button
              type="button"
              onClick={() => setExportType('csv')}
              className={`p-3 rounded-2xl border-2 transition-all ${exportType === 'csv' ? 'border-purple-400 bg-purple-50' : 'border-gray-200 bg-white hover:border-purple-200'}`}
            >
              <div className="icon-table text-lg mb-1 text-blue-500"></div>
              <div className="text-sm">CSV</div>
            </button>
            <button
              type="button"
              onClick={() => setExportType('zip')}
              className={`p-3 rounded-2xl border-2 transition-all ${exportType === 'zip' ? 'border-purple-400 bg-purple-50' : 'border-gray-200 bg-white hover:border-purple-200'}`}
            >
              <div className="icon-file-archive text-lg mb-1 text-amber-500"></div>
              <div className="text-sm">ZIP</div>
            </button>
          </div>
          <div className="flex items-center gap-3 mt-4">
            <button
              onClick={confirmExport}
              disabled={isExporting}
              className={`btn btn-primary flex-1 ${isExporting ? 'opacity-60' : ''}`}
            >
              {isExporting ? '导出中...' : '开始导出'}
            </button>
            <button
              onClick={() => setShowExportData(false)}
              className="btn btn-secondary flex-1"
            >
              取消
            </button>
          </div>
        </div>
      )}

      <div className="space-y-3">
        <button
          onClick={handleExportData}
          className="w-full bg-gradient-to-r from-white to-blue-50 p-4 rounded-2xl border border-blue-100 hover:border-blue-200 transition-all duration-300 hover:shadow-lg group"
        >
          <div className="flex items-center justify-between">
            <div className="flex items-center">
              <div className="w-12 h-12 bg-blue-100 rounded-2xl flex items-center justify-center mr-4 group-hover:scale-110 transition-transform">
                <div className="icon-download text-xl text-blue-600"></div>
              </div>
              <div className="text-left">
                <div className="font-semibold text-gray-800">导出数据</div>
                <div className="text-sm text-gray-500">备份你的所有记录</div>
              </div>
            </div>
            <div className="icon-chevron-right text-blue-400 group-hover:translate-x-1 transition-transform"></div>
          </div>
        </button>

        <button
          onClick={handleClearData}
          className="w-full bg-gradient-to-r from-white to-red-50 p-4 rounded-2xl border border-red-100 hover:border-red-200 transition-all duration-300 hover:shadow-lg group"
        >
          <div className="flex items-center justify-between">
            <div className="flex items-center">
              <div className="w-12 h-12 bg-red-100 rounded-2xl flex items-center justify-center mr-4 group-hover:scale-110 transition-transform">
                <div className="icon-trash-2 text-xl text-red-600"></div>
              </div>
              <div className="text-left">
                <div className="font-semibold text-red-600">清除所有数据</div>
                <div className="text-sm text-red-400">此操作不可恢复</div>
              </div>
            </div>
            <div className="icon-chevron-right text-red-400 group-hover:translate-x-1 transition-transform"></div>
          </div>
        </button>
      </div>

      <div className="card bg-gradient-to-br from-gray-50 to-white">
        <div className="text-center">
          <div className="w-16 h-16 bg-gradient-to-br from-gray-100 to-gray-200 rounded-full flex items-center justify-center mx-auto mb-4">
            <div className="icon-info text-2xl text-gray-600"></div>
          </div>
          <h3 className="font-semibold text-gray-800 mb-2">关于 N</h3>
          <p className="text-gray-500 text-sm leading-relaxed">
            N 是一个简洁轻量的生活记录应用，帮助你记录生活中的每一个美好瞬间。
            所有数据都安全地存储在你的设备本地，保护你的隐私。
          </p>
          <div className="text-xs text-gray-400 mt-3">
            © 2025 N Life Record App
          </div>
        </div>
      </div>
    </div>
  );
}

export default Profile;
