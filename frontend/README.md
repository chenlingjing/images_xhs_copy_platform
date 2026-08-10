# 小红书文案生成平台 · 前端

基于 Vue 3 + TypeScript + Vite 的前端骨架，当前仅包含用户工作台页面，使用假数据模拟图片上传与文案生成流程，未接入真实后端接口。

## 技术栈

- Vue 3 (Composition API + `<script setup>`)
- TypeScript
- Vite
- Vue Router
- Pinia
- Tailwind CSS

## 已实现功能

- [x] 工作台页面 `/workspace`
- [x] 图片本地上传（拖拽 / 点击）
- [x] 图片 URL 输入加载
- [x] 生成参数：产品名称、目标人群、语气风格
- [x] 小红书笔记卡片样式结果展示
- [x] 一键复制全文 / 单独复制标题、正文、标签
- [x] 重新生成
- [x] 上传 loading、生成 loading、空状态、错误状态
- [x] 最近生成历史展示
- [x] 响应式布局

## 项目结构

```
frontend/
├── public/              # 静态资源
├── src/
│   ├── components/      # 公共组件
│   ├── router/          # 路由配置
│   ├── services/        # 模拟 API（mockApi.ts）
│   ├── stores/          # Pinia 状态管理
│   ├── types/           # TypeScript 类型
│   ├── utils/           # 工具函数
│   ├── views/           # 页面
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
# 进入前端目录
cd frontend

# 安装依赖
npm install

# 启动开发服务器
npm run dev
```

开发服务器默认运行在 http://localhost:5173

## 构建

```bash
npm run build
```

## 后续接入真实接口说明

当前所有网络请求均使用 `src/services/mockApi.ts` 中的假数据实现。后续接入后端时，只需：

1. 将 `mockApi.ts` 替换为真实的 HTTP 请求（如 axios/fetch）。
2. 在 `src/stores/generation.ts` 中保持状态与调用方式不变。
3. 根据后端接口地址配置 Vite 代理（`vite.config.ts` 中 `server.proxy`）。
