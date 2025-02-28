from app.utils.metrics import count_logs_by_message, calculate_request_rate


class MetricsService:
    @staticmethod
    def get_metrics():
        """Collect and return various metrics from the log file."""
        total_requests = count_logs_by_message("Received request for moderation")
        success_count = count_logs_by_message("Moderation completed successfully")
        error_count = count_logs_by_message("Error")
        request_rate = calculate_request_rate()

        return {
            "total_requests": total_requests,
            "success_count": success_count,
            "error_count": error_count,
            "request_rate": request_rate,
        }
