from pydantic import BaseModel


class MetricsResponse(BaseModel):
    total_requests: int
    success_count: int
    error_count: int
    request_rate: float
