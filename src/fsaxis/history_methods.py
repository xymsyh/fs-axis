import os
from datetime import datetime
import sys

# 获取当前脚本所在目录
script_dir = os.path.dirname(os.path.abspath(__file__))

# 读取历史记录的函数，根据参数确定文件名
def read(record_type):
    file_name = f'history_{record_type}.md'  # 根据参数确定文件名
    file_path = os.path.join(script_dir, file_name)
    
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            history = file.readlines()
        return history
    except FileNotFoundError:
        print(f"文件 {file_name} 不存在")
        return []

# 写入修改记录的函数，根据参数确定文件名
def write(record_type, modification, time=None):
    print("历史记录写入中……")

    file_name = f'history_{record_type}.md'  # 根据参数确定文件名
    file_path = os.path.join(script_dir, file_name)

    if time is None:
        time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # 使用当前时间，包括秒

    # 检查modification是否为多行文本
    if '\n' in modification:
        modification = modification.replace('\n', '\\n')  # 将换行符替换为字符形式「\n」

    with open(file_path, 'a', encoding='utf-8') as file:
        file.write(f'\n{time}: {modification}')

def delete_last_lines(record_type, num_lines):
    print("正在删除历史记录……")

    file_name = f'history_{record_type}.md'  # 根据参数确定文件名
    file_path = os.path.join(script_dir, file_name)

    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            lines = file.readlines()

        # 检查是否有足够的行来删除
        if num_lines > len(lines):
            print(f"错误：文件只有 {len(lines)} 行，无法删除 {num_lines} 行")
            return

        # 删除最后num_lines行
        new_lines = lines[:-num_lines]

        with open(file_path, 'w', encoding='utf-8') as file:
            file.writelines(new_lines)

        print(f"成功删除了最后 {num_lines} 行")

    except FileNotFoundError:
        print(f"文件 {file_name} 不存在")

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

# 示例使用1
if __name__ == "__main__":
    history22 = read("line")
    print(history22)

'''sys.exit()
# 示例使用2
if __name__ == "__main__":
    record_type = "cell"  # 指定记录类型，可以根据需要修改
    # 读取历史记录
    history = read(record_type)
    print(f"历史记录 ({record_type}):")
    for entry in history:
        print(entry.strip())

    # 添加新的修改记录
    new_modification = "更新了单元格内容"
    write(record_type, new_modification)
    print(f"已添加新的修改记录 ({record_type}): {new_modification}")

    print(read("line"))'''