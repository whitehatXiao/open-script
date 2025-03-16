# type/api_response.py
from fastapi.responses import JSONResponse
from typing import Any, Optional, Dict

class ApiResponse:
    """FastAPI 兼容的标准 API 响应格式"""

    def __init__(
            self,
            data: Optional[Any] = None,
            code: int = 200,
            message: str = "success",
            headers: Optional[Dict] = None
    ):
        self.content = {
            "code": code,
            "data": data if data is not None else {},
            "message": message
        }
        self.status_code = code
        self.headers = headers or {}

    def to_response(self) -> JSONResponse:
        """转换为 FastAPI 的 JSONResponse"""
        return JSONResponse(
            content=self.content,
            status_code=self.status_code,
            headers=self.headers
        )
