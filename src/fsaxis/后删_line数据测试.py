from datetime import datetime

def insert_current_time(line_data):
    current_time = datetime.now().strftime("%H:%M")
    
    if line_data == "[起床[]起床]" or line_data == "[入睡[]入睡]":
        line_data = line_data.replace("[]", f"[{current_time}]")
    
    return line_data

# 调用示例
input_data = "[起床[]起床]"
result = insert_current_time(input_data)
print(result)