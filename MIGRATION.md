# 项目迁移指南

本文档说明如何从原始项目迁移到新的拆分项目结构。

## 迁移概述

原始项目包含两个版本的代码：
- 根目录：网页端版本（HTML + React CDN）
- my-app目录：移动端版本（Create React App + Capacitor）

现在已拆分为两个独立项目：
- `n-web/`：网页端项目
- `n-mobile/`：移动端项目

## 迁移步骤

### 1. 备份原始项目

```bash
# 创建备份
cp -r . ../N-mobile-app-backup
```

### 2. 清理原始文件

迁移完成后，可以删除以下文件：
- `app.js` (已迁移到 n-web/)
- `index.html` (已迁移到 n-web/)
- `components/` (已迁移到 n-web/)
- `utils/` (已迁移到 n-web/)
- `manifest.json` (已迁移到 n-web/)
- `sw.js` (已迁移到 n-web/)
- `my-app/` (已迁移到 n-mobile/)

### 3. 更新开发流程

#### 网页端开发
```bash
cd n-web
npm install
npm start
```

#### 移动端开发
```bash
cd n-mobile
npm install
npm start
```

## 文件对应关系

### 网页端 (n-web)
| 原始位置 | 新位置 | 说明 |
|---------|--------|------|
| `app.js` | `n-web/app.js` | 主应用逻辑 |
| `index.html` | `n-web/index.html` | 主页面 |
| `components/` | `n-web/components/` | React组件 |
| `utils/` | `n-web/utils/` | 工具函数 |
| `manifest.json` | `n-web/manifest.json` | PWA配置 |
| `sw.js` | `n-web/sw.js` | Service Worker |

### 移动端 (n-mobile)
| 原始位置 | 新位置 | 说明 |
|---------|--------|------|
| `my-app/src/` | `n-mobile/src/` | React源代码 |
| `my-app/public/` | `n-mobile/public/` | 静态资源 |
| `my-app/android/` | `n-mobile/android/` | Android原生代码 |
| `my-app/ios/` | `n-mobile/ios/` | iOS原生代码 |
| `my-app/package.json` | `n-mobile/package.json` | 项目配置 |
| `my-app/capacitor.config.ts` | `n-mobile/capacitor.config.ts` | Capacitor配置 |

## 配置更新

### 网页端配置
- 更新了 `package.json` 中的项目信息
- 添加了开发服务器配置
- 优化了依赖管理

### 移动端配置
- 更新了项目名称和描述
- 添加了Capacitor相关脚本
- 优化了构建配置

## 开发环境设置

### 网页端环境
```bash
cd n-web
npm install
npm start
```

### 移动端环境
```bash
cd n-mobile
npm install
npm start
```

## 测试验证

### 网页端测试
1. 启动开发服务器
2. 访问 http://localhost:3000
3. 测试所有功能模块
4. 验证PWA功能

### 移动端测试
1. 启动开发服务器
2. 构建移动应用
3. 在设备上测试
4. 验证原生功能

## 常见问题

### Q: 如何同时开发两个项目？
A: 可以打开两个终端窗口，分别进入 n-web 和 n-mobile 目录进行开发。

### Q: 数据如何共享？
A: 两个项目使用相同的本地存储方案，数据格式兼容。

### Q: 如何部署？
A: 网页端部署到静态托管服务，移动端构建APK/IPA文件。

### Q: 代码如何同步？
A: 核心业务逻辑和UI组件需要手动同步，建议建立共享组件库。

## 后续优化建议

1. **建立共享组件库**
   - 提取公共组件
   - 使用npm包管理
   - 版本控制

2. **统一代码规范**
   - ESLint配置
   - Prettier格式化
   - Git hooks

3. **自动化部署**
   - CI/CD流程
   - 自动化测试
   - 版本管理

4. **性能优化**
   - 代码分割
   - 懒加载
   - 缓存策略

## 联系支持

如果在迁移过程中遇到问题，请：
1. 查看项目文档
2. 提交Issue
3. 联系开发团队 