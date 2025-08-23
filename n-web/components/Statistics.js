function Statistics() {
  try {
    const [records, setRecords] = React.useState([]);
    const [timeRange, setTimeRange] = React.useState('month');
    const [chartData, setChartData] = React.useState(null);
    const exportRef = React.useRef(null);

    React.useEffect(() => {
      setRecords(getRecords());
    }, []);

    React.useEffect(() => {
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

    React.useEffect(() => {
      if (chartData && chartData.categories.length > 0) {
        const ctx = document.getElementById('categoryChart');
        if (ctx) {
          // Clear previous chart
          ChartJS.getChart(ctx)?.destroy();
          
          new ChartJS(ctx, {
            type: 'doughnut',
            data: {
              labels: chartData.categories,
              datasets: [{
                data: chartData.counts,
                backgroundColor: [
                  'rgba(99, 102, 241, 0.8)',
                  'rgba(16, 185, 129, 0.8)', 
                  'rgba(245, 158, 11, 0.8)',
                  'rgba(239, 68, 68, 0.8)',
                  'rgba(139, 92, 246, 0.8)',
                  'rgba(6, 182, 212, 0.8)',
                  'rgba(249, 115, 22, 0.8)',
                  'rgba(132, 204, 22, 0.8)'
                ],
                borderWidth: 2,
                borderColor: '#ffffff',
                hoverBackgroundColor: [
                  '#6366f1', '#10b981', '#f59e0b', '#ef4444', 
                  '#8b5cf6', '#06b6d4', '#f97316', '#84cc16'
                ]
              }]
            },
            options: {
              responsive: true,
              maintainAspectRatio: false,
              plugins: {
                legend: {
                  position: 'bottom',
                  display: false
                }
              }
            }
          });
        }
      }
    }, [chartData]);

    const exportStatsAsPDF = async () => {
      try {
        const { jsPDF } = window.jspdf || {};
        if (!window.html2canvas || !jsPDF) {
          alert('缺少导出依赖，请检查网络或稍后再试');
          return;
        }
        const exportArea = exportRef.current || document.querySelector('[data-name="statistics"] [data-export-area="stats"]');
        if (!exportArea) {
          alert('未找到导出区域');
          return;
        }
        const canvas = await window.html2canvas(exportArea, {
          backgroundColor: '#ffffff',
          scale: Math.min(2, window.devicePixelRatio || 2),
          useCORS: true
        });
        const imgData = canvas.toDataURL('image/png');
        const pdf = new jsPDF('p', 'mm', 'a4');
        const pageWidth = pdf.internal.pageSize.getWidth();
        const pageHeight = pdf.internal.pageSize.getHeight();

        // 等比缩放以适配单页
        let imgWidth = pageWidth;
        let imgHeight = canvas.height * imgWidth / canvas.width;
        if (imgHeight > pageHeight) {
          imgHeight = pageHeight;
          imgWidth = canvas.width * imgHeight / canvas.height;
        }
        const marginX = (pageWidth - imgWidth) / 2;
        const marginY = (pageHeight - imgHeight) / 2;

        pdf.addImage(imgData, 'PNG', marginX, marginY, imgWidth, imgHeight);
        const dateStr = new Date().toISOString().split('T')[0];
        pdf.save(`统计数据_${dateStr}.pdf`);
      } catch (e) {
        console.error('导出 PDF 失败:', e);
        alert('导出失败，请重试');
      }
    };

    return (
      <div className="py-6 space-y-6" data-name="statistics" data-file="components/Statistics.js">
        <div className="text-center">
          <div className="inline-flex items-center justify-center w-16 h-16 bg-gradient-to-br from-green-400 to-blue-500 rounded-3xl mb-4">
            <div className="icon-trending-up text-2xl text-white"></div>
          </div>
          <h1 className="text-3xl font-bold bg-gradient-to-r from-gray-900 to-gray-600 bg-clip-text text-transparent">
            数据统计
          </h1>
          <p className="text-gray-500 mt-2">洞察你的生活模式</p>
        </div>
        
        <div ref={exportRef} data-export-area="stats" className="space-y-6">
          <div className="card">
            <div className="flex justify-between items-center mb-6">
              <h3 className="text-lg font-semibold text-gray-800 flex items-center">
                <div className="icon-filter text-lg mr-2 text-blue-500"></div>
                时间范围
              </h3>
              <div className="flex items-center gap-2">
                <button
                  onClick={exportStatsAsPDF}
                  type="button"
                  className="btn btn-secondary !px-4 !py-2 flex items-center"
                  title="将统计数据导出为 PDF"
                >
                  <div className="icon-share-2 text-base mr-2"></div>
                  分享
                </button>
                <select
                  className="input-field w-auto min-w-24"
                  value={timeRange}
                  onChange={(e) => setTimeRange(e.target.value)}
                >
                  <option value="week">本周</option>
                  <option value="month">本月</option>
                  <option value="year">今年</option>
                </select>
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
                <div className="h-64 relative mb-4">
                  <canvas id="categoryChart"></canvas>
                </div>
                <div className="grid grid-cols-2 gap-2">
                  {chartData.categories.map((category, index) => (
                    <div key={category} className="flex items-center text-sm">
                      <div 
                        className="w-3 h-3 rounded-full mr-2"
                        style={{backgroundColor: [
                          '#6366f1', '#10b981', '#f59e0b', '#ef4444', 
                          '#8b5cf6', '#06b6d4', '#f97316', '#84cc16'
                        ][index % 8]}}
                      ></div>
                      <span className="text-gray-600">{category}</span>
                      <span className="ml-auto text-gray-800 font-medium">{chartData.counts[index]}</span>
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
        </div>
      </div>
    );
  } catch (error) {
    console.error('Statistics component error:', error);
    return null;
  }
}
