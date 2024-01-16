def time_formatting(log_data):
    from datetime import datetime, timedelta

    # Current time for reference
    current_time = datetime.now()

    # Function to convert time to a relative time string
    def time_ago(time):
        diff = current_time - time
        seconds = diff.total_seconds()

        if seconds < 60:
            return f"{int(seconds)}秒前"
        elif seconds < 3600:
            return f"{int(seconds // 60)}分钟前"
        elif seconds < 86400:
            return f"{int(seconds // 3600)}小时前"
        else:
            return f"{int(seconds // 86400)}天前"

    # Processing the log data to convert times
    converted_log_data = []
    for entry in log_data:
        time_str, log_entry = entry.split(': ', 1)
        log_time = datetime.strptime(time_str, '%Y-%m-%d %H:%M:%S')
        converted_log_data.append(f"{time_ago(log_time)}: {log_entry}")

    print(converted_log_data)
    return converted_log_data



# --- 下为测试 ---

log_data = [
    '2024-01-15 22:02:00: 测试\n',
    '2024-01-15 22:03:19: 测试\n',
    '2024-01-15 22:03:24: 测试\n',
    '2024-01-15 22:07:30: 测试\n',
    '2024-01-16 15:39:36: 测试\n',
    '2024-01-16 15:48:36: 测试\n',
]

time_formatting(log_data)