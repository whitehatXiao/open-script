from django.http import JsonResponse

class ApiResponse(JsonResponse):
    """自定义API响应格式"""

    def __init__(self,
                 data=None,
                 code=200,
                 message="success",
                 **kwargs):
        # 构建标准数据结构
        response_data = {
            "code": code,
            "data": data if data is not None else [],
            "message": message
        }

        # 继承JsonResponse实现
        super().__init__(
            data=response_data,
            status=code,
            **kwargs
        )