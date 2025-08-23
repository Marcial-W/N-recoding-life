# N - 生活记录应用 (移动端)

一个基于React和Capacitor的跨平台移动应用，帮助你记录生活中的每一个美好瞬间。

## 特性

- 📱 **跨平台支持** - Android和iOS原生应用
- 📝 **简洁记录** - 快速记录生活中的重要时刻
- 📊 **数据统计** - 可视化分析你的记录数据
- 🔒 **隐私保护** - 所有数据本地存储
- 📤 **数据导出** - 支持多种格式导出
- ⚡ **原生性能** - 接近原生应用的性能体验

## 技术栈

- **前端框架**: React 19
- **跨平台**: Capacitor 7
- **样式框架**: Tailwind CSS
- **图标库**: Lucide Icons
- **图表库**: Chart.js
- **构建工具**: Create React App
- **原生开发**: Android Studio / Xcode

## 快速开始

### 环境要求

- Node.js 18+
- npm 或 yarn
- Android Studio (Android开发)
- Xcode (iOS开发，仅macOS)

### 安装依赖

```bash
npm install
```

### 启动开发服务器

```bash
npm start
```

应用将在 http://localhost:3000 启动

### 构建生产版本

```bash
npm run build
```

### 移动端开发

#### Android

```bash
# 同步代码到Android项目
npm run cap:sync

# 打开Android Studio
npm run cap:open:android

# 构建Android应用
npm run cap:build:android
```

#### iOS

```bash
# 同步代码到iOS项目
npm run cap:sync

# 打开Xcode
npm run cap:open:ios

# 构建iOS应用
npm run cap:build:ios
```

## 项目结构

```
n-mobile/
├── src/                    # React源代码
│   ├── components/         # React组件
│   │   ├── BottomNav.js    # 底部导航
│   │   ├── CreateRecord.js # 创建记录
│   │   ├── Statistics.js   # 统计页面
│   │   └── Profile.js      # 个人中心
│   ├── utils/              # 工具函数
│   │   └── storage.js      # 本地存储
│   ├── App.js              # 主应用组件
│   ├── App.css             # 应用样式
│   └── index.js            # 入口文件
├── public/                 # 静态资源
├── android/                # Android原生代码
├── ios/                    # iOS原生代码
├── capacitor.config.ts     # Capacitor配置
└── package.json           # 项目配置
```

## 功能模块

### 1. 创建记录
- 快速添加生活记录
- 支持分类标签
- 位置信息记录
- 时间自动记录

### 2. 数据统计
- 记录数量统计
- 分类分布图表
- 时间趋势分析
- 数据可视化

### 3. 个人中心
- 数据导出功能
- 应用设置管理
- 数据清理功能
- 关于信息

## 数据导出

支持多种格式导出：
- **JSON格式** - 完整数据结构
- **CSV格式** - 表格数据
- **ZIP格式** - 包含JSON和CSV

## 平台支持

### Android
- Android 5.0+ (API 21+)
- 支持ARM和x86架构

### iOS
- iOS 13.0+
- 支持iPhone和iPad

## 开发指南

### 添加新组件
1. 在 `src/components/` 目录创建新组件
2. 在 `App.js` 中导入并使用
3. 添加相应的样式

### 修改样式
- 使用 Tailwind CSS 类名
- 自定义样式在 `App.css` 中

### 本地存储
- 使用 `src/utils/storage.js` 中的函数
- 数据存储在设备的本地存储中

### 原生功能集成
- 使用 Capacitor 插件
- 在 `capacitor.config.ts` 中配置

## 构建和部署

### Android APK构建
```bash
npm run cap:build:android
```

### iOS应用构建
```bash
npm run cap:build:ios
```

### 应用商店发布
1. 构建生产版本
2. 签名应用
3. 上传到应用商店

## 开发工具

### 推荐IDE
- Visual Studio Code
- Android Studio
- Xcode

### 调试工具
- Chrome DevTools (Web调试)
- Android Studio Debugger (Android调试)
- Xcode Debugger (iOS调试)

## 贡献

欢迎提交 Issue 和 Pull Request！

## 许可证

MIT License
