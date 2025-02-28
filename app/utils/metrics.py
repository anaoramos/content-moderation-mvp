from datetime import datetime

LOG_FILE = "server.log"


def count_logs_by_message(message: str) -> int:
    """Count the number of times a specific message appears in the log file.

    Args:
        message (str): The specific log message to count.

    Returns:
        int: The number of occurrences of the message in the log file.
    """
    count = 0
    with open(LOG_FILE, "r") as file:
        for line in file:
            if message in line:
                count += 1

    return count


def calculate_request_rate(time_window_seconds=60) -> float:
    """Calculate the request rate over a rolling time window (e.g., last 60 seconds).

    Args:
        time_window_seconds (int): The duration (in seconds) to look back for rate calculation.

    Returns:
        float: Requests per second based on the last `time_window_seconds` seconds.
    """
    request_times = []

    with open(LOG_FILE, "r") as file:
        for line in file:
            if "Received request for moderation" in line:
                timestamp_str = line.split(" ")[0] + " " + line.split(" ")[1]
                timestamp = datetime.strptime(timestamp_str, "%Y-%m-%d %H:%M:%S,%f")
                request_times.append(timestamp)

    if not request_times:
        return 0

    now = datetime.now()

    relevant_requests = [timestamp for timestamp in request_times if
                         (now - timestamp).total_seconds() <= time_window_seconds]

    if not relevant_requests:
        return 0

    request_rate = len(relevant_requests) / time_window_seconds

    return round(request_rate, 4)
