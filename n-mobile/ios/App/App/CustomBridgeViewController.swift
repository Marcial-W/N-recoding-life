import UIKit
import Capacitor
import WebKit

class CustomBridgeViewController: CAPBridgeViewController {
    
    override func viewDidLoad() {
        super.viewDidLoad()
        
        // 配置WebView
        configureWebView()
        
        // 设置导航栏
        setupNavigationBar()
        
        // 添加加载指示器
        setupLoadingIndicator()
    }
    
    override func viewWillAppear(_ animated: Bool) {
        super.viewWillAppear(animated)
        
        // 隐藏导航栏
        navigationController?.setNavigationBarHidden(true, animated: animated)
    }
    
    // MARK: - WebView Configuration
    
    private func configureWebView() {
        guard let webView = webView else { return }
        
        // 设置WebView代理
        webView.navigationDelegate = self
        webView.uiDelegate = self
        
        // 配置WebView设置
        webView.configuration.allowsInlineMediaPlayback = true
        webView.configuration.mediaTypesRequiringUserActionForPlayback = []
        webView.configuration.allowsAirPlayForMediaPlayback = true
        
        // 设置用户代理
        webView.customUserAgent = "N-Mobile-App/1.0"
        
        // 启用JavaScript
        webView.configuration.preferences.javaScriptEnabled = true
        
        // 允许文件访问
        webView.configuration.preferences.setValue(true, forKey: "allowFileAccessFromFileURLs")
        webView.configuration.preferences.setValue(true, forKey: "allowUniversalAccessFromFileURLs")
    }
    
    // MARK: - Navigation Bar Setup
    
    private func setupNavigationBar() {
        // 设置状态栏样式
        setNeedsStatusBarAppearanceUpdate()
    }
    
    override var preferredStatusBarStyle: UIStatusBarStyle {
        return .lightContent
    }
    
    override var prefersStatusBarHidden: Bool {
        return false
    }
    
    // MARK: - Loading Indicator
    
    private func setupLoadingIndicator() {
        // 创建加载指示器
        let activityIndicator = UIActivityIndicatorView(style: .large)
        activityIndicator.color = .systemBlue
        activityIndicator.tag = 999
        activityIndicator.hidesWhenStopped = true
        
        view.addSubview(activityIndicator)
        activityIndicator.translatesAutoresizingMaskIntoConstraints = false
        
        NSLayoutConstraint.activate([
            activityIndicator.centerXAnchor.constraint(equalTo: view.centerXAnchor),
            activityIndicator.centerYAnchor.constraint(equalTo: view.centerYAnchor)
        ])
    }
    
    private func showLoadingIndicator() {
        if let indicator = view.viewWithTag(999) as? UIActivityIndicatorView {
            indicator.startAnimating()
        }
    }
    
    private func hideLoadingIndicator() {
        if let indicator = view.viewWithTag(999) as? UIActivityIndicatorView {
            indicator.stopAnimating()
        }
    }
    
    // MARK: - Error Handling
    
    private func showError(_ error: Error) {
        let alert = UIAlertController(
            title: "加载错误",
            message: error.localizedDescription,
            preferredStyle: .alert
        )
        
        alert.addAction(UIAlertAction(title: "重试", style: .default) { _ in
            self.reloadWebView()
        })
        
        alert.addAction(UIAlertAction(title: "取消", style: .cancel))
        
        present(alert, animated: true)
    }
    
    private func reloadWebView() {
        webView?.reload()
    }
    
    // MARK: - Capacitor Bridge Overrides
    
    override func webView(_ webView: WKWebView, didStartProvisionalNavigation navigation: WKNavigation!) {
        super.webView(webView, didStartProvisionalNavigation: navigation)
        showLoadingIndicator()
    }
    
    override func webView(_ webView: WKWebView, didFinish navigation: WKNavigation!) {
        super.webView(webView, didFinish: navigation)
        hideLoadingIndicator()
    }
    
    override func webView(_ webView: WKWebView, didFail navigation: WKNavigation!, withError error: Error) {
        super.webView(webView, didFail: navigation, withError: error)
        hideLoadingIndicator()
        showError(error)
    }
    
    override func webView(_ webView: WKWebView, didFailProvisionalNavigation navigation: WKNavigation!, withError error: Error) {
        super.webView(webView, didFailProvisionalNavigation: navigation, withError: error)
        hideLoadingIndicator()
        showError(error)
    }
}

// MARK: - WKNavigationDelegate

extension CustomBridgeViewController: WKNavigationDelegate {
    
    func webView(_ webView: WKWebView, decidePolicyFor navigationAction: WKNavigationAction, decisionHandler: @escaping (WKNavigationActionPolicy) -> Void) {
        // 处理外部链接
        if let url = navigationAction.request.url, !url.absoluteString.contains("localhost") {
            if UIApplication.shared.canOpenURL(url) {
                UIApplication.shared.open(url)
                decisionHandler(.cancel)
                return
            }
        }
        
        decisionHandler(.allow)
    }
    
    func webView(_ webView: WKWebView, decidePolicyFor navigationResponse: WKNavigationResponse, decisionHandler: @escaping (WKNavigationResponsePolicy) -> Void) {
        decisionHandler(.allow)
    }
}

// MARK: - WKUIDelegate

extension CustomBridgeViewController: WKUIDelegate {
    
    func webView(_ webView: WKWebView, createWebViewWith configuration: WKWebViewConfiguration, for navigationAction: WKNavigationAction, windowFeatures: WKWindowFeatures) -> WKWebView? {
        // 处理新窗口打开
        if navigationAction.targetFrame == nil {
            webView.load(navigationAction.request)
        }
        return nil
    }
    
    func webView(_ webView: WKWebView, runJavaScriptAlertPanelWithMessage message: String, initiatedByFrame frame: WKFrameInfo, completionHandler: @escaping () -> Void) {
        let alert = UIAlertController(title: nil, message: message, preferredStyle: .alert)
        alert.addAction(UIAlertAction(title: "确定", style: .default) { _ in
            completionHandler()
        })
        present(alert, animated: true)
    }
    
    func webView(_ webView: WKWebView, runJavaScriptConfirmPanelWithMessage message: String, initiatedByFrame frame: WKFrameInfo, completionHandler: @escaping (Bool) -> Void) {
        let alert = UIAlertController(title: nil, message: message, preferredStyle: .alert)
        alert.addAction(UIAlertAction(title: "确定", style: .default) { _ in
            completionHandler(true)
        })
        alert.addAction(UIAlertAction(title: "取消", style: .cancel) { _ in
            completionHandler(false)
        })
        present(alert, animated: true)
    }
} 