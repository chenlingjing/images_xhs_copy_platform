import json

import httpx

from ..core.config import settings
from ..prompts import (
    DEFAULT_PRODUCT_NAME,
    DEFAULT_TARGET_AUDIENCE,
    DEFAULT_TONE_STYLE,
    SYSTEM_PROMPT,
    USER_PROMPT,
)
from ..utils.exceptions import LLMCallException, LLMParseException


class LLMService:
    def __init__(self) -> None:
        self.api_key = settings.QWEN_API_KEY
        self.model = settings.QWEN_MODEL
        self.base_url = settings.QWEN_BASE_URL.rstrip("/")

    async def call_vision(
        self,
        image_base64: str,
        product_name: str = "",
        target_audience: str = "",
        tone_style: str = "",
    ) -> dict:
        if not self.api_key:
            raise LLMCallException("大模型 API Key 未配置")

        system_prompt = SYSTEM_PROMPT
        user_prompt = USER_PROMPT.format(
            tone_style=tone_style or DEFAULT_TONE_STYLE,
            product_name=product_name or DEFAULT_PRODUCT_NAME or "无",
            target_audience=target_audience or DEFAULT_TARGET_AUDIENCE or "通用",
        )

        payload = {
            "model": self.model,
            "input": {
                "messages": [
                    {
                        "role": "system",
                        "content": system_prompt,
                    },
                    {
                        "role": "user",
                        "content": [
                            {"image": f"data:image/png;base64,{image_base64}"},
                            {"text": user_prompt},
                        ],
                    }
                ]
            },
            "parameters": {
                "result_format": "message",
                "temperature": 0.7,
                "max_tokens": 1000,
            },
        }

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

        try:
            async with httpx.AsyncClient(timeout=60.0) as client:
                resp = await client.post(
                    f"{self.base_url}/services/aigc/text2image/text-generation",
                    headers=headers,
                    json=payload,
                )
        except httpx.ConnectError as e:
            raise LLMCallException(f"大模型 API 连接失败：{str(e)}")
        except httpx.TimeoutException:
            raise LLMCallException("大模型 API 请求超时")
        except Exception as e:
            raise LLMCallException(f"大模型 API 调用异常：{str(e)}")

        if resp.status_code != 200:
            raise LLMCallException(
                f"大模型 API 返回错误（HTTP {resp.status_code}）：{resp.text}"
            )

        try:
            return self._parse_response(resp.json())
        except LLMParseException:
            raise
        except Exception as e:
            raise LLMParseException(f"大模型响应解析异常：{str(e)}")

    def _parse_response(self, response_data: dict) -> dict:
        try:
            output = response_data.get("output", {})
            choices = output.get("choices", [])
            if not choices:
                raise LLMParseException("大模型响应中没有 choices 字段")
            message = choices[0].get("message", {})
            content = message.get("content", "")
            if isinstance(content, list):
                content = content[0].get("text", "") if content else ""
            elif isinstance(content, dict):
                content = content.get("text", "")
            elif not isinstance(content, str):
                content = str(content)

            content = content.strip()

            if content.startswith("```"):
                content = content.strip("```json").strip("```").strip()

            try:
                result = json.loads(content)
                return self._validate_result(result)
            except json.JSONDecodeError:
                return {
                    "title": "",
                    "content": content,
                    "tags": [],
                }
        except LLMParseException:
            raise
        except Exception as e:
            raise LLMParseException(f"大模型响应解析异常：{str(e)}")

    def _validate_result(self, result: dict) -> dict:
        title = str(result.get("title", ""))[:50]
        content = str(result.get("content", ""))
        tags_raw = result.get("tags", [])
        tags = [str(t) for t in tags_raw if str(t)]

        return {
            "title": title,
            "content": content,
            "tags": tags,
        }


llm_service = LLMService()
