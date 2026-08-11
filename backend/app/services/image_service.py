import aiofiles
import base64
import io
import uuid
from pathlib import Path
from urllib.parse import urlparse

import aiohttp
from PIL import Image

from ..core.config import UPLOAD_DIR
from ..utils.exceptions import ImageUploadException, ImageUrlException


ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".gif", ".webp", ".bmp"}
MAX_IMAGE_SIZE = 10 * 1024 * 1024


def _validate_extension(filename: str) -> None:
    ext = Path(filename).suffix.lower()
    if ext not in ALLOWED_EXTENSIONS:
        raise ImageUploadException(f"不支持的图片格式：{ext}，允许的格式：{', '.join(ALLOWED_EXTENSIONS)}")


def _generate_safe_filename(original_filename: str) -> str:
    ext = Path(original_filename).suffix.lower()
    return f"{uuid.uuid4().hex}{ext}"


async def save_image(file_bytes: bytes, original_filename: str) -> str:
    _validate_extension(original_filename)

    if len(file_bytes) > MAX_IMAGE_SIZE:
        raise ImageUploadException(f"图片大小超过限制（最大 {MAX_IMAGE_SIZE // 1024 // 1024}MB）")

    try:
        img = Image.open(io.BytesIO(file_bytes))
        img.verify()
    except Exception:
        raise ImageUploadException("图片文件损坏或无效")

    safe_name = _generate_safe_filename(original_filename)
    save_path = UPLOAD_DIR / safe_name

    async with aiofiles.open(save_path, "wb") as f:
        await f.write(file_bytes)

    return f"/uploads/{safe_name}"


async def validate_image_url(image_url: str) -> dict:
    parsed = urlparse(image_url)
    if parsed.scheme not in ("http", "https"):
        raise ImageUrlException("图片URL必须以 http:// 或 https:// 开头")
    if not parsed.netloc:
        raise ImageUrlException("图片URL域名无效")

    try:
        timeout = aiohttp.ClientTimeout(total=15)
        async with aiohttp.ClientSession(timeout=timeout) as session:
            async with session.head(image_url, allow_redirects=True) as resp:
                if resp.status != 200:
                    raise ImageUrlException(f"图片URL无法访问（HTTP {resp.status}）")
                content_type = resp.headers.get("Content-Type", "")
                if not content_type.startswith("image/"):
                    raise ImageUrlException(f"URL不是图片类型：{content_type}")
                content_length = int(resp.headers.get("Content-Length", 0))
                if content_length > MAX_IMAGE_SIZE:
                    raise ImageUrlException(f"图片大小超过限制（最大 {MAX_IMAGE_SIZE // 1024 // 1024}MB）")
    except ImageUrlException:
        raise
    except Exception as e:
        raise ImageUrlException(f"图片URL校验失败：{str(e)}")

    return {
        "valid": True,
        "content_type": content_type,
        "content_length": content_length,
    }


async def image_to_base64(image_source: str, image_type: int) -> str:
    if image_type == 1:
        file_path = UPLOAD_DIR / Path(image_source).name
        if not file_path.exists():
            raise ImageUploadException("图片文件不存在")
        async with aiofiles.open(file_path, "rb") as f:
            data = await f.read()
    elif image_type == 2:
        timeout = aiohttp.ClientTimeout(total=15)
        async with aiohttp.ClientSession(timeout=timeout) as session:
            async with session.get(image_source) as resp:
                if resp.status != 200:
                    raise ImageUrlException(f"无法下载图片（HTTP {resp.status}）")
                data = await resp.read()
    else:
        raise ImageUploadException("无效的图片类型")

    if len(data) > MAX_IMAGE_SIZE:
        raise ImageUploadException(f"图片大小超过限制（最大 {MAX_IMAGE_SIZE // 1024 // 1024}MB）")

    return base64.b64encode(data).decode("utf-8")
