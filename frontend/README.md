# 小红书文案生成平台 · 前端

基于 Vue 3 + TypeScript + Vite 的前端骨架，使用假数据模拟图片上传、文案生成、用户鉴权与历史记录，未接入真实后端接口。

## 技术栈

- Vue 3 (Composition API + `<script setup>`)
- TypeScript
- Vite
- Vue Router
- Pinia
- Tailwind CSS

## 已完成功能

### 官网前台

- [x] 官网首页 `/`
- [x] Hero 区域与价值主张
- [x] 功能亮点展示
- [x] 生成效果示例（小红书笔记卡片）
- [x] FAQ 折叠面板
- [x] 进入工作台 CTA

### 用户鉴权

- [x] 登录页 `/login`
- [x] 注册页 `/register`
- [x] 退出登录
- [x] 登录态持久化（localStorage）
- [x] 未登录用户不能访问工作台与历史记录页
- [x] 已登录用户不能访问登录/注册页

### 用户工作台

- [x] 工作台布局 `/workspace`（左侧侧边栏切换子页面）
- [x] 文案生成页 `/workspace/generate`
- [x] 图片本地上传（拖拽 / 点击）
- [x] 图片 URL 输入加载
- [x] 生成参数：产品名称、目标人群、语气风格
- [x] 小红书笔记卡片样式结果展示
- [x] 一键复制全文 / 单独复制标题、正文、标签
- [x] 重新生成
- [x] 上传 loading、生成 loading、空状态、错误状态

### 历史记录

- [x] 历史记录页 `/workspace/history`
- [x] 持久化存储（localStorage 按用户隔离）
- [x] 结构化展示：图片、输入参数、生成结果、时间、状态
- [x] 搜索与状态筛选
- [x] 回溯到工作台继续查看/编辑
- [x] 复制全文与删除单条记录

### 后台管理台

- [x] 管理员路由守卫（非管理员访问会被重定向）
- [x] 用量概览 `/admin`：用户总数、生成次数、成功率、趋势图、模型性能
- [x] 用户管理 `/admin/users`：用户列表、角色标识、搜索
- [x] 生成记录 `/admin/generations`：所有记录、状态筛选、搜索、删除

## 项目结构

```
frontend/
├── public/                  # 静态资源
├── src/
│   ├── components/          # 公共组件
│   │   ├── admin/           # 后台管理组件
│   │   └── WorkspaceLayout.vue
│   ├── router/              # 路由配置
│   ├── services/            # 模拟 API
│   │   ├── mockApi.ts       # 工作台相关
│   │   └── adminApi.ts      # 后台管理相关
│   ├── stores/              # Pinia 状态管理
│   │   ├── auth.ts          # 模拟登录态与角色
│   │   ├── generation.ts    # 文案生成状态
│   │   └── history.ts       # 历史记录持久化
│   ├── types/               # TypeScript 类型
│   ├── utils/               # 工具函数
│   ├── views/               # 页面
│   │   ├── HomeView.vue
│   │   ├── LoginView.vue
│   │   ├── RegisterView.vue
│   │   ├── WorkspaceView.vue
│   │   ├── HistoryView.vue
│   │   └── admin/           # 后台页面
│   ├── App.vue
│   ├── main.ts
│   └── style.css
├── index.html
├── package.json
├── tailwind.config.js
├── tsconfig.json
└── vite.config.ts
```

## 本地启动

```bash
cd frontend
npm install
npm run dev
```

开发服务器默认运行在 http://localhost:5173

## 演示账号

| 角色 | 用户名 | 密码 |
|------|--------|------|
| 普通用户 | demo | demo123 |
| 管理员 | admin | admin123 |

登录后，普通用户可进入工作台与历史记录；管理员额外可在顶部导航看到「后台管理」。

## 响应式说明

- 工作台在桌面端显示左侧固定侧边栏，移动端显示顶部折叠菜单
- 所有页面使用 Tailwind 响应式类，宽屏与窄屏均可正常浏览

## 构建

```bash
npm run build
```

## 后续接入真实接口说明

当前所有网络请求均使用 `src/services/` 下的假数据实现，用户与历史数据保存在 `localStorage`。后续接入后端时，只需：

1. 将 `src/services/mockApi.ts` 与 `src/services/adminApi.ts` 替换为真实的 HTTP 请求（如 axios/fetch）。
2. 在 `src/stores/auth.ts` 中接入真实登录态与角色判断，移除 localStorage 密码存储。
3. 在 `src/stores/history.ts` 中改为从后端加载/保存历史记录。
4. 保持页面组件与状态调用方式不变。
5. 根据后端接口地址配置 Vite 代理（`vite.config.ts` 中 `server.proxy`）。
