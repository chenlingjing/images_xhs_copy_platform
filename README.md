# 小红书文案生成平台

一个用于将图片通过大模型生成小红书风格文案的项目，包含前端（Vue 3 + Vite）、后端（FastAPI + SQLAlchemy + Redis）与 Docker 配置（MySQL / Redis）。

## 目录结构（简要）
- `frontend/`：前端代码（Vue 3 + Pinia），开发入口 `src/main.ts`，路由 `src/router`，与 API 封装 `src/services/mockApi.ts`。
- `backend/`：后端代码（FastAPI），入口 `app/main.py`，配置 `app/core/config.py`，数据库 `app/core/database.py`，redis `app/core/redis.py`，服务在 `app/services`。
- `docker/`：用于本地运行 MySQL 与 Redis 的 `docker-compose.yml` 与初始化脚本。

## 快速开始（开发）

先确保本机安装了：
- Node.js（建议 18+）和 npm 或 yarn
- Python 3.9+（或项目虚拟环境）
- Docker（可选，用于快速启动 MySQL/Redis）

1. 启动数据库服务（可选，若用 Docker）：

```bash
cd docker
docker compose up -d
```

2. 后端：

```bash
cd backend
# 可选：创建并激活虚拟环境
python -m venv .venv
source .venv/bin/activate
# 安装依赖（项目可能在 requirements.txt/pyproject 中声明）
pip install -r requirements.txt
# 启动后端（默认端口 8081）
uvicorn app.main:app --host 0.0.0.0 --port 8081
```

3. 前端：

```bash
cd frontend
npm install
npm run dev
# 浏览器会打开： http://localhost:5173
```

前端默认会请求后端 `http://localhost:8081`（见 `frontend/src/services/mockApi.ts` 中的 `API_BASE_URL`）。如果后端在其它地址，请通过环境变量 `VITE_API_BASE_URL` 覆盖，例如：

```bash
VITE_API_BASE_URL=http://localhost:8081 npm run dev
```

## 关键文件说明
- `frontend/src/main.ts`：应用入口，创建并挂载 Vue 应用。挂载点在根 HTML 的 `<div id="app">`。
- `frontend/index.html`：页面模板，加载前端入口脚本。
- `frontend/src/services/mockApi.ts`：封装与后端交互的请求、图片上传与生成调用逻辑（默认指向 `/images/upload` 与 `/api/generate`）。
- `backend/app/main.py`：后端入口，注册路由、CORS、静态文件（`/uploads`）与生命周期。健康检查接口见 `backend/app/routers/health.py`。

## 常见问题与排查
- 如果前端出现 `failed to fetch` 或 CORS 报错，检查：
  - 后端是否已启动且可访问（`curl http://localhost:8081/health`）
  - `app/core/config.py` 中 `CORS_ORIGINS` 是否包含前端地址（如 `http://localhost:5173`）
- 图片上传后无法显示：确认后端 `uploads` 目录存在且 `app.main` 已 `mount` 静态路径 `/uploads`。
- 大模型调用失败：确认 `QWEN_API_KEY`（或 `DASHSCOPE_API_KEY`）在后端环境中已配置，见 `backend/app/core/config.py`。

## 部署建议
- 将前端构建产物发布到静态站点或由后端静态服务提供（`vite build`）。
- 后端在生产环境建议使用 Gunicorn/uvicorn workers 或容器化部署，数据库与缓存使用受管或容器化实例。

## 贡献与代码审阅
- 我们使用分支开发，请在 feature 分支上提交补丁并提交 Pull Request 到 `dev` 分支进行审查与合并。

---
如需我代为创建 PR、或把 README 推送到远程分支并打开 PR 页面，请确认，我会继续操作。
# images_xhs_copy_platform
基于多模态大模型的图片小红书文案生成平台，支持图片上传与 URL 输入，自动生成小红书风格的标题、正文与话题标签。
