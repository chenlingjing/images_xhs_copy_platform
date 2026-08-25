-- Docker entrypoint 会使用 MYSQL_DATABASE 指定的数据库执行此脚本。

CREATE TABLE IF NOT EXISTS users (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(50) NOT NULL UNIQUE,
    email VARCHAR(120) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    role VARCHAR(20) NOT NULL DEFAULT 'user',
    avatar TEXT,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    last_active_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_users_role (role),
    INDEX idx_users_last_active_at (last_active_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='平台用户表';

-- 文案生成记录表（核心业务表）
CREATE TABLE IF NOT EXISTS generate_record (
    id BIGINT PRIMARY KEY AUTO_INCREMENT COMMENT '主键ID',
    user_id BIGINT NULL COMMENT '所属用户ID',
    image_type TINYINT DEFAULT 1 COMMENT '图片类型：1-本地上传 2-URL链接',
    image_url VARCHAR(500) DEFAULT '' COMMENT '图片存储路径/在线URL',
    product_name VARCHAR(100) DEFAULT '' COMMENT '产品名称（用户可选输入）',
    target_audience VARCHAR(100) DEFAULT '' COMMENT '目标人群（用户可选输入）',
    tone_style VARCHAR(50) DEFAULT '' COMMENT '语气风格（用户可选输入）',
    title VARCHAR(50) DEFAULT '' COMMENT '生成的小红书标题',
    content TEXT COMMENT '生成的小红书正文',
    tags VARCHAR(200) DEFAULT '' COMMENT '话题标签，英文逗号分隔',
    status VARCHAR(20) NOT NULL DEFAULT 'pending' COMMENT '生成状态',
    error_message VARCHAR(500) NOT NULL DEFAULT '' COMMENT '失败原因',
    duration_ms INT NOT NULL DEFAULT 0 COMMENT '生成耗时（毫秒）',
    create_time DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    update_time DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    INDEX idx_create_time (create_time),
    INDEX idx_generate_user_id (user_id),
    INDEX idx_generate_status (status),
    CONSTRAINT fk_generate_user FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='文案生成记录表';

CREATE TABLE IF NOT EXISTS auth_sessions (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    token_hash VARCHAR(64) NOT NULL UNIQUE,
    user_id BIGINT NOT NULL,
    expires_at DATETIME NOT NULL,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_auth_sessions_user_id (user_id),
    INDEX idx_auth_sessions_expires_at (expires_at),
    CONSTRAINT fk_auth_session_user FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='用户登录会话表';
