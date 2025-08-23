function BottomNav({ activeTab, onTabChange }) {
  try {
    const tabs = [
      { id: 'create', label: '创建', icon: 'plus-circle', color: 'from-blue-500 to-purple-600' },
      { id: 'stats', label: '统计', icon: 'bar-chart-3', color: 'from-green-500 to-blue-600' },
      { id: 'profile', label: '我的', icon: 'user', color: 'from-purple-500 to-pink-600' }
    ];

    return (
      <div className="bottom-nav" data-name="bottom-nav" data-file="components/BottomNav.js">
        {tabs.map(tab => (
          <div
            key={tab.id}
            className={`nav-item ${activeTab === tab.id ? 'active' : ''}`}
            onClick={() => onTabChange(tab.id)}
          >
            <div className="relative">
              <div className={`icon-${tab.icon} text-xl mb-1 transition-all duration-300`}></div>
              {activeTab === tab.id && (
                <div className="absolute -inset-2 bg-white/20 rounded-full animate-pulse"></div>
              )}
            </div>
            <span className="text-xs font-medium">{tab.label}</span>
          </div>
        ))}
      </div>
    );
  } catch (error) {
    console.error('BottomNav component error:', error);
    return null;
  }
}
