-- 使用数据库（容器启动时自动创建，直接使用）
USE xhs_copy_db;

-- 文案生成记录表（核心业务表）
CREATE TABLE IF NOT EXISTS generate_record (
    id BIGINT PRIMARY KEY AUTO_INCREMENT COMMENT '主键ID',
    image_type TINYINT DEFAULT 1 COMMENT '图片类型：1-本地上传 2-URL链接',
    image_url VARCHAR(500) DEFAULT '' COMMENT '图片存储路径/在线URL',
    product_name VARCHAR(100) DEFAULT '' COMMENT '产品名称（用户可选输入）',
    target_audience VARCHAR(100) DEFAULT '' COMMENT '目标人群（用户可选输入）',
    tone_style VARCHAR(50) DEFAULT '' COMMENT '语气风格（用户可选输入）',
    title VARCHAR(50) DEFAULT '' COMMENT '生成的小红书标题',
    content TEXT COMMENT '生成的小红书正文',
    tags VARCHAR(200) DEFAULT '' COMMENT '话题标签，英文逗号分隔',
    create_time DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    update_time DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    INDEX idx_create_time (create_time)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='文案生成记录表';