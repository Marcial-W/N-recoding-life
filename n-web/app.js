class ErrorBoundary extends React.Component {
  constructor(props) {
    super(props);
    this.state = { hasError: false, error: null };
  }

  static getDerivedStateFromError(error) {
    return { hasError: true, error };
  }

  componentDidCatch(error, errorInfo) {
    console.error('ErrorBoundary caught an error:', error, errorInfo.componentStack);
  }

  render() {
    if (this.state.hasError) {
      return (
        <div className="min-h-screen flex items-center justify-center bg-gray-50">
          <div className="text-center">
            <h1 className="text-2xl font-bold text-gray-900 mb-4">出现了一些问题</h1>
            <p className="text-gray-600 mb-4">抱歉，发生了意外错误</p>
            <button
              onClick={() => window.location.reload()}
              className="btn btn-primary"
            >
              重新加载
            </button>
          </div>
        </div>
      );
    }

    return this.props.children;
  }
}

function App() {
  try {
    const [activeTab, setActiveTab] = React.useState('create');

    const renderContent = () => {
      switch (activeTab) {
        case 'create':
          return <CreateRecord />;
        case 'stats':
          return <Statistics />;
        case 'profile':
          return <Profile />;
        default:
          return <CreateRecord />;
      }
    };

    return (
      <div className="min-h-screen pb-24 animate-fade-in" data-name="app" data-file="app.js">
        <div className="container mx-auto max-w-lg px-4">
          <div className="animate-slide-up">
            {renderContent()}
          </div>
        </div>
        <BottomNav activeTab={activeTab} onTabChange={setActiveTab} />
      </div>
    );
  } catch (error) {
    console.error('App component error:', error);
    return null;
  }
}

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <ErrorBoundary>
    <App />
  </ErrorBoundary>
);