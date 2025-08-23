# N - 生活记录应用 (网页版)

一个简洁轻量的生活记录应用，帮助你记录生活中的每一个美好瞬间。

## 特性

- 📝 **简洁记录** - 快速记录生活中的重要时刻
- 📊 **数据统计** - 可视化分析你的记录数据
- 📱 **响应式设计** - 完美适配各种设备
- 🔒 **隐私保护** - 所有数据本地存储
- 📤 **数据导出** - 支持多种格式导出
- ⚡ **PWA支持** - 可安装为桌面应用

## 技术栈

- **前端框架**: React 18 (CDN)
- **样式框架**: Tailwind CSS
- **图标库**: Lucide Icons
- **图表库**: Chart.js
- **构建工具**: 原生HTML + CDN

## 快速开始

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

## 项目结构

```
n-web/
├── index.html          # 主页面
├── app.js              # 主应用逻辑
├── components/         # React组件
│   ├── BottomNav.js    # 底部导航
│   ├── CreateRecord.js # 创建记录
│   ├── Statistics.js   # 统计页面
│   └── Profile.js      # 个人中心
├── utils/              # 工具函数
│   └── storage.js      # 本地存储
├── assets/             # 静态资源
├── manifest.json       # PWA配置
├── sw.js              # Service Worker
└── package.json       # 项目配置
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

## 浏览器支持

- Chrome 60+
- Firefox 55+
- Safari 12+
- Edge 79+

## 开发指南

### 添加新组件
1. 在 `components/` 目录创建新组件
2. 在 `app.js` 中导入并使用
3. 添加相应的样式

### 修改样式
- 使用 Tailwind CSS 类名
- 自定义样式在 `index.html` 的 `<style>` 标签中

### 本地存储
- 使用 `utils/storage.js` 中的函数
- 数据存储在浏览器的 localStorage 中

## 部署

### 静态托管
可以直接部署到任何静态托管服务：
- GitHub Pages
- Netlify
- Vercel
- 阿里云OSS

### PWA部署
1. 确保 `manifest.json` 配置正确
2. 部署 `sw.js` Service Worker
3. 使用HTTPS协议

## 贡献

欢迎提交 Issue 和 Pull Request！

## 许可证

MIT License 