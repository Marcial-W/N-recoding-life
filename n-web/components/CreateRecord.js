function CreateRecord() {
  try {
    const [formData, setFormData] = React.useState({
      title: '',
      date: new Date().toISOString().split('T')[0],
      time: new Date().toLocaleTimeString('zh-CN', { hour12: false, hour: '2-digit', minute: '2-digit' }),
      location: '',
      description: '',
      category: '生活'
    });
    
    const [records, setRecords] = React.useState([]);
    const [isSubmitting, setIsSubmitting] = React.useState(false);

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

    React.useEffect(() => {
      setRecords(getRecords());
    }, []);

    const [selectedRecord, setSelectedRecord] = React.useState(null);

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
                placeholder="在哪里发生的呢..."
                className="input-field"
                value={formData.location}
                onChange={(e) => setFormData({...formData, location: e.target.value})}
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-3">分类</label>
              <div className="grid grid-cols-4 gap-3">
                {categories.map(cat => (
                  <button
                    key={cat.name}
                    type="button"
                    onClick={() => setFormData({...formData, category: cat.name})}
                    className={`p-3 rounded-2xl border-2 transition-all duration-300 ${
                      formData.category === cat.name 
                        ? 'border-purple-400 bg-gradient-to-br ' + cat.color + ' text-white transform scale-105' 
                        : 'border-gray-200 bg-white hover:border-purple-200 hover:scale-105'
                    }`}
                  >
                    <div className={`icon-${cat.icon} text-lg mb-1`}></div>
                    <span className="text-xs font-medium">{cat.name}</span>
                  </button>
                ))}
              </div>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">描述</label>
              <textarea
                placeholder="详细描述一下这个美好时刻..."
                className="input-field resize-none h-24"
                value={formData.description}
                onChange={(e) => setFormData({...formData, description: e.target.value})}
              />
            </div>
          </div>

          <button 
            type="submit" 
            disabled={isSubmitting}
            className={`btn btn-primary w-full flex items-center justify-center ${isSubmitting ? 'opacity-50' : ''}`}
          >
            {isSubmitting ? (
              <>
                <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-white mr-2"></div>
                保存中...
              </>
            ) : (
              <>
                <div className="icon-save text-lg mr-2"></div>
                保存记录
              </>
            )}
          </button>
        </form>

        <div>
          <h3 className="text-xl font-semibold text-gray-800 mb-4 flex items-center">
            <div className="icon-clock text-lg mr-2 text-purple-500"></div>
            最近记录
          </h3>
          <div className="space-y-3">
            {[...records]
              .sort((a, b) => new Date(b.createdAt || `${b.date}T${b.time || '00:00'}`) - new Date(a.createdAt || `${a.date}T${a.time || '00:00'}`))
              .slice(0, 5)
              .map((record, index) => (
              <div 
                key={record.id} 
                className="record-card animate-slide-up"
                style={{animationDelay: `${index * 0.1}s`}}
                onClick={() => setSelectedRecord(record)}
              >
                <div className="flex items-start space-x-3">
                  <div className={`w-10 h-10 rounded-2xl bg-gradient-to-br ${getCategoryColor(record.category)} flex items-center justify-center flex-shrink-0`}>
                    <div className={`icon-${getCategoryIcon(record.category)} text-white text-sm`}></div>
                  </div>
                  <div className="flex-1 min-w-0">
                    <div className="flex justify-between items-start mb-1">
                      <h4 className="font-semibold text-gray-800 truncate">{record.title}</h4>
                      <span className="text-xs text-purple-500 font-medium bg-purple-50 px-2 py-1 rounded-full">{record.category}</span>
                    </div>
                    <div className="text-sm text-gray-500 space-y-1">
                      <div className="flex items-center">
                        <div className="icon-calendar text-xs mr-1"></div>
                        {record.date} {record.time}
                      </div>
                      {record.location && (
                        <div className="flex items-center">
                          <div className="icon-map-pin text-xs mr-1 text-red-400"></div>
                          {record.location}
                        </div>
                      )}
                    </div>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>

        {selectedRecord && (
          <div className="fixed inset-0 bg-black/30 backdrop-blur-sm flex items-end sm:items-center justify-center z-50" onClick={() => setSelectedRecord(null)}>
            <div 
              className="w-full sm:max-w-md bg-white rounded-t-3xl sm:rounded-3xl p-6 shadow-2xl animate-slide-up"
              onClick={(e) => e.stopPropagation()}
            >
              <div className="flex items-center justify-between mb-4">
                <div className="flex items-center">
                  <div className={`w-12 h-12 rounded-2xl bg-gradient-to-br ${getCategoryColor(selectedRecord.category)} flex items-center justify-center mr-3`}>
                    <div className={`icon-${getCategoryIcon(selectedRecord.category)} text-white`}></div>
                  </div>
                  <div>
                    <div className="font-semibold text-gray-800 text-lg">{selectedRecord.title}</div>
                    <div className="text-xs text-purple-500 font-medium bg-purple-50 px-2 py-0.5 rounded-full inline-block mt-1">{selectedRecord.category}</div>
                  </div>
                </div>
                <button className="p-2 rounded-xl hover:bg-gray-100" onClick={() => setSelectedRecord(null)}>
                  <div className="icon-x"></div>
                </button>
              </div>

              <div className="space-y-3 text-sm text-gray-600">
                <div className="flex items-center">
                  <div className="icon-calendar mr-2 text-gray-400"></div>
                  <span>{selectedRecord.date} {selectedRecord.time}</span>
                </div>
                {selectedRecord.location && (
                  <div className="flex items-center">
                    <div className="icon-map-pin mr-2 text-red-400"></div>
                    <span>{selectedRecord.location}</span>
                  </div>
                )}
                {selectedRecord.description && (
                  <div className="flex items-start">
                    <div className="icon-align-left mr-2 mt-0.5 text-gray-400"></div>
                    <span className="whitespace-pre-wrap break-words">{selectedRecord.description}</span>
                  </div>
                )}
              </div>

              <div className="mt-5">
                <button className="btn btn-secondary w-full" onClick={() => setSelectedRecord(null)}>关闭</button>
              </div>
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
