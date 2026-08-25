from fastapi import APIRouter, Depends, UploadFile

from ..dependencies.auth import get_current_user
from ..schemas.common import ApiResponse
from ..services.image_service import MAX_IMAGE_SIZE, save_image, validate_image_url
from ..utils.exceptions import ImageUploadException

router = APIRouter(
    prefix="/images",
    tags=["图片管理"],
    dependencies=[Depends(get_current_user)],
)


@router.post("/upload", response_model=ApiResponse, response_model_by_alias=True)
async def upload_image(file: UploadFile) -> ApiResponse:
    file_bytes = await file.read(MAX_IMAGE_SIZE + 1)
    if len(file_bytes) > MAX_IMAGE_SIZE:
        raise ImageUploadException(
            f"图片大小超过限制（最大 {MAX_IMAGE_SIZE // 1024 // 1024}MB）"
        )
    url = await save_image(file_bytes, file.filename or "unnamed")
    return ApiResponse(data={"image_url": url, "filename": file.filename})


@router.post("/validate-url", response_model=ApiResponse, response_model_by_alias=True)
async def validate_url(image_url: str) -> ApiResponse:
    result = await validate_image_url(image_url)
    return ApiResponse(data=result)
