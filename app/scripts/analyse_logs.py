import os
from datetime import datetime

LOG_FILE = "../../server.log"


def count_logs_by_message(log_file: str, message: str)-> int:
    """Count the number of times a specific message appears in the log file.

    Args:
        log_file (str): Path to the log file.
        message (str): The specific log message to count.

    Returns:
        int: The number of occurrences of the message in the log file.
    """
    count = 0
    with open(log_file, 'r') as file:
        for line in file:
            if message in line:
                count += 1

    return count


def calculate_request_rate(log_file: str) -> float:
    """Calculate the request rate based on log timestamps.

    Args:
        log_file (str): Path to the log file.

    Returns:
        float: Requests per second calculated from log timestamps.
    """
    total_requests = 0
    first_timestamp = None
    last_timestamp = None

    with open(log_file, 'r') as file:
        for line in file:
            if "Received request for moderation" in line:
                total_requests += 1
                timestamp_str = line.split(" ")[0] + " " + line.split(" ")[1]
                timestamp = datetime.strptime(timestamp_str, "%Y-%m-%d %H:%M:%S,%f")

                if first_timestamp is None:
                    first_timestamp = timestamp
                last_timestamp = timestamp

    if first_timestamp is None or last_timestamp is None or total_requests == 0:
        return 0

    duration = (last_timestamp - first_timestamp).total_seconds()
    request_rate = total_requests / duration if duration > 0 else 0
    return request_rate


def main():
    if not os.path.exists(LOG_FILE):
        print(f"Log file {LOG_FILE} does not exist.")
        return

    total_requests = count_logs_by_message(LOG_FILE, "Received request for moderation")
    print(f"Total requests: {total_requests}")

    success_count = count_logs_by_message(LOG_FILE, "Moderation completed successfully")
    print(f"Successful requests: {success_count}")

    error_count = count_logs_by_message(LOG_FILE, "Error")
    print(f"Error requests: {error_count}")

    request_rate = calculate_request_rate(LOG_FILE)
    print(f"Request rate: {request_rate:.2f} requests per second")


if __name__ == "__main__":
    main()
