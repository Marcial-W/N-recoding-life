# iOS端开发指南

本文档详细说明iOS端的开发、构建和部署流程。

## 项目结构

```
ios/
├── App/                          # iOS应用主目录
│   ├── App/                      # 应用源代码
│   │   ├── AppDelegate.swift     # 应用代理
│   │   ├── SceneDelegate.swift   # 场景代理 (iOS 13+)
│   │   ├── CustomBridgeViewController.swift # 自定义Capacitor控制器
│   │   ├── Info.plist           # 应用配置
│   │   ├── Assets.xcassets/     # 应用资源
│   │   ├── Base.lproj/          # 基础本地化
│   │   ├── en.lproj/            # 英文本地化
│   │   └── zh-Hans.lproj/       # 中文简体本地化
│   ├── App.xcodeproj/           # Xcode项目文件
│   ├── App.xcworkspace/         # Xcode工作空间
│   └── Podfile                  # CocoaPods依赖配置
├── build.sh                     # 构建脚本
└── README.md                    # 本文档
```

## 环境要求

### 开发环境
- **macOS**: 12.0 或更高版本
- **Xcode**: 14.0 或更高版本
- **iOS SDK**: 14.0 或更高版本
- **CocoaPods**: 1.11.0 或更高版本
- **Node.js**: 16.0 或更高版本

### 目标设备
- **iOS**: 14.0 或更高版本
- **设备**: iPhone, iPad, iPod touch

## 安装和配置

### 1. 安装依赖

```bash
# 进入iOS目录
cd n-mobile/ios/App

# 安装CocoaPods依赖
pod install

# 返回项目根目录安装Node.js依赖
cd ../..
npm install
```

### 2. 打开项目

```bash
# 使用Xcode打开工作空间
open App.xcworkspace
```

**注意**: 必须打开 `.xcworkspace` 文件，而不是 `.xcodeproj` 文件。

## 开发流程

### 1. 启动开发服务器

```bash
# 在项目根目录启动React开发服务器
cd n-mobile
npm start
```

### 2. 在模拟器中运行

```bash
# 在iOS目录中运行
cd ios/App
npx cap run ios
```

### 3. 在真机上运行

1. 在Xcode中打开项目
2. 选择目标设备
3. 配置开发者账号和证书
4. 点击运行按钮

## 构建和部署

### 使用构建脚本

```bash
# 进入iOS目录
cd n-mobile/ios

# 查看帮助
./build.sh help

# 完整构建流程
./build.sh full

# 单独步骤
./build.sh clean      # 清理项目
./build.sh install    # 安装依赖
./build.sh build      # 构建项目
./build.sh archive    # 构建归档
./build.sh export     # 导出IPA
```

### 手动构建

#### 1. 清理项目
```bash
xcodebuild clean -workspace App.xcworkspace -scheme App
```

#### 2. 构建项目
```bash
xcodebuild build \
  -workspace App.xcworkspace \
  -scheme App \
  -configuration Release \
  -destination 'generic/platform=iOS'
```

#### 3. 构建归档
```bash
xcodebuild archive \
  -workspace App.xcworkspace \
  -scheme App \
  -configuration Release \
  -archivePath ./build/App.xcarchive \
  -destination 'generic/platform=iOS'
```

#### 4. 导出IPA
```bash
xcodebuild -exportArchive \
  -archivePath ./build/App.xcarchive \
  -exportPath ./build/App.ipa \
  -exportOptionsPlist exportOptions.plist
```

## 配置说明

### Info.plist 配置

主要配置项包括：

- **应用标识**: `CFBundleIdentifier`
- **应用名称**: `CFBundleDisplayName`
- **版本信息**: `CFBundleShortVersionString`, `CFBundleVersion`
- **权限描述**: 相机、相册、位置等权限的使用说明
- **URL Schemes**: 自定义URL协议支持
- **后台模式**: 后台运行支持

### Podfile 配置

包含以下主要依赖：

- **Capacitor核心**: 跨平台框架
- **Capacitor插件**: 各种原生功能插件
- **第三方库**: 网络、图片、数据库等

### 本地化支持

支持中文简体和英文：

- `zh-Hans.lproj/Localizable.strings`: 中文简体
- `en.lproj/Localizable.strings`: 英文

## 权限配置

### 相机权限
```xml
<key>NSCameraUsageDescription</key>
<string>此应用需要访问相机来拍摄照片</string>
```

### 相册权限
```xml
<key>NSPhotoLibraryUsageDescription</key>
<string>此应用需要访问相册来选择照片</string>
```

### 位置权限
```xml
<key>NSLocationWhenInUseUsageDescription</key>
<string>此应用需要访问位置信息来提供相关服务</string>
```

### 麦克风权限
```xml
<key>NSMicrophoneUsageDescription</key>
<string>此应用需要访问麦克风来录制音频</string>
```

## 代码签名

### 开发证书
1. 在Apple Developer网站创建开发证书
2. 下载并安装证书
3. 在Xcode中配置证书

### 发布证书
1. 创建App Store发布证书
2. 创建Provisioning Profile
3. 配置代码签名设置

## 测试

### 单元测试
```bash
xcodebuild test \
  -workspace App.xcworkspace \
  -scheme App \
  -destination 'platform=iOS Simulator,name=iPhone 14,OS=latest'
```

### UI测试
1. 在Xcode中创建UI测试目标
2. 编写UI测试用例
3. 运行UI测试

## 常见问题

### 1. 构建失败
- 检查Xcode版本是否兼容
- 清理项目并重新构建
- 检查依赖是否正确安装

### 2. 权限问题
- 确保Info.plist中包含相应的权限描述
- 检查设备设置中的权限状态

### 3. 网络问题
- 检查网络权限配置
- 验证HTTPS证书设置

### 4. 代码签名问题
- 检查证书是否有效
- 验证Provisioning Profile配置
- 确认Bundle Identifier匹配

## 性能优化

### 1. 启动优化
- 减少启动时的资源加载
- 优化启动画面显示
- 使用懒加载

### 2. 内存优化
- 及时释放不需要的资源
- 使用自动释放池
- 避免内存泄漏

### 3. 网络优化
- 使用缓存机制
- 压缩网络请求
- 实现断点续传

## 发布流程

### 1. 准备发布
- 更新版本号
- 配置发布证书
- 测试应用功能

### 2. 上传到App Store
- 使用Xcode或Application Loader上传
- 填写应用信息
- 提交审核

### 3. 发布管理
- 监控应用性能
- 收集用户反馈
- 及时更新版本

## 联系支持

如果在开发过程中遇到问题，请：

1. 查看项目文档
2. 提交Issue到项目仓库
3. 联系开发团队

## 更新日志

### v1.0.0 (2024-01-01)
- 初始版本发布
- 支持基本的跨平台功能
- 集成Capacitor框架
- 添加本地化支持 