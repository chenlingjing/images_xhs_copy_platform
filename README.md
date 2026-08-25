# images_xhs_copy_platform
基于多模态大模型的图片小红书文案生成平台，支持图片上传与 URL 输入，自动生成小红书风格的标题、正文与话题标签。

## 本地运行

1. 将 `.env.example` 复制为根目录 `.env`，并替换 MySQL、Redis、Qwen 和初始管理员配置。
2. 启动依赖：`docker compose -f docker/docker-compose.yml up -d`。
3. 启动后端：`python -m uvicorn backend.app.main:app --reload --port 8080`。
4. 启动前端：`cd frontend && npm run dev`。

后端首次启动时会自动创建或升级数据库表。仅当
`INITIAL_ADMIN_USERNAME`、`INITIAL_ADMIN_EMAIL`、`INITIAL_ADMIN_PASSWORD`
均已配置且账号不存在时，才会创建初始管理员；管理员密码不会写入代码仓库。
