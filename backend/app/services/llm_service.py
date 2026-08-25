import json
import re

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
            "messages": [
                {
                    "role": "system",
                    "content": system_prompt,
                },
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": user_prompt,
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/png;base64,{image_base64}",
                            },
                        },
                    ],
                },
            ],
            "temperature": 0.7,
            "max_tokens": 1000,
        }

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

        try:
            async with httpx.AsyncClient(timeout=60.0) as client:
                resp = await client.post(
                    f"{self.base_url}/chat/completions",
                    headers=headers,
                    json=payload,
                )
        except httpx.ConnectError:
            raise LLMCallException("无法连接大模型服务")
        except httpx.TimeoutException:
            raise LLMCallException("大模型 API 请求超时")
        except Exception:
            raise LLMCallException("大模型 API 调用异常")

        if resp.status_code != 200:
            raise LLMCallException(
                f"大模型 API 返回错误（HTTP {resp.status_code}）"
            )

        try:
            return self._parse_response(resp.json())
        except LLMParseException:
            raise
        except Exception:
            raise LLMParseException("大模型响应解析异常")

    def _parse_response(self, response_data: dict) -> dict:
        try:
            choices = response_data.get("choices")
            if not choices:
                output = response_data.get("output", {})
                choices = output.get("choices", [])

            if not choices:
                raise LLMParseException("大模型响应中没有 choices 字段")

            message = choices[0].get("message", {})
            content = message.get("content", "")

            if isinstance(content, list):
                text_parts = []
                for item in content:
                    if isinstance(item, dict):
                        if item.get("type") in {"text", "output_text"}:
                            text_parts.append(str(item.get("text", "")))
                        elif "text" in item:
                            text_parts.append(str(item.get("text", "")))
                content = "".join(text_parts)
            elif isinstance(content, dict):
                content = content.get("text", "")
            elif not isinstance(content, str):
                content = str(content)

            content = (content or "").strip()
            if not content:
                raise LLMParseException("大模型响应中没有正文内容")

            if content.startswith("```"):
                content = re.sub(r"^```(?:json)?\s*", "", content, flags=re.IGNORECASE | re.DOTALL)
                content = re.sub(r"\s*```$", "", content, flags=re.DOTALL)

            candidate_texts = [content]
            match = re.search(r"\{.*\}", content, flags=re.DOTALL)
            if match:
                candidate_texts.insert(0, match.group(0))

            for candidate in candidate_texts:
                try:
                    result = json.loads(candidate)
                    if isinstance(result, dict):
                        return self._validate_result(result)
                except json.JSONDecodeError:
                    continue

            return {
                "title": "",
                "content": content,
                "tags": [],
            }
        except LLMParseException:
            raise
        except Exception:
            raise LLMParseException("大模型响应解析异常")

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
