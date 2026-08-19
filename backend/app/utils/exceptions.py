class AppException(Exception):
    def __init__(self, code: int = 400, message: str = "请求失败"):
        self.code = code
        self.message = message
        super().__init__(message)


class ImageUploadException(AppException):
    def __init__(self, message: str = "图片上传失败"):
        super().__init__(code=400, message=message)


class ImageUrlException(AppException):
    def __init__(self, message: str = "图片URL无效"):
        super().__init__(code=400, message=message)


class LLMCallException(AppException):
    def __init__(self, message: str = "大模型调用失败"):
        super().__init__(code=500, message=message)


class LLMParseException(AppException):
    def __init__(self, message: str = "大模型返回解析失败"):
        super().__init__(code=500, message=message)


class DatabaseException(AppException):
    def __init__(self, message: str = "数据库操作失败"):
        super().__init__(code=500, message=message)


class ConfigException(AppException):
    def __init__(self, message: str = "配置错误"):
        super().__init__(code=500, message=message)
