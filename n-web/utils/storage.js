// 本地存储工具函数
const STORAGE_KEYS = {
  RECORDS: 'n_app_records'
};

// 获取所有记录
function getRecords() {
  try {
    const records = localStorage.getItem(STORAGE_KEYS.RECORDS);
    return records ? JSON.parse(records) : [];
  } catch (error) {
    console.error('获取记录失败:', error);
    return [];
  }
}

// 保存记录
function saveRecord(record) {
  try {
    const allRecords = getRecords();
    
    const existingIndex = allRecords.findIndex(r => r.id === record.id);
    if (existingIndex >= 0) {
      allRecords[existingIndex] = record;
    } else {
      allRecords.push(record);
    }
    
    localStorage.setItem(STORAGE_KEYS.RECORDS, JSON.stringify(allRecords));
    return true;
  } catch (error) {
    console.error('保存记录失败:', error);
    return false;
  }
}

// 删除记录
function deleteRecord(recordId) {
  try {
    const allRecords = getRecords();
    const filteredRecords = allRecords.filter(r => r.id !== recordId);
    
    localStorage.setItem(STORAGE_KEYS.RECORDS, JSON.stringify(filteredRecords));
    return true;
  } catch (error) {
    console.error('删除记录失败:', error);
    return false;
  }
}

// 清除所有记录
function clearAllRecords() {
  try {
    localStorage.removeItem(STORAGE_KEYS.RECORDS);
    return true;
  } catch (error) {
    console.error('清除记录失败:', error);
    return false;
  }
}
